"""Run a synthetic referral through the PP node, and show what survives.

    python src/referral_demo.py            all samples, summary
    python src/referral_demo.py 1          one sample, in full

This is the concrete form of the argument the rest of the submission makes in
the abstract. It does three things to a referral document:

  1. COMPLETENESS  - which of the six clinical fields are absent.
  2. DE-IDENTIFY   - remove every direct identifier, the way a field-based
                     de-identification stage does.
  3. RESIDUAL RISK - look at what is left and flag phrases that could still
                     identify the patient.

Step 3 is the point. Step 2 succeeds completely and step 3 still finds people.
A field-based de-identifier passes a document that names the mayor's brother,
because "the mayor's brother" is not a field.

And then the question that has no answer: is the output of step 2 lawfully
anonymised? Saudi law requires removal of direct AND indirect identifiers, and
requires a re-identification risk assessment. It publishes no identifier
schedule, no risk threshold and no method. So this script can flag candidates
and cannot adjudicate them - not because it is weak, but because there is
nothing to adjudicate against.

All data in data/samples/referrals.json is synthetic.
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

BOLD, DIM, RED, YEL, GRN, CYN, OFF = (
    "\033[1m", "\033[2m", "\033[31m", "\033[33m", "\033[32m", "\033[36m", "\033[0m",
)

# ---------------------------------------------------------------- direct IDs
# The identifiers a field-based stage removes. Each is a formal pattern: it can
# be written as a rule, so it can be removed by a rule.
DIRECT = [
    ("NATIONAL_ID", re.compile(r"\b[12]\d{9}\b")),
    ("PHONE", re.compile(r"(?:\+966[\s-]?|0)5\d{2}[\s-]?\d{3}[\s-]?\d{3}\b")),
    ("MRN", re.compile(r"\b[A-Z]{3}-[A-Z]{3}-\d{6,8}\b")),
    ("REG_NO", re.compile(r"SCFHS\s+Reg\.\s*\d+", re.I)),
    ("DATE", re.compile(r"\b\d{2}/\d{2}/\d{4}\b")),
]

# --------------------------------------------------------- quasi-identifiers
# Phrases that identify a person without being an identifier. None of these can
# be expressed as a field. Each pattern below is a heuristic, and heuristics
# are exactly what a published methodology would replace.
QUASI = [
    (re.compile(r"\b(?:brother|sister|son|daughter|wife|husband|father|mother|cousin|nephew|niece)\s+of\s+the\s+\w+", re.I),
     "named relationship to a public office-holder"),
    (re.compile(r"\bonly\s+\w+(?:\s+\w+)?\s+(?:at|in|of)\s+(?:the\s+)?[\w-]+", re.I),
     "sole holder of a role in a named place"),
    (re.compile(r"\b(?:mayor|governor|imam|principal|chief|director|sheikh)\b", re.I),
     "public office named"),
    (re.compile(r"\b(?:border|crossing|settlement|village|tribe)\b", re.I),
     "small or bounded community named"),
    (re.compile(r"\bAl-[A-Z][a-z]+\b"),
     "specific locality named"),
    (re.compile(r"\b(?:Friday prayer|Ramadan|Eid|Hajj|Umrah)\b", re.I),
     "narrow time window implied"),
    (re.compile(r"\b(?:father|mother|husband|wife)\s+works?\s+(?:at|in|for)\b", re.I),
     "family member's workplace named"),
]

CLINICAL_FIELDS = [
    ("history", "History"),
    ("examination", "Examination findings"),
    ("vital_signs", "Vital signs"),
    ("investigations", "Investigation results"),
    ("provisional_diagnosis", "Provisional diagnosis"),
    ("current_treatment", "Current treatment"),
]


def load() -> dict:
    return json.loads((ROOT / "data" / "samples" / "referrals.json").read_text(encoding="utf-8"))


def deidentify(text: str) -> tuple[str, list[str]]:
    """Remove every direct identifier. Report what was removed."""
    removed = []
    for label, pattern in DIRECT:
        for match in pattern.findall(text):
            removed.append(f"{label}: {match}")
        text = pattern.sub(f"[{label} REMOVED]", text)
    # Names are carried in dedicated fields in this format, so the stage
    # removes them structurally rather than by pattern. Free text is where
    # names escape - and where nothing structural can reach them.
    return text, removed


def residual_risk(text: str) -> list[tuple[str, str]]:
    found = []
    for pattern, why in QUASI:
        for match in pattern.findall(text):
            snippet = match if isinstance(match, str) else " ".join(match)
            found.append((snippet.strip(), why))
    seen, unique = set(), []
    for snippet, why in found:
        key = snippet.lower()
        if key not in seen:
            seen.add(key)
            unique.append((snippet, why))
    return unique


def format_referral_document(ref: dict, *, deidentified: bool = False) -> dict:
    """Human-readable referral view for before/after de-identification."""
    patient = ref["patient"]
    referring = ref["referring"]
    requested = ref["requested"]
    clinical = ref["clinical"]

    if deidentified:
        patient_fields = [
            ("National ID", "[NATIONAL_ID REMOVED]"),
            ("Date of birth", "[DATE REMOVED]"),
            ("Phone", "[PHONE REMOVED]"),
            ("MRN", "[MRN REMOVED]"),
            ("Name (Arabic)", "[NAME REMOVED]"),
            ("Name (English)", "[NAME REMOVED]"),
        ]
        physician = "[PHYSICIAN REMOVED]"
        facility = referring["facility"]
        date = "[DATE REMOVED]"
    else:
        patient_fields = [
            ("National ID", patient["national_id"]),
            ("Date of birth", patient.get("dob", "")),
            ("Phone", patient.get("phone", "")),
            ("MRN", patient.get("mrn", "")),
            ("Name (Arabic)", patient.get("name_ar", "")),
            ("Name (English)", patient.get("name_en", "")),
        ]
        physician = referring.get("physician", "")
        facility = referring["facility"]
        date = ref.get("date", "")

    clinical_lines = []
    for key, label in CLINICAL_FIELDS:
        value = clinical.get(key, "").strip()
        clinical_lines.append({
            "field": label,
            "value": value if value else "(absent)",
            "absent": not bool(value),
        })

    free_text = ref["free_text"]
    if deidentified:
        free_text, _ = deidentify(free_text)

    return {
        "ref": ref["ref"],
        "date": date,
        "patient": patient_fields,
        "referring": {
            "facility": facility,
            "physician": physician,
            "region": referring.get("region", ""),
        },
        "requested": {
            "specialty": requested.get("specialty", ""),
            "urgency": requested.get("urgency", ""),
        },
        "clinical": clinical_lines,
        "free_text": free_text,
    }


def analyze_referral(ref: dict) -> dict:
    """Structured referral analysis for API and CLI."""
    missing_keys = [
        key for key, _ in CLINICAL_FIELDS if not ref["clinical"].get(key, "").strip()
    ]
    missing_labels = [
        label for key, label in CLINICAL_FIELDS if key in missing_keys
    ]
    present = len(CLINICAL_FIELDS) - len(missing_keys)
    blob = json.dumps(ref, ensure_ascii=False)
    _, removed = deidentify(blob)
    free_text = ref["free_text"]
    clean_text, _ = deidentify(free_text)
    risks = [
        {"snippet": snippet, "reason": why}
        for snippet, why in residual_risk(free_text)
    ]
    return {
        "ref": ref["ref"],
        "specialty": ref["requested"]["specialty"],
        "urgency": ref["requested"]["urgency"],
        "region": ref["referring"]["region"],
        "synthetic": True,
        "document_before": format_referral_document(ref, deidentified=False),
        "document_after": format_referral_document(ref, deidentified=True),
        "free_text_before": ref["free_text"],
        "completeness": {
            "present": present,
            "total": len(CLINICAL_FIELDS),
            "missing_fields": missing_labels,
            "note": "No published national referral content standard. See gap G11.",
        },
        "deidentification": {
            "direct_identifiers_removed": len(removed),
            "removed": removed,
            "structural_fields_dropped": ["name_ar", "name_en", "physician"],
        },
        "residual_risk": {
            "candidate_count": len(risks),
            "candidates": risks,
            "free_text_after_deid": clean_text,
        },
    }


def show(ref: dict, verbose: bool) -> tuple[int, int]:
    data = analyze_referral(ref)
    print(f"\n{BOLD}{'=' * 74}{OFF}")
    print(f"{BOLD}{data['ref']}{OFF}   {data['specialty']} · "
          f"{data['urgency']} · {data['region']}")
    print(f"{BOLD}{'=' * 74}{OFF}")

    # ---- 1. completeness -------------------------------------------------
    missing = data["completeness"]["missing_fields"]
    present = data["completeness"]["present"]
    colour = GRN if not missing else (YEL if len(missing) < 4 else RED)
    print(f"\n{BOLD}1. COMPLETENESS{OFF}   {colour}{present}/{len(CLINICAL_FIELDS)} clinical fields present{OFF}")
    for label in missing:
        print(f"     {RED}absent{OFF}  {label}")
    if not missing:
        print(f"     {DIM}nothing absent{OFF}")
    print(f"{DIM}     Scored against: no published national standard. See gap G11.{OFF}")

    # ---- 2. de-identification -------------------------------------------
    removed = data["deidentification"]["removed"]
    print(f"\n{BOLD}2. DE-IDENTIFICATION{OFF}   {GRN}{len(removed)} direct identifiers removed{OFF}")
    for item in removed[: (99 if verbose else 4)]:
        print(f"     {DIM}{item}{OFF}")
    if not verbose and len(removed) > 4:
        print(f"     {DIM}... and {len(removed) - 4} more{OFF}")
    print(f"     {DIM}Structural fields also dropped: name_ar, name_en, physician{OFF}")

    # ---- 3. what survives ------------------------------------------------
    risks = data["residual_risk"]["candidates"]
    print(f"\n{BOLD}3. RESIDUAL RE-IDENTIFICATION RISK{OFF}   "
          f"{(RED if risks else GRN)}{len(risks)} candidate quasi-identifiers in free text{OFF}")
    if verbose or risks:
        print(f"\n{DIM}     Free text, after de-identification:{OFF}")
        clean = data["residual_risk"]["free_text_after_deid"]
        for line in [clean[i:i + 66] for i in range(0, len(clean), 66)]:
            print(f"     {line}")
        print()
    for item in risks:
        print(f"     {RED}flag{OFF}  \"{item['snippet']}\"")
        print(f"           {DIM}{item['reason']}{OFF}")
    if not risks:
        print(f"     {DIM}none detected{OFF}")

    return len(risks), len(missing)


def main() -> None:
    data = load()
    refs = data["referrals"]
    args = sys.argv[1:]

    print(f"\n{YEL}{BOLD}SYNTHETIC DATA{OFF}{YEL} - no real patient, clinician or facility "
          f"record is represented.{OFF}")

    if args and args[0].isdigit() and 1 <= int(args[0]) <= len(refs):
        risks, _ = show(refs[int(args[0]) - 1], verbose=True)
        totals = [risks]
    else:
        totals = [show(r, verbose=False)[0] for r in refs]

    flagged = sum(1 for t in totals if t)
    print(f"\n{BOLD}{'=' * 74}{OFF}")
    print(f"{BOLD}{flagged} of {len(totals)} referrals still carry candidate quasi-identifiers "
          f"after\nevery direct identifier has been removed.{OFF}")
    print(f"""
{CYN}The de-identification stage did its job. It removed every identifier that can
be expressed as a rule. What remains is text a clinician wrote to explain
themselves, and it identifies people anyway.

Whether these documents are lawfully anonymised is not a question this tool
can answer, and not because the tool is weak. Saudi law requires removal of
direct AND indirect identifiers, and requires a re-identification risk
assessment before release. It publishes no identifier schedule, no risk
threshold, and no method. There is nothing to adjudicate against.

That is gap G4, on a document rather than in the abstract.{OFF}
""")


if __name__ == "__main__":
    main()
