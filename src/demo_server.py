"""Browser demo server for the Saudi Health AI Readiness Assessor."""

from __future__ import annotations

import json
import pathlib
import sys
from dataclasses import asdict

from flask import Flask, jsonify, request, send_from_directory

ROOT = pathlib.Path(__file__).resolve().parent.parent
WEB = ROOT / "web"
sys.path.insert(0, str(ROOT / "src"))

from assessor import assess, corpus_hash, load_rules, schema  # noqa: E402
from cli import run_scenario  # noqa: E402
from evidence import evidence_payload  # noqa: E402
from gapfinder import analyse, METHOD_GAP, POLICY_GAP, SCOPE_GAP, CURRENCY_GAP  # noqa: E402
from kb import KnowledgeBase  # noqa: E402
from labels import AUTHORITY_BY_GAP, concern_label, node_label  # noqa: E402
from readiness import readiness_payload  # noqa: E402
from referral_demo import analyze_referral, load as load_referrals  # noqa: E402

app = Flask(__name__, static_folder=str(WEB), static_url_path="")
_kb: KnowledgeBase | None = None


def kb() -> KnowledgeBase:
    global _kb
    if _kb is None:
        _kb = KnowledgeBase()
    return _kb


def _finding_status(f) -> str:
    if f.covered and not f.method_published:
        return "duty_only"
    if f.covered:
        return "covered"
    return "no_cover"


@app.get("/")
def index():
    return send_from_directory(WEB, "index.html")


@app.get("/api/overview")
def api_overview():
    k = kb()
    report = k.full_report()
    governed = sum(1 for n in report for f in report[n] if f.covered and f.method_published)
    duty_only = sum(1 for n in report for f in report[n] if f.covered and not f.method_published)
    total = sum(len(v) for v in report.values())
    gaps = analyse(k)
    return jsonify(
        {
            "corpus_documents": len(k.docs),
            "corpus_hash": corpus_hash(),
            "rules_version": load_rules()["version"],
            "governed": governed,
            "duty_only": duty_only,
            "total_concerns": total,
            "gap_count": len(gaps),
            "headline": f"{governed}/{total} concerns governed · rules stop where the AI starts",
        }
    )


@app.get("/api/assessment/schema")
def api_assessment_schema():
    return jsonify(schema())


@app.post("/api/assessment")
def api_assessment():
    values = request.get_json(force=True) or {}
    return jsonify(assess(values, kb()))


@app.post("/api/assessment/export")
def api_assessment_export():
    values = request.get_json(force=True) or {}
    result = assess(values, kb())
    return jsonify(result)


@app.get("/api/evidence")
def api_evidence():
    return jsonify(evidence_payload())


@app.get("/api/coverage")
def api_coverage():
    k = kb()
    report = k.full_report()
    nodes = []
    for node, findings in report.items():
        items = []
        for f in findings:
            items.append(
                {
                    "concern": f.concern,
                    "concern_label": concern_label(f.concern),
                    "status": _finding_status(f),
                    "gap_id": f.gap_id,
                    "citations": [
                        {"doc_id": c.doc_id, "title": c.title, "url": c.url, "binding": c.binding}
                        for c in f.citations[:3]
                    ],
                    "scoped_out": f.scoped_out,
                }
            )
        nodes.append({"node": node, "label": node_label(node), "concerns": items})
    return jsonify({"nodes": nodes})


@app.get("/api/readiness")
def api_readiness():
    return jsonify(readiness_payload())


@app.get("/api/gaps")
def api_gaps():
    k = kb()
    gaps = analyse(k)
    order = {METHOD_GAP: 0, SCOPE_GAP: 1, POLICY_GAP: 2, CURRENCY_GAP: 3}
    gaps.sort(key=lambda g: (order[g.kind], g.node))
    grouped: dict[str, list] = {}
    for gap in gaps:
        authority = AUTHORITY_BY_GAP.get(gap.gap_id or "", "General")
        grouped.setdefault(authority, []).append(
            {
                **asdict(gap),
                "concern_label": concern_label(gap.concern),
                "node_label": node_label(gap.node) if gap.node != "-" else gap.node,
                "authority": authority,
            }
        )
    return jsonify({"gaps": [asdict(g) for g in gaps], "by_authority": grouped})


@app.get("/api/scenarios")
def api_scenarios():
    data = json.loads((ROOT / "data" / "scenarios.json").read_text(encoding="utf-8"))
    return jsonify(data)


@app.get("/api/scenarios/<scenario_id>")
def api_scenario(scenario_id: str):
    result = run_scenario(kb(), scenario_id)
    if not result:
        return jsonify({"error": f"No scenario {scenario_id}"}), 404
    return jsonify(result)


