"""Self-test: every command runs, and every figure the report claims holds.

Run before recording the demo or submitting. It checks two things that matter
and are easy to get wrong: that nothing crashes, and that the numbers printed
on screen are the numbers written in the report.

    python src/selftest.py
"""

from __future__ import annotations

import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CLI = [sys.executable, str(ROOT / "src" / "cli.py")]

passed: list[str] = []
failed: list[str] = []


def check(name: str, condition: bool, detail: str = "") -> None:
    (passed if condition else failed).append(f"{name}{'  -> ' + detail if detail and not condition else ''}")
    print(f"  {'PASS' if condition else 'FAIL'}  {name}" + (f"   {detail}" if detail and not condition else ""))


def run(*args: str) -> tuple[int, str]:
    r = subprocess.run(CLI + list(args), capture_output=True, text=True,
                       encoding="utf-8", errors="replace", cwd=ROOT)
    return r.returncode, r.stdout + r.stderr


print("\n1. Every command exits cleanly")
for args in ([], ["coverage"], ["gaps"], ["scenarios"],
             ["run", "S1"], ["run", "S2"], ["run", "S3"], ["run", "S4"], ["run", "S5"],
             ["ask", "re-identification risk assessment"]):
    code, out = run(*args)
    label = " ".join(args) or "(menu)"
    check(f"cli.py {label}", code == 0 and "Traceback" not in out)

print("\n2. Bad input fails gracefully rather than crashing")
for args, expect in ((["run", "S99"], "No scenario"), (["wibble"], "Demo interface")):
    code, out = run(*args)
    check(f"cli.py {' '.join(args)}", code == 0 and expect in out and "Traceback" not in out)

print("\n3. Corpus is complete")
sys.path.insert(0, str(ROOT / "src"))
from kb import KnowledgeBase  # noqa: E402

kb = KnowledgeBase()
missing = []
for doc_id in kb.docs:
    body = kb._load_text(doc_id)
    if len(body) < 400:
        missing.append(doc_id)
check("every instrument has text", not missing,
      f"no text for {missing} - run 'python src/fetch_corpus.py' to download them")
check("29 instruments in corpus", len(kb.docs) == 29, f"found {len(kb.docs)}")

print("\n4. No extract is shadowed by a stale copy in data/text")
shadowed = []
for path in (ROOT / "data" / "extracts").glob("*.txt"):
    twin = ROOT / "data" / "text" / path.name
    if not twin.exists():
        continue
    copy = twin.read_text(encoding="utf-8", errors="ignore")
    # Full downloaded text legitimately supersedes an extract. Only a stale
    # *copy of the extract itself* is a problem.
    if "CURATED EXTRACT" in copy[:400] and copy != path.read_text(encoding="utf-8", errors="ignore"):
        shadowed.append(path.stem)
check("extracts are authoritative", not shadowed,
      f"stale copies in data/text: {shadowed} - delete them")

print("\n5. Figures match what the report claims")
report = kb.full_report()
governed = sum(1 for n in report for f in report[n] if f.covered and f.method_published)
duty_only = sum(1 for n in report for f in report[n] if f.covered and not f.method_published)
total = sum(len(v) for v in report.values())
check("17 of 35 governed", (governed, total) == (17, 35), f"got {governed}/{total}")
check("1 duty-only concern", duty_only == 1, f"got {duty_only}")

subprocess.run([sys.executable, str(ROOT / "src" / "gapfinder.py")],
               capture_output=True, cwd=ROOT)
gaps = json.loads((ROOT / "output" / "gap_report.json").read_text(encoding="utf-8"))
kinds: dict[str, int] = {}
for g in gaps:
    kinds[g["kind"]] = kinds.get(g["kind"], 0) + 1
check("22 findings in the register", len(gaps) == 22, f"got {len(gaps)}")
check("kind breakdown 4/7/9/2",
      (kinds.get("METHOD GAP"), kinds.get("SCOPE GAP"),
       kinds.get("POLICY GAP"), kinds.get("CURRENCY GAP")) == (4, 7, 9, 2),
      str(kinds))

ids = {g["gap_id"] for g in gaps if g["gap_id"]}
expected_ids = {"G1", "G2", "G3", "G4", "G5", "G6", "G7", "G9", "G10", "G11"}
check("every gap id the report names is in the register",
      expected_ids <= ids, f"missing: {sorted(expected_ids - ids)}")

print("\n6. The headline finding reads correctly")
code, out = run("run", "S2")
check("S2 shows the duty/method distinction",
      "DUTY IMPOSED, NO METHOD PUBLISHED" in out)
check("S2 tallies 4 of 4", "4 of 4 concerns" in out)
check("S2 does not print any concern as plainly GOVERNED",
      ": GOVERNED" not in out)

code, out = run("run", "S4")
check("S4 tallies 4 of 5", "4 of 5 concerns" in out)

print("\n7. The referral demo makes the abstract argument concrete")
r = subprocess.run([sys.executable, str(ROOT / "src" / "referral_demo.py")],
                   capture_output=True, text=True, encoding="utf-8",
                   errors="replace", cwd=ROOT)
demo = r.stdout + r.stderr
check("referral_demo.py runs", r.returncode == 0 and "Traceback" not in demo)
check("data is labelled synthetic", "SYNTHETIC DATA" in demo)
check("de-identification removes direct identifiers", "direct identifiers removed" in demo)
check("quasi-identifiers survive de-identification",
      "3 of 4 referrals still carry candidate quasi-identifiers" in demo)
check("the mayor's brother is flagged", "Brother of the mayor" in demo)
check("a complete, low-risk referral is not flagged", "nothing absent" in demo)

