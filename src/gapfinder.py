"""
Gap analysis engine.

Three kinds of gap are distinguished, because they call for different remedies:

  POLICY GAP     - no binding instrument governs this concern at all.
  SCOPE GAP      - an instrument exists and is on point, but its own stated
                   scope excludes systems like ours. The most dangerous kind,
                   because a reader skimming the corpus will believe the
                   concern is covered.
  METHOD GAP     - an obligation exists but no method is published by which
                   compliance can be demonstrated or audited.
  CURRENCY GAP   - the governing instrument has lapsed or is undated.

The distinction matters for the fourth hackathon criterion: a policymaker can
act on "publish a method" far more readily than on "there is no policy".
"""

from __future__ import annotations

import json
import pathlib
from dataclasses import asdict, dataclass

from kb import KnowledgeBase, ConcernFinding

import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

POLICY_GAP = "POLICY GAP"
SCOPE_GAP = "SCOPE GAP"
METHOD_GAP = "METHOD GAP"
CURRENCY_GAP = "CURRENCY GAP"

# Concerns where an obligation is known to exist without a published method.
METHOD_GAP_CONCERNS = {
    ("PP", "deidentification_method"),
    ("PP", "reidentification_risk"),
    ("PP", "anonymisation"),
    ("SRC", "referral_content_standard"),
}


@dataclass
class Gap:
    node: str
    concern: str
    kind: str
    statement: str
    gap_id: str | None
    evidence: list[str]
    recommendation: str


RECOMMENDATIONS = {
    ("PP", "deidentification_method"): (
        "Publish an identifier schedule and a re-identification risk methodology "
        "for health data, comparable to HIPAA Safe Harbor and Expert Determination."
    ),
    ("PP", "reidentification_risk"): (
        "Specify an acceptable residual re-identification risk threshold and the "
        "method by which it is to be measured."
    ),
    ("PP", "anonymisation"): (
        "Define which attributes constitute direct and indirect identifiers in "
        "health data, so that 'permanent' anonymisation becomes auditable."
    ),
    ("P", "human_oversight"): (
        "Extend an 'enhance, not replace' duty beyond the medical-device route, "
        "keyed to clinical consequence rather than device classification."
    ),
    ("P", "override"): (
        "Require a documented clinician override pathway for any AI system whose "
        "output influences patient routing or prioritisation."
    ),
    ("P", "advisory_vs_blocking"): (
        "Distinguish advisory from blocking AI enforcement in policy, and require "
        "that systems affecting care access default to advisory."
    ),
    ("P", "threshold_justification"): (
        "Require that any operational threshold in a health AI system cite a "
        "published clinical or regulatory source."
    ),
    ("M", "model_validation"): (
        "Establish a validation regime for health AI keyed to clinical impact "
        "rather than device classification."
    ),
    ("M", "accuracy_certification"): (
        "Designate an accredited body for health-AI performance assessment, "
        "extending the IS0304 conformance model beyond interoperability."
    ),
    ("M", "benchmarking"): (
        "Publish national reference datasets and benchmarks for health AI, "
        "including Arabic-language clinical text."
    ),
    ("M", "bias_evaluation"): (
        "Require demographic subgroup performance reporting for health AI "
        "deployed in Saudi facilities."
    ),
    ("SINK", "ai_disclosure"): (
        "Require disclosure that an AI system contributed to any health "
        "judgement communicated to a clinician or patient."
    ),
    ("SINK", "language_accessibility"): (
        "Address Arabic dialect and vocabulary variation in health AI "
        "performance requirements."
    ),
    ("SINK", "impairment_accessibility"): (
        "Extend accessibility requirements to health AI interfaces for users "
        "with hearing or mobility impairment."
    ),
    ("SRC", "referral_content_standard"): (
        "Publish a minimum referral dataset defining the content a referral "
        "document must carry, as several national health systems do."
    ),
    ("D", "ai_security"): (
        "Introduce AI-specific controls into the national cybersecurity "
        "baseline (ECC), which presently contains none."
    ),
    ("C", "infrastructure_reliability"): (
        "Issue a current, dated successor to the lapsed telehealth regulations."
    ),
}


def classify(finding: ConcernFinding) -> str | None:
    """Classify a concern, or return None if it is properly governed.

    Order matters. A method gap is precisely the case where an obligation
    exists AND is governed, but no method of compliance is published - so it
    must be tested before coverage, not after. Testing coverage first made the
    method-gap branch unreachable and reported the re-identification duty as
    satisfied, which is the opposite of the finding.
    """
    if not finding.method_published:
        return METHOD_GAP

    if finding.covered:
        return None

    if (finding.node, finding.concern) in METHOD_GAP_CONCERNS:
        return METHOD_GAP

    # On-point binding instruments exist, but every one of them excludes this
    # system by its own scope clause. Taken from the corpus, not from retrieval.
    if finding.scoped_out:
        return SCOPE_GAP

    return POLICY_GAP


