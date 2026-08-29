"""
Demo interface for the ITU AI Readiness gap analyser.

    python3 src/cli.py coverage            full node-by-node coverage matrix
    python3 src/cli.py gaps                the gap register
    python3 src/cli.py scenarios           list evaluation scenarios
    python3 src/cli.py run S3              run one scenario against the KB
    python3 src/cli.py ask "..."           free-text query against the corpus
"""

from __future__ import annotations

import json
import pathlib
import sys
import textwrap

from kb import KnowledgeBase
from gapfinder import analyse, METHOD_GAP, SCOPE_GAP, POLICY_GAP, CURRENCY_GAP

ROOT = pathlib.Path(__file__).resolve().parent.parent

# The corpus contains Arabic. Windows pipes stdout as cp1252 by default, which
# raises UnicodeEncodeError on the first Arabic character - so the tool works
# in the terminal and crashes when redirected. Force UTF-8, and degrade rather
# than die if a character still cannot be represented.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

BOLD, DIM, RED, YEL, GRN, CYN, OFF = (
    "\033[1m", "\033[2m", "\033[31m", "\033[33m", "\033[32m", "\033[36m", "\033[0m",
)

KIND_COLOUR = {
    METHOD_GAP: RED,
    SCOPE_GAP: RED,
    POLICY_GAP: YEL,
    CURRENCY_GAP: DIM,
}


def rule(title: str = "") -> None:
    print(f"\n{BOLD}{'=' * 78}{OFF}")
    if title:
        print(f"{BOLD}{title}{OFF}")
        print(f"{BOLD}{'=' * 78}{OFF}")


def wrap(text: str, indent: int = 4) -> str:
    return textwrap.fill(
        text, width=78, initial_indent=" " * indent, subsequent_indent=" " * indent
    )


def cmd_coverage(kb: KnowledgeBase) -> None:
    rule("NODE COVERAGE MATRIX  -  ITU-T Y.3172 pipeline against the policy corpus")
    total = covered = 0
    for node, findings in kb.full_report().items():
        print(f"\n{BOLD}{node}{OFF}")
        for f in findings:
            total += 1
            if f.covered and not f.method_published:
                # The duty exists and binds. No method of compliance is
                # published, so it can be neither demonstrated nor audited.
                mark, colour = "DUTY ONLY", YEL
                cites = ", ".join(
                    i for i, d in kb.docs.items()
                    if f.concern in d.get("governs_without_method", [])
                )[:52]
            elif f.covered:
                covered += 1
                mark, colour = "COVERED  ", GRN
                cites = ", ".join(
                    c.doc_id for c in f.citations if c.binding and not c.scope_limit
                )[:52]
            else:
                mark, colour = "NO COVER ", RED
                cites = ", ".join(f"{i}*" for i in f.scoped_out[:2])[:52]
                cites = cites or ", ".join(f"{c.doc_id}*" for c in f.citations[:2])[:52] or "-"
            print(f"  {colour}{mark}{OFF} {f.concern:<28} {DIM}{cites}{OFF}")
    print(f"\n{BOLD}{covered}/{total} concerns governed by a binding, in-scope instrument.{OFF}")
    print(f"{DIM}DUTY ONLY = the obligation binds, but no method of compliance is published{OFF}")
    print(f"{DIM}* = relevant instrument, but non-binding, scope-limited, or silent on this concern{OFF}")


def cmd_gaps(kb: KnowledgeBase) -> None:
    gaps = analyse(kb)
    order = {METHOD_GAP: 0, SCOPE_GAP: 1, POLICY_GAP: 2, CURRENCY_GAP: 3}
    gaps.sort(key=lambda g: (order[g.kind], g.node))

    rule(f"GAP REGISTER  -  {len(gaps)} findings")
    for gap in gaps:
        colour = KIND_COLOUR[gap.kind]
        tag = f" [{gap.gap_id}]" if gap.gap_id else ""
        print(f"\n{colour}{BOLD}{gap.kind}{OFF}{tag}  {BOLD}{gap.node}{OFF} / {gap.concern}")
        print(wrap(gap.statement))
        print(f"{DIM}{wrap('Evidence: ' + '; '.join(gap.evidence))}{OFF}")
        print(f"{CYN}{wrap('-> ' + gap.recommendation)}{OFF}")


def cmd_scenarios() -> None:
    data = json.loads((ROOT / "data" / "scenarios.json").read_text(encoding="utf-8"))
    rule("EVALUATION SCENARIOS")
    for s in data["scenarios"]:
        print(f"\n  {BOLD}{s['id']}{OFF}  [{s['kind']}]  {s['title']}")
        print(f"{DIM}{wrap(s['question'], 6)}{OFF}")