@app.get("/api/referrals")
def api_referrals():
    data = load_referrals()
    return jsonify(
        {
            "synthetic_warning": data["_warning"],
            "referrals": [
                {
                    "index": i + 1,
                    "ref": r["ref"],
                    "specialty": r["requested"]["specialty"],
                    "region": r["referring"]["region"],
                }
                for i, r in enumerate(data["referrals"])
            ],
        }
    )


@app.get("/api/referrals/<int:index>")
def api_referral(index: int):
    data = load_referrals()
    refs = data["referrals"]
    if index < 1 or index > len(refs):
        return jsonify({"error": "Invalid referral index"}), 404
    return jsonify(analyze_referral(refs[index - 1]))


@app.get("/api/search")
def api_search():
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify({"hits": []})
    hits = kb().search(query, k=6)
    return jsonify(
        {
            "query": query,
            "hits": [
                {
                    "doc_id": c.doc_id,
                    "title": c.title,
                    "issuer": c.issuer,
                    "url": c.url,
                    "score": c.score,
                    "snippet": c.snippet,
                    "binding": c.binding,
                    "scope_limit": c.scope_limit,
                    "currency_warning": c.currency_warning,
                }
                for c in hits
            ],
        }
    )


@app.get("/api/corpus")
def api_corpus():
    k = kb()
    manifest = {
        m["id"]: m for m in json.loads((ROOT / "data" / "manifest.json").read_text(encoding="utf-8"))
    }
    docs = []
    for doc in sorted(k.corpus["documents"], key=lambda d: (d.get("jurisdiction") != "SA", d["issuer"])):
        prov = manifest.get(doc["id"], {})
        docs.append(
            {
                "id": doc["id"],
                "title": doc["title"],
                "issuer": doc["issuer"],
                "year": doc.get("year"),
                "jurisdiction": doc.get("jurisdiction", "SA"),
                "binding": doc.get("binding", False),
                "url": doc["url"],
                "nodes": doc.get("nodes", []),
                "provenance": prov.get("provenance", "unknown"),
                "chars": prov.get("chars"),
            }
        )
    saudi = sum(1 for d in docs if d["jurisdiction"] == "SA")
    return jsonify({"count": len(docs), "saudi_count": saudi, "documents": docs})


