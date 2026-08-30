# Demo presentation transcript

What to **say**. Italic lines are screen cues.

Start on http://localhost:8080, Step 1.

---

## Opening and Step 1 — What is this?

- Health domain. Proposed system: AI screening of referral letters, before they enter Ehalati.
- Two questions: is it complete, and is it appropriate.
- Complete = diagnosis, examination, investigations, history, current treatment.
- Appropriate = does this patient need specialist transfer at all.
- Not a medical device. Evaluates a document. Does not diagnose.
- 755,000 e-referrals in 2023–24. MOH’s own Medical Referrals Centre recommends AI triage.
- This is not a trained model. No ChatGPT, no API key, nothing stochastic.
- This is a governance analyser: maps the workflow to ITU-T Y.3172, checks 29 real instruments.
- Saudi law, Saudi health standards, WHO, ITU.
- 17 of 35 concerns covered by a binding, in-scope instrument. The rest are gaps. Shape matters more than the number.
- Left: hybrid default — strip identifiers in hospital, then Saudi cloud. Also a fully on-prem path.
- Right: completeness checks, residual privacy flags, pipeline coverage, cited gaps with owners.
- A real operational model would need authorised MOH data, clinician labels, external validation. We have not done that.

*Start assessment.*

---

## Step 2 — Assess the workflow

- Three fixed presets — not a free-form form. Same preset, same result every time.
- Ehalati referral-screening is the default: administrative, hybrid, advisory, named clinician.
- On-premises ML: model never leaves the facility.
- Competitor auto-reject: blocking, no human — that lights up G2.
- Running the default: the responsible version.

*Run assessment.*

---

## Step 3 — What did we find?

- Four steps: map to seven Y.3172 nodes → activate concerns → check 29 instruments → classify.
- Headline: not ready. That is the honest result.
- Look at the shape, not the count.
- Source and Collector (left, Level 1, inside the hospital): almost green.
- Collection, confidentiality, residency, infrastructure — real binding law. PDPL, Law of Practicing Healthcare Professions, cloud controls.
- Model: entirely red. Sink: almost entirely red. That is where the AI sits.
- Saudi Arabia does not lack AI rules. **The rules stop exactly where the AI starts.**
- Green = binding, in-scope. Amber = duty binds, no published method. Red = gap.

*Open PP.*

- Preprocessing. De-identification inside the hospital. Headline is G4.
- Permanent anonymisation is required. SDAIA: remove direct *and* indirect identifiers, permanently.
- IS0303: re-identification risk assessment before release. Both duties bind.
- No identifier schedule. No risk threshold. No method.
- Operator cannot prove compliance. Regulator cannot audit. Method gap, not absence of law.
- US publishes both: HIPAA Safe Harbor and Expert Determination. Saudi Arabia has the duty, not the method.

*Open M.*

- Model. G1 and G5.
- Non-device workflow AI sits outside SFDA MDS-G-010. That guidance is good. It does not apply here, or to most hospital AI.
- No Saudi body validates model performance for non-device systems.
- Fastest-growing category: unregulated and unvalidated.
- Coverage is a curated legal judgement in the corpus file, not search. Retrieval only cites. Contest any line.

---

## Step 4 — Proof on a document

- Before the law, the document. Synthetic. No real patient.
- Left: as written. National ID, phone, MRN, name, date of birth.
- Right: after hybrid de-identification. Every direct identifier gone.
- The stage did not fail. Everything you can write as a rule was removed.
- Free text that survives: “Brother of the mayor of Al-Quwayiyah. Asked to be seen quickly.”
- Town of about 4,000. Everyone knows who that is. Not a field. No rule reaches it.

*If time: switch to Jeddah or Arar sample.*

- Same pattern: “only dialysis technician at the Al-Lith unit.” “Father works at the crossing.”
- Fourth sample has none of that — not indiscriminate flagging.
- Was this lawfully anonymised before it left the facility? Nobody can answer. No published test.
- That is G4 on a page, not in the abstract.
- Fully on-prem: text never hits the cloud, residency is structural. G4 still applies to extracts and audit logs.

---

## Step 5 — What to do next

- 22 findings. Each has an owner. Strategy input, not a deployment approval.
- **SDAIA:** identifier schedule + re-ID method, like HIPAA. Closes G4.
- **SFDA:** human oversight keyed to clinical consequence, not device class. “Enhance, not replace” should apply here. G2.
- **MOH:** you publish response-time standards, not a minimum referral dataset. CBAHI is survey criteria, not a spec a machine can apply. Publish the dataset. G11.
- **NCA:** ECC-2:2024, all 108 controls, no AI provision. Add AI to the cybersecurity baseline. G10.

**ITU / Y.3172**

- PP has no privacy obligation attached. A de-identification spec with a measurable threshold would close G4 once, for every country.
- Silent on which node boundary enforces residency. Level 1 / Level 2 split at PP is a candidate: identifiers never cross.
- Policy node has no advisory vs blocking. That distinction decides whether human oversight is real.

---

## Close

- Limits: no Gulf or Arabic operational study. Almost no global study shows better time-to-treatment.
- Referral acceptance already rose 74% → 90% without AI.
- Not claiming clinical outcomes. Claiming a reproducible map of where governance stops.
- Knowledge base, code, gap register: in the repo. Happy to take a scenario live.

---

## Extra time

### Competitor: auto-reject

*Step 2 → preset “Competitor: auto-reject referrals” → Run.*

- Rival product: auto-rejects below a completeness threshold. No human. Unpublished threshold. No clinical source.
- Urgent but poorly documented patient rejected twice before a clinician sees it.
- Lawful in Saudi Arabia today? Yes. Nothing prohibits it.
- Outside the device route: no HITL duty, no advisory duty, no threshold justification, no AI-disclosure duty.
- We impose all four voluntarily. A competitor imposing none is equally compliant.
- Good practice is optional. G2 at its sharpest.

### Knowledge base

*Header: Knowledge base.*

- 29 instruments: issuer, binding, provenance, URL. JSON download.
- Search “re-identification risk assessment.” Same query, same citations, every time. Term Frequency-Inverse Document Frequency (TF-IDF). No network. No model.
- Pipeline matrix: all 35 concerns, not only this workflow.
- Scenarios: S2 = mayor’s brother. S4 = competitor who does not ask.

---

## If a judge throws a scenario

- Name the technical failure first.
- Then: is there a binding instrument.
- If the answer is “unanswerable,” say so — that *is* G4.
- Search the corpus in front of them.