def analyse(kb: KnowledgeBase) -> list[Gap]:
    gaps: list[Gap] = []
    for node, findings in kb.full_report().items():
        for finding in findings:
            kind = classify(finding)
            if not kind:
                continue

            evidence = []
            for doc_id in finding.scoped_out:
                doc = kb.docs[doc_id]
                evidence.append(f"{doc_id} (binding) [SCOPE-LIMITED: {doc['scope_limit']}]")
            if not finding.method_published:
                for doc_id, doc in kb.docs.items():
                    if (finding.concern in doc.get("governs_without_method", [])
                            and doc.get("binding") and not doc.get("scope_limit")):
                        evidence.append(
                            f"{doc_id} (binding) [IMPOSES THE DUTY, PUBLISHES NO METHOD]")
            already = set(finding.scoped_out)
            if not finding.method_published:
                already |= {
                    i for i, d in kb.docs.items()
                    if finding.concern in d.get("governs_without_method", [])
                    and d.get("binding") and not d.get("scope_limit")
                }
            for cite in finding.citations[:3]:
                if cite.doc_id in already:
                    continue
                note = ""
                if cite.scope_limit:
                    note = f" [SCOPE-LIMITED: {cite.scope_limit}]"
                elif cite.currency_warning:
                    note = f" [CURRENCY: {cite.currency_warning}]"
                kind_label = "binding" if cite.binding else "non-binding"
                evidence.append(f"{cite.doc_id} ({kind_label}){note}")
            if not evidence:
                evidence = ["No document in the corpus addresses this concern."]

            gaps.append(
                Gap(
                    node=node,
                    concern=finding.concern,
                    kind=kind,
                    statement=finding.gap_statement
                    or f"No binding instrument governs '{finding.concern.replace('_',' ')}' at the {node} node.",
                    gap_id=finding.gap_id,
                    evidence=evidence,
                    recommendation=RECOMMENDATIONS.get(
                        (node, finding.concern),
                        "Issue guidance addressing this concern for non-device health AI.",
                    ),
                )
            )
    # Corpus-level findings. G1 and G3 are not properties of any single
    # node-concern pair - they are statements about the shape of the corpus as
    # a whole - so they never surface through the node walk and must be
    # emitted explicitly, or the register silently omits two findings the
    # report relies on.
    for gid in ("G1", "G3"):
        gap = kb.known_gaps.get(gid)
        if not gap or not gap.get("corpus_level"):
            continue
        if gid == "G1":
            evidence = [
                f"{i} (binding) [SCOPE-LIMITED: {d['scope_limit']}]"
                for i, d in kb.docs.items()
                if d.get("scope_limit") and d.get("binding")
                and "SFDA" in d.get("issuer", "")
            ]
            rec = ("Extend health-AI regulation to systems that influence clinical "
                   "workflow without meeting the medical device definition, keyed to "
                   "clinical consequence rather than device classification.")
        else:
            evidence = ["LAW-HEALTH-PROF (binding) [professional-duty statute, not a records standard]",
                        "No Saudi statute governing electronic health records was located."]
            rec = ("Enact or designate an instrument governing electronic health "
                   "records as such, rather than relying on a practitioner conduct "
                   "provision and a general data protection article.")
        gaps.append(
            Gap(node=gap["node"], concern="corpus_level_finding", kind=SCOPE_GAP if gid == "G1" else POLICY_GAP,
                statement=gap["statement"], gap_id=gid,
                evidence=evidence or ["No in-scope binding instrument located."],
                recommendation=rec))

    # Instruments relied upon in practice that have lapsed or carry no date.
    # These do not surface through node coverage - an undated guideline is
    # still consulted daily - so they are reported in their own right.
    for doc_id, doc in kb.docs.items():
        warning = doc.get("currency_warning")
        if not warning:
            continue
        gaps.append(
            Gap(
                node=", ".join(doc.get("nodes", [])) or "-",
                concern="instrument_currency",
                kind=CURRENCY_GAP,
                statement=f"{doc['title']} is relied upon in practice but {warning[0].lower()}{warning[1:]}.",
                gap_id="G7",
                evidence=[f"{doc_id} ({'binding' if doc.get('binding') else 'non-binding'})"],
                recommendation="Issue a current, dated successor instrument, or formally withdraw it.",
            )
        )

    return gaps


def main() -> None:
    kb = KnowledgeBase()
    gaps = analyse(kb)

    order = {METHOD_GAP: 0, SCOPE_GAP: 1, POLICY_GAP: 2, CURRENCY_GAP: 3}
    gaps.sort(key=lambda g: (order[g.kind], g.node))

    out = ROOT / "output" / "gap_report.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps([asdict(g) for g in gaps], indent=2), encoding="utf-8")

    print(f"Corpus: {len(kb.docs)} documents, {len(kb.chunks)} chunks\n")
    by_kind: dict[str, int] = {}
    for gap in gaps:
        by_kind[gap.kind] = by_kind.get(gap.kind, 0) + 1
    for kind, count in sorted(by_kind.items()):
        print(f"  {kind:<14} {count}")
    print(f"\n{len(gaps)} gaps written to output/gap_report.json")


if __name__ == "__main__":
    main()