@app.get("/api/methodology")
def api_methodology():
    return jsonify(
        {
            "what": (
                "This prototype shows what Saudi healthcare organisations and policymakers "
                "need in place to use AI-assisted referral screening responsibly."
            ),
            "why": (
                "Saudi Arabia processed 755,000 e-referrals in 2023–24. The Ministry of "
                "Health recommends AI triage — but governance rules stop where the AI starts."
            ),
            "how": [
                "Analyse the referral workflow on synthetic documents",
                "Map the workflow to 7 ITU-T Y.3172 pipeline stages",
                "Activate governance concerns from the configured workflow",
                "Check each concern against 29 curated policy instruments",
                "Classify gaps and recommend actions by responsible authority",
            ],
            "workflow": {
                "title": "Referral workflow being assessed",
                "body": (
                    "An ML screening model checks referral documents for missing clinical "
                    "information and appropriateness signals. The default preset assumes "
                    "hybrid deployment: direct identifiers are stripped on-premises before "
                    "text crosses to a cloud screening service. An on-premises offline path "
                    "can run the same ML on full referral text inside the facility — removing "
                    "the separate de-identification export step and satisfying data residency "
                    "structurally when nothing leaves the hospital."
                ),
            },
            "insights": {
                "title": "Insights this prototype delivers now",
                "body": (
                    "Working completeness checks, deployment architecture comparison, "
                    "before/after de-identification (hybrid path), residual privacy-risk "
                    "flags, Y.3172 pipeline coverage, citation-backed policy gaps, and "
                    "authority-specific recommendations."
                ),
                "items": [
                    "Which clinical referral fields are missing from each example",
                    "How hybrid vs on-premises ML architectures change the privacy boundary",
                    "Which direct identifiers are removed before cloud processing (hybrid path)",
                    "Which contextual phrases still create re-identification risk",
                    "Which Y.3172 stages and governance concerns apply",
                    "Which concerns are covered and which are policy, scope, method, or currency gaps",
                    "Which authority can act on each gap and what is recommended",
                ],
            },
            "readiness_path": {
                "title": "What is needed for operational readiness?",
                "body": (
                    "The next stage is governed ML model development using authorised "
                    "MOH/SMARC referral data, clinician-defined labels, external validation, "
                    "and subgroup evaluation. On-premises offline deployment removes the "
                    "cloud export boundary but still requires a published de-identification "
                    "methodology for any secondary use or audit extracts."
                ),
            },
            "architecture": {
                "title": "Two deployment architectures",
                "hybrid": {
                    "label": "Hybrid (default preset)",
                    "steps": [
                        "Clinician drafts a referral inside the healthcare facility",
                        "On-premises preprocessing removes direct identifiers before text crosses the Level 1 boundary",
                        "ML screening service in Saudi cloud analyses de-identified clinical content",
                        "Advisory signal returned to a named clinician who remains responsible",
                    ],
                },
                "on_premises": {
                    "label": "On-premises offline ML",
                    "steps": [
                        "Clinician drafts a referral inside the healthcare facility",
                        "ML screening model runs entirely on-premises on full referral text — no cloud export",
                        "No separate de-identification export step required for residency",
                        "Advisory signal returned to a named clinician who remains responsible",
                    ],
                    "note": (
                        "When referral text never leaves the facility, cross-border residency "
                        "concerns at the cloud boundary are structurally addressed. Human "
                        "oversight, audit trails, and contextual quasi-identifiers (G4) still "
                        "require governance — but the export de-identification stage is no "
                        "longer the primary control."
                    ),
                },
            },
            "data_flow": [
                "A clinician drafts a referral inside the healthcare facility",
                "The on-premises preprocessing stage removes direct identifiers before text reaches the screening service or cloud layer",
                "The ML screening service analyses de-identified clinical content for completeness and referral-support signals",
                "An advisory signal is returned to a named clinician, who remains responsible for the decision",
            ],
            "tooltips": {
                "y3172": "ITU standard defining where AI sits in a data pipeline",
                "pp": "De-identification stage inside the hospital (Level 1 boundary)",
                "method_gap": "Law requires something, but no published way to prove compliance",
                "duty_only": "Obligation binds; compliance method is missing",
                "ai_readiness": "Whether governance, data, standards, and policy support safe deployment",
            },
            "status_meanings": {
                "covered": "A binding, in-scope instrument governs this concern",
                "duty_only": "Duty exists but no published compliance method",
                "method_gap": "Obligation exists; method to demonstrate compliance is missing",
                "policy_gap": "No binding instrument addresses this concern",
                "scope_gap": "Instrument exists but excludes systems like this one",
                "currency_gap": "Governing instrument has lapsed or is undated",
            },
            "steps": [
                {
                    "title": "What is this?",
                    "subtitle": "See what this referral-screening prototype reveals about Saudi healthcare AI readiness.",
                    "explain": (
                        "This prototype identifies the controls, evidence, data access, validation, "
                        "and policy changes required before AI-assisted referral screening can move "
                        "into operational use."
                    ),
                },
                {
                    "title": "Assess the referral workflow",
                    "subtitle": "Configure how patient data is handled, where processing occurs, and how outputs affect referrals.",
                    "explain": (
                        "These choices determine which governance concerns apply to the referral-screening "
                        "workflow. Changing advisory output to blocking activates additional human-oversight concerns."
                    ),
                },
                {
                    "title": "What did we find?",
                    "subtitle": "See which pipeline stages are governed and where readiness gaps remain.",
                    "explain": (
                        "The workflow was mapped to Y.3172, governance concerns were activated, "
                        "29 policy instruments were checked, and each concern was classified."
                    ),
                },
                {
                    "title": "Proof on a document",
                    "subtitle": "See how architecture choice affects privacy controls on a real referral shape.",
                    "explain": (
                        "The hybrid path removes direct identifiers on-premises before the ML "
                        "screening service sees the text — but contextual phrases can still "
                        "identify a patient (gap G4). An on-premises offline ML path processes "
                        "full referral text inside the facility, removing the export "
                        "de-identification step when nothing crosses the cloud boundary."
                    ),
                },
                {
                    "title": "What to do next",
                    "subtitle": "Authority-specific recommendations, sources, and export for policymakers.",
                    "explain": (
                        "Each gap has a recommended owner. This is input to national AI strategy and "
                        "standards work — not a deployment approval."
                    ),
                },
            ],
        }
    )


@app.get("/api/corpus/export")
def api_corpus_export():
    k = kb()
    manifest = json.loads((ROOT / "data" / "manifest.json").read_text(encoding="utf-8"))
    return jsonify(
        {
            "corpus_name": k.corpus.get("corpus_name"),
            "compiled": k.corpus.get("compiled"),
            "corpus_hash": corpus_hash(),
            "document_count": len(k.docs),
            "documents": k.corpus["documents"],
            "manifest": manifest,
            "node_concerns": k.node_concerns,
        }
    )


def main() -> None:
    print("Saudi Health AI Readiness Assessor")
    print("Open http://localhost:8080")
    app.run(host="127.0.0.1", port=8080, debug=False)


if __name__ == "__main__":
    main()