r2 = subprocess.run([sys.executable, str(ROOT / "src" / "referral_demo.py"), "1"],
                    capture_output=True, text=True, encoding="utf-8",
                    errors="replace", cwd=ROOT)
check("single-sample view runs", r2.returncode == 0 and "Traceback" not in (r2.stdout + r2.stderr))

print("\n8. Search returns primary law, not our own analysis")
code, out = run("ask", "re-identification risk assessment")
first = next((l for l in out.splitlines() if "score=" in l), "")
check("top hit is the binding Saudi instrument", "IS0303" in first, f"got: {first.strip()}")
check("no table-of-contents fragments returned", "......" not in out)

print("\n9. Synthetic identifiers are unmistakably synthetic")
samples = json.loads((ROOT / "data" / "samples" / "referrals.json").read_text(encoding="utf-8"))
ids = [r["patient"]["national_id"] for r in samples["referrals"]]
check("every sample id uses the reserved 10000000xx block",
      all(i.startswith("10000") for i in ids), str(ids))
check("sample file carries a synthetic warning", "SYNTHETIC DATA" in samples["_warning"])

print("\n10. Assessor is deterministic and presets differ")
from assessor import assess, activate_concerns, load_rules, schema  # noqa: E402

rules = load_rules()
screening = rules["presets"]["referral_screening"]["values"]
blocking = rules["presets"]["referral_blocking"]["values"]
a1 = assess(screening, kb)
a2 = assess(screening, kb)
check("same inputs produce identical assessment", a1 == a2)
check("assessment schema exposes presets", "referral_screening" in schema()["presets"])
screen_concerns = {c.concern for c in activate_concerns(screening)}
block_concerns = {c.concern for c in activate_concerns(blocking)}
check("blocking preset activates advisory_vs_blocking", "advisory_vs_blocking" in block_concerns - screen_concerns)
check("screening preset activates audit_trail concern", "audit_trail" in screen_concerns - block_concerns)
check("assessment returns human labels", all("node_label" in f and "concern_label" in f for f in a1["findings"]))
check("material blockers have human labels",
      all("node_label" in b and "concern_label" in b for b in a1["material_blockers"]))
check("pipeline nodes include concern details",
      all("concerns" in n and isinstance(n["concerns"], list) for n in a1["pipeline"]))
check("pipeline concerns match activated findings",
      sum(len(n["concerns"]) for n in a1["pipeline"]) == len(a1["findings"]))

print("\n11. Referral analysis returns structured JSON")
from referral_demo import analyze_referral, load as load_referrals  # noqa: E402

ref = analyze_referral(load_referrals()["referrals"][0])
check("referral JSON has completeness", "completeness" in ref and ref["completeness"]["total"] == 6)
check("referral JSON flags mayor's brother", any("mayor" in c["snippet"].lower() for c in ref["residual_risk"]["candidates"]))
check("referral JSON has before/after documents",
      "document_before" in ref and "document_after" in ref)
check("after document removes identifiers",
      "REMOVED" in ref["document_after"]["patient"][0][1])

print("\n12. Demo server APIs respond")
from demo_server import app  # noqa: E402

client = app.test_client()
endpoints = [
    ("/api/overview", None),
    ("/api/assessment/schema", None),
    ("/api/evidence", None),
    ("/api/coverage", None),
    ("/api/readiness", None),
    ("/api/gaps", None),
    ("/api/scenarios", None),
    ("/api/scenarios/S2", None),
    ("/api/referrals", None),
    ("/api/referrals/1", None),
    ("/api/search?q=re-identification+risk+assessment", None),
    ("/api/corpus", None),
    ("/api/corpus/export", None),
    ("/api/methodology", None),
]
for path, _ in endpoints:
    r = client.get(path)
    check(f"GET {path}", r.status_code == 200 and r.is_json)

post = client.post("/api/assessment", json=screening)
check("POST /api/assessment", post.status_code == 200 and post.is_json)
overview = client.get("/api/overview").get_json()
check("overview corpus count matches kb", overview["corpus_documents"] == len(kb.docs))
export = client.get("/api/corpus/export").get_json()
check("corpus export has document_count", export["document_count"] == len(kb.docs))

page = client.get("/")
check("index page serves", page.status_code == 200 and b"Saudi Health AI Readiness Assessor" in page.data)
check("index has knowledge base nav", b"knowledge-base-btn" in page.data and b"Knowledge base" in page.data)
check("methodology endpoint has steps", len(client.get("/api/methodology").get_json()["steps"]) == 5)
methodology = client.get("/api/methodology").get_json()
check("methodology has workflow and insights", "workflow" in methodology and "insights" in methodology)
check("methodology has architecture paths", "architecture" in methodology and "on_premises" in methodology["architecture"])
check("methodology has no negations strip", "negations" not in methodology)
schema_data = client.get("/api/assessment/schema").get_json()
check("on-prem ML preset exists", "referral_onprem_ml" in schema_data["presets"])
check("gaps endpoint includes register", "register" in client.get("/api/gaps").get_json() and "G4" in client.get("/api/gaps").get_json()["register"])
gaps_reg = client.get("/api/gaps").get_json()["register"]["G4"]
check("gap register G4 has statement", "statement" in gaps_reg and gaps_reg.get("node_name") == "Preprocessor")

print("\n" + "=" * 62)
if failed:
    print(f"{len(failed)} CHECK(S) FAILED\n")
    for f in failed:
        print("  - " + f)
    sys.exit(1)
print(f"ALL {len(passed)} CHECKS PASSED - safe to record and submit.")
