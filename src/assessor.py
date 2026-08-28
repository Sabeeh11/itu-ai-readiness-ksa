"""Deterministic Saudi healthcare AI governance-readiness assessment."""

from __future__ import annotations

import hashlib
import json
import pathlib
from dataclasses import asdict, dataclass, field

from gapfinder import RECOMMENDATIONS, analyse, classify
from kb import KnowledgeBase, ConcernFinding
from labels import AUTHORITY_BY_GAP, concern_label, node_label

ROOT = pathlib.Path(__file__).resolve().parent.parent
RULES_PATH = ROOT / "data" / "assessment_rules.json"
CORPUS_PATH = ROOT / "data" / "corpus.json"


@dataclass
class ActivatedConcern:
    node: str
    concern: str
    rationale: str


@dataclass
class FindingResult:
    node: str
    concern: str
    status: str
    rationale: str
    gap_id: str | None = None
    gap_kind: str | None = None
    statement: str | None = None
    recommendation: str | None = None
    authority: str | None = None
    citations: list[dict] = field(default_factory=list)
    scoped_out: list[str] = field(default_factory=list)


def corpus_hash() -> str:
    return hashlib.sha256(CORPUS_PATH.read_bytes()).hexdigest()[:16]


def load_rules() -> dict:
    return json.loads(RULES_PATH.read_text(encoding="utf-8"))


def _match_when(values: dict, when: dict) -> bool:
    for key, expected in when.items():
        actual = values.get(key)
        if isinstance(expected, list):
            if actual not in expected:
                return False
        elif actual != expected:
            return False
    return True


def activate_concerns(values: dict, rules: dict | None = None) -> list[ActivatedConcern]:
    rules = rules or load_rules()
    activated: list[ActivatedConcern] = []
    seen: set[tuple[str, str]] = set()

    for node, concerns in rules["baseline_concerns"].items():
        for concern in concerns:
            key = (node, concern)
            if key not in seen:
                seen.add(key)
                activated.append(
                    ActivatedConcern(
                        node=node,
                        concern=concern,
                        rationale=rules["rationales"].get(
                            concern, "Baseline governance concern for deployed health AI."
                        ),
                    )
                )

    for rule in rules["concern_rules"]:
        if not _match_when(values, rule["when"]):
            continue
        key = (rule["node"], rule["concern"])
        if key in seen:
            continue
        seen.add(key)
        activated.append(
            ActivatedConcern(
                node=rule["node"],
                concern=rule["concern"],
                rationale=rules["rationales"].get(
                    rule["concern"], "Activated by the supplied deployment profile."
                ),
            )
        )

    return activated


def _finding_status(finding: ConcernFinding, gap_kind: str | None) -> str:
    if gap_kind:
        return gap_kind.lower().replace(" ", "_")
    if finding.covered and not finding.method_published:
        return "duty_only"
    if finding.covered:
        return "covered"
    return "no_cover"


def _serialize_citations(finding: ConcernFinding) -> list[dict]:
    out = []
    for c in finding.citations[:4]:
        out.append(
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
        )
    return out


def _serialize_finding(f: FindingResult) -> dict:
    return {
        **asdict(f),
        "concern_label": concern_label(f.concern),
        "node_label": node_label(f.node),
    }


def _gap_priority(gap_kind: str | None) -> int:
    if not gap_kind:
        return 9
    key = gap_kind.lower().replace(" ", "_")
    return {"method_gap": 0, "policy_gap": 1, "scope_gap": 2, "currency_gap": 3}.get(key, 9)


def assess(values: dict, kb: KnowledgeBase | None = None) -> dict:
    kb = kb or KnowledgeBase()
    rules = load_rules()
    activated = activate_concerns(values, rules)
    findings: list[FindingResult] = []

    for item in activated:
        raw = kb.concern_finding(item.node, item.concern)
        gap_kind = classify(raw)
        gap_id = raw.gap_id
        recommendation = RECOMMENDATIONS.get((item.node, item.concern))
        if gap_kind and gap_id and gap_id in AUTHORITY_BY_GAP:
            authority = AUTHORITY_BY_GAP[gap_id]
        elif gap_kind:
            authority = "MOH / SDAIA"
        else:
            authority = None

        findings.append(
            FindingResult(
                node=item.node,
                concern=item.concern,
                status=_finding_status(raw, gap_kind),
                rationale=item.rationale,
                gap_id=gap_id,
                gap_kind=gap_kind,
                statement=raw.gap_statement,
                recommendation=recommendation,
                authority=authority,
                citations=_serialize_citations(raw),
                scoped_out=list(raw.scoped_out),
            )
        )

    gaps = [f for f in findings if f.gap_kind]
    covered = [f for f in findings if f.status == "covered"]
    duty_only = [f for f in findings if f.status == "duty_only"]

    # Material blockers: method gaps first, then policy, then scope
    blockers = sorted(
        gaps,
        key=lambda f: (_gap_priority(f.gap_kind), f.node, f.concern),
    )[:3]

    if len(gaps) >= 5:
        readiness = "Not ready under the evidence in this corpus"
        summary = (
            f"This profile activates {len(findings)} governance concerns. "
            f"{len(covered)} are covered by binding in-scope instruments, "
            f"{len(duty_only)} impose a duty without a published compliance method, "
            f"and {len(gaps)} remain gaps or uncertainties. "
            "This is a policy-readiness assessment, not legal clearance."
        )
    elif gaps:
        readiness = "Proceed with material governance gaps unresolved"
        summary = (
            f"{len(gaps)} material gap(s) remain for this deployment profile. "
            "Address the blockers below before operational deployment."
        )
    else:
        readiness = "Largely governed on the included concerns"
        summary = (
            "No gap was identified among the activated concerns, though this corpus "
            "does not prove clinical safety or regulatory approval."
        )

    nodes = rules["node_activation"]["always"]
    serialized = [_serialize_finding(f) for f in findings]
    pipeline = []
    for node in nodes:
        node_findings = [f for f in serialized if f["node"] == node]
        pipeline.append(
            {
                "node": node,
                "label": node_label(node),
                "level": 1 if node in {"SRC", "C", "PP"} else 2,
                "concern_count": len(node_findings),
                "gap_count": sum(1 for f in node_findings if f.get("gap_kind")),
                "concerns": node_findings,
            }
        )

    return {
        "rules_version": rules["version"],
        "corpus_hash": corpus_hash(),
        "input": values,
        "readiness_summary": readiness,
        "executive_summary": summary,
        "counts": {
            "activated": len(findings),
            "covered": len(covered),
            "duty_only": len(duty_only),
            "gaps": len(gaps),
        },
        "material_blockers": [_serialize_finding(b) for b in blockers],
        "pipeline": pipeline,
        "findings": serialized,
        "disclaimer": (
            "Policy-readiness assessment based on the included corpus. "
            "Not legal advice, regulatory approval, or proof of clinical safety."
        ),
    }


def schema() -> dict:
    rules = load_rules()
    return {
        "rules_version": rules["version"],
        "fields": rules["fields"],
        "presets": rules["presets"],
    }
