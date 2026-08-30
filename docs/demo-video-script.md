# Demo Video Script — 7 minutes

Read this aloud while clicking through the **5-step browser demo**. Timings are guides. English throughout.

**Before you start recording**

- Run `python src/demo_server.py` and open http://localhost:8080
- Browser maximised, zoom 110–125%
- Click through the stepper or use **Start demo tour**
- Turn on subtitles/captions

---

## 0:00 — 0:40 · Step 1: What is this?

> Hello. We are [NAMES], and our submission is the Referral Screening Governance Gap Analyser, in the health domain.
>
> This tool checks whether Saudi law and policy are ready for a proposed healthcare AI — before you build or deploy it. It is not a clinical AI. It is not ChatGPT. There is no trained referral model.
>
> We propose an AI that screens referral letters. What we built is a governance analyser that maps your deployment to ITU-T Y.3172 and checks it against twenty-nine real policy instruments.

*(Screen: Step 1 — proposed vs built boxes, overview stats.)*

---

## 0:40 — 1:25 · Step 2: Describe your AI

> Click **Start assessment**. The Ehalati referral-screening preset is preloaded — a fixed profile, not free-form knobs. Hybrid de-identification, advisory output, named clinician.
>
> Saudi Arabia processed seven hundred and fifty-five thousand e-referrals in twenty twenty-three to twenty-four. The Ministry's own Medical Referrals Centre recommends AI triage. We built for that use case.

*(Click **Run assessment** on Step 2.)*

---

## 1:25 — 2:45 · Step 3: What did we find?

> Four steps: we mapped your profile to Y.3172, activated governance concerns, checked twenty-nine instruments, and classified gaps.
>
> Look at the shape of the pipeline. Source and Collector are almost green. Model is entirely red. The rules stop exactly where the AI starts.
>
> Click any node to see its concerns. Green means covered. Amber means a duty exists but no compliance method is published. Red is a gap.
>
> The headline is gap G4 — re-identification risk. The obligation binds. The method does not.

*(Expand PP node. Point at material blockers.)*

---

## 2:45 — 3:35 · Step 4: Proof on a document

> Before the law, the document. Synthetic referral — no real patient.
>
> Left: before de-identification. National ID, phone, medical record number. Right: after. Every direct identifier removed.
>
> Read what survives. "Brother of the mayor of Al-Quwayiyah." Everyone in a town that size knows who that is. That is gap G4 on a document.

*(Step 4 — before/after columns.)*

---

## 3:35 — 4:45 · Step 5: What to do next

> Twenty-two findings, each with a recommended owner. SDAIA: publish an identifier schedule. SFDA: extend human oversight beyond device classification. MOH: publish a minimum referral dataset. NCA: add AI to the cybersecurity baseline.
>
> Three standards gaps for ITU: Y.3172's preprocessing node has no privacy obligation; it is silent on residency boundaries; it has no notion of advisory versus blocking enforcement.

*(Step 5 — gaps by authority, readiness factors.)*

---

## 4:45 — 5:30 · Competitor curveball (optional live demo)

> Go back to Step 2. Switch preset to **Competitor: auto-reject referrals**. Run again.
>
> A vendor auto-rejects with no human review. Is that lawful? Yes. Every part of it. Good practice in Saudi health AI is currently optional.

---

## 5:30 — 6:10 · Reference material

> Open **Reference material** for the full thirty-five-concern matrix, live corpus search, and policy instrument table. Download the knowledge base JSON for expert review.

---

## 6:10 — 6:50 · Limits and close

> We are direct about limits. No Gulf study exists. No clinical-outcome proof. Referral acceptance improved without AI. What is new is a reproducible way to show where governance stops.
>
> The knowledge base, code, and gap register are in the repository. Thank you.

---

## If a judge adds a scenario live

1. Name the technical failure first.
2. Open **Reference material → Search corpus** and query live.
3. Give the verdict either way — checking is the point of what you built.