def run_scenario(kb: KnowledgeBase, scenario_id: str) -> dict | None:
    data = json.loads((ROOT / "data" / "scenarios.json").read_text(encoding="utf-8"))
    match = next(
        (s for s in data["scenarios"] if s["id"].upper() == scenario_id.upper()), None
    )
    if not match:
        return None

    concerns = match.get("concerns")
    findings = []
    for node in match["nodes"]:
        node_concerns = concerns or kb.node_concerns[node]
        for concern in node_concerns:
            if concern in kb.node_concerns[node]:
                f = kb.concern_finding(node, concern)
                if f.covered and not f.method_published:
                    status = "duty_only"
                elif f.covered:
                    status = "covered"
                else:
                    status = "not_governed"
                findings.append(
                    {
                        "node": node,
                        "concern": concern,
                        "status": status,
                        "citations": [
                            {
                                "doc_id": c.doc_id,
                                "title": c.title,
                                "url": c.url,
                                "binding": c.binding,
                                "scope_limit": c.scope_limit,
                                "currency_warning": c.currency_warning,
                            }
                            for c in f.citations[:3]
                        ],
                        "scoped_out": [
                            {
                                "doc_id": doc_id,
                                "title": kb.docs[doc_id]["title"],
                                "url": kb.docs[doc_id]["url"],
                                "scope_limit": kb.docs[doc_id]["scope_limit"],
                            }
                            for doc_id in f.scoped_out
                        ],
                    }
                )

    unmet = [f for f in findings if f["status"] != "covered"]
    return {
        "scenario": match,
        "findings": findings,
        "unmet_count": len(unmet),
        "total_count": len(findings),
        "expected_finding": match["expected_finding"],
    }


def cmd_run(kb: KnowledgeBase, scenario_id: str) -> None:
    result = run_scenario(kb, scenario_id)
    if not result:
        print(f"No scenario {scenario_id}. Try: python3 src/cli.py scenarios")
        return
    match = result["scenario"]

    rule(f"{match['id']}  -  {match['title']}   [{match['kind']}]")
    for i, step in enumerate(match["steps"], 1):
        print(f"\n{BOLD}Step {i}.{OFF}")
        print(wrap(step))

    print(f"\n{BOLD}QUESTION{OFF}")
    print(wrap(match["question"]))

    print(f"\n{BOLD}KNOWLEDGE BASE CONSULTATION{OFF}")
    for f in result["findings"]:
        if f["status"] == "duty_only":
            status = f"{YEL}DUTY IMPOSED, NO METHOD PUBLISHED{OFF}"
        elif f["status"] == "covered":
            status = f"{GRN}GOVERNED{OFF}"
        else:
            status = f"{RED}NOT GOVERNED{OFF}"
        print(f"\n  {f['node']} / {f['concern']}: {status}")

        if f["status"] != "covered":
            for doc in f["scoped_out"]:
                line = "- {}: {}  [OUT OF SCOPE: {}]".format(
                    doc["doc_id"], doc["title"], doc["scope_limit"])
                print(f"{DIM}{wrap(line, 6)}{OFF}")
                print(f"{DIM}{wrap(doc['url'], 8)}{OFF}")

        scoped_ids = {d["doc_id"] for d in f["scoped_out"]}
        rest = [c for c in f["citations"] if c["doc_id"] not in scoped_ids]
        if not rest and not f["scoped_out"] and f["status"] == "covered":
            print(f"{DIM}{wrap('No instrument in the corpus addresses this.', 6)}{OFF}")
        for c in rest[:3]:
            flags = []
            if not c["binding"]:
                flags.append("non-binding")
            if c.get("scope_limit"):
                flags.append(f"OUT OF SCOPE: {c['scope_limit']}")
            if c.get("currency_warning"):
                flags.append(f"CURRENCY: {c['currency_warning']}")
            suffix = f"  [{'; '.join(flags)}]" if flags else "  [binding, in scope]"
            entry = "- " + c["doc_id"] + ": " + c["title"] + suffix
            print(f"{DIM}{wrap(entry, 6)}{OFF}")
            print(f"{DIM}{wrap(c['url'], 8)}{OFF}")

    print(f"\n{BOLD}FINDING{OFF}")
    print(wrap(result["expected_finding"]))
    unmet = result["unmet_count"]
    ok = result["total_count"] - unmet
    if unmet:
        print(
            f"\n{RED}{BOLD}{unmet} of {result['total_count']} concerns raised by this "
            f"scenario are either ungoverned or governed without any published method "
            f"of compliance.{OFF}"
            + (f"{DIM}\n  The remaining {ok} {'is' if ok == 1 else 'are'} "
               f"properly governed.{OFF}" if ok else "")
        )


def cmd_ask(kb: KnowledgeBase, query: str) -> None:
    rule(f'QUERY: "{query}"')
    hits = kb.search(query, k=6)
    if not hits:
        print("\n  No matching passage in the corpus.")
        return
    for c in hits:
        flags = []
        if not c.binding:
            flags.append("non-binding")
        if c.scope_limit:
            flags.append("scope-limited")
        if c.currency_warning:
            flags.append("currency warning")
        tag = f" {DIM}({', '.join(flags)}){OFF}" if flags else f" {GRN}(binding){OFF}"
        print(f"\n  {BOLD}{c.doc_id}{OFF}  score={c.score}{tag}")
        print(wrap(c.title, 4))
        print(f"{DIM}{wrap(c.snippet + ' ...', 6)}{OFF}")
        print(f"{DIM}{wrap(c.url, 6)}{OFF}")


def main() -> None:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return
    kb = KnowledgeBase()
    cmd = args[0]
    if cmd == "coverage":
        cmd_coverage(kb)
    elif cmd == "gaps":
        cmd_gaps(kb)
    elif cmd == "scenarios":
        cmd_scenarios()
    elif cmd == "run" and len(args) > 1:
        cmd_run(kb, args[1])
    elif cmd == "ask" and len(args) > 1:
        cmd_ask(kb, " ".join(args[1:]))
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
