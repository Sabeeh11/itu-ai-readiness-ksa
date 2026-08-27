# Demo Video Script — 7 minutes

Read this aloud while clicking. Timings are guides, not rules. English throughout — the organisers require the explanation in English even where source material is Arabic.

**Before you start recording**

- Terminal open, maximised, in the project folder
- Font size up (Ctrl + `+` a few times) so text is readable when compressed
- The report open in a second window, ready to switch to
- Have every command already typed out somewhere you can copy from — do not type live, you will make mistakes and it wastes seconds
- Turn on subtitles/captions in whatever you record with, or add them after

---

## 0:00 — 0:40 · Who and what

> Hello. We are [NAMES], and our submission is the Referral Screening Governance Gap Analyser, in the health domain.
>
> Saudi Arabia runs a national medical referral system called Ehalati. It processed seven hundred and fifty-five thousand referrals in 2023 to 2024. Screening those referrals is done by hand today.
>
> In 2025, twelve authors published an analysis of that system. Eight of them work at the Ministry of Health's Medical Referrals Centre — the body that actually operates it. Their recommendation was, and I quote, "integrating AI tools for referral triage to optimize patient allocation, thereby reducing unnecessary transfers."
>
> So we built for that. But the more interesting half of what we found is not the AI. It is what governs it.

*(Screen: just the terminal, nothing running yet.)*

---

## 0:40 — 1:25 · The use case and the setup

> Our system reads a referral document before it is submitted and answers two questions. Is it complete — does it carry a diagnosis, examination findings, investigation results. And is it appropriate — does this patient need transfer at all.
>
> Referral documents contain names, national ID numbers, addresses, dates of birth. So a de-identification stage runs inside the sending facility. The model never sees an identifier. Only de-identified text leaves the building.
>
> The setup is deliberately simple. Python, four standard libraries, no API keys, no network at query time. The knowledge base is twenty-nine real published instruments — Saudi law and regulation, plus WHO and ITU guidance. Twenty are indexed from their full downloaded text; the rest from curated extracts of their operative provisions, because several issuers block automated retrieval.

*(Type: `python src/check_corpus.py` — let it scroll, don't read it out.)*

> Twenty-nine instruments, none without text.

*(Note: the referral demo at 2:20 uses synthetic data. Say the word "synthetic" out loud when it appears — the organisers ban real confidential data, and volunteering it costs nothing.)*

---

## 1:25 — 2:20 · The coverage matrix

*(Type: `python src/cli.py coverage`)*

> This maps our system onto the seven nodes of the ITU-T Y point three one seven two machine learning pipeline, and for each node asks which published instruments govern the concerns arising there.
>
> Look at the shape of this.

*(Scroll to the top. Point at SRC and C.)*

> Source and Collector are almost entirely green. Saudi Arabia governs data collection, medical confidentiality, data residency and infrastructure properly. Real, binding law.

*(Scroll to M and SINK.)*

> Model is entirely red. Sink is almost entirely red.
>
> Seventeen of thirty-five concerns are governed by a binding, in-scope instrument. One more is amber — marked DUTY ONLY. That means the obligation binds, but no method of compliance is published. I will come back to that one.
>
> And the finding is not that Saudi Arabia has no AI rules. It is that **the rules stop exactly where the AI starts.**

---

## 2:20 — 3:10 · A referral, and what survives de-identification

*(Type: `python src/referral_demo.py 1`)*

> Before the law, the document. This is a synthetic referral — no real patient — built to the field structure the published research says the national system captures.
>
> Step one, completeness. One of six clinical fields present. No history, no examination, no investigations, no provisional diagnosis, no treatment. That is the failure pattern the last Saudi study of referral letter quality measured, and it is what our system is built to catch.
>
> Step two, de-identification. Six direct identifiers removed — national ID, phone, medical record number, registration number, dates. Names dropped structurally. That stage worked perfectly.
>
> Step three. Read what is left.

*(Point at the free text.)*

> "Brother of the mayor of Al-Quwayiyah." "Seen after Friday prayer."
>
> Every identifier is gone and the patient is still identifiable. In a town of that size, everyone knows who the mayor's brother is. That sentence is not a field. No rule removes it, because a clinician wrote it to explain themselves.
>
> Three of our four referrals still carry these after full de-identification. One does not — so this is not a tool that flags everything.
>
> So: was that document lawfully anonymised?

---

## 3:10 — 4:10 · Scenario 2 — the question with no answer

*(Type: `python src/cli.py run S2`)*

*(Let the output settle. Point at the amber DUTY ONLY line first, then the red ones.)*

> Look at the amber line. Re-identification risk assessment is marked as a duty that binds — IS0303 requires one before any de-identified release, and it is binding and in scope. That is not a loophole in our favour. It is the finding.
>
> SDAIA's guidance likewise requires removal of direct **and indirect** identifiers, in a way that permanently makes it impossible to identify the data subject.
>
> Both obligations are real. Neither instrument publishes an identifier schedule, a risk threshold, or any method by which either duty could be discharged.
>
> The obligation exists. The method does not. Which means the hospital cannot demonstrate compliance, and the regulator cannot audit it.
>
> We call this a method gap, and it is our headline finding. The comparison is HIPAA, which pairs a Safe Harbor list of eighteen identifiers with an Expert Determination standard. Saudi Arabia has the duty without either.

---

## 4:10 — 5:20 · Scenario 4 — the uncomfortable one

*(Type: `python src/cli.py run S4`)*

> This scenario is about a competitor, not about us.
>
> A vendor sells a rival product to the same hospital. It automatically rejects any referral scoring below a completeness threshold, and returns it without any human ever looking. The threshold is the vendor's own, unpublished, citing no clinical source. A patient with an atypical but urgent presentation is auto-rejected twice before a clinician sees the referral.
>
> Is that lawful in Saudi Arabia today?

*(Let it finish.)*

> Yes. Every part of it.
>
> Outside the medical-device route there is no Saudi obligation for human oversight. None requiring AI enforcement to be advisory rather than blocking. None requiring an operational threshold to cite a published source. None requiring anyone to disclose that AI made the decision.
>
> Our system imposes all four of those constraints on itself, voluntarily. A competitor that imposes none is exactly as compliant as we are.
>
> That is the sharpest way we can state gap G2. Good practice in Saudi health AI is currently optional, and the market does not reward it.

---

## 5:20 — 6:10 · The gap register

*(Type: `python src/cli.py gaps`)*

> Twenty-two findings, sorted into four kinds, because each needs a different remedy.
>
> A **method gap** is an obligation with no published way to comply. A **scope gap** is the dangerous one — a good, binding instrument exists and is directly on point, but its own scope excludes systems like ours. Anyone skimming the corpus concludes the concern is covered. It is not.
>
> Five findings we would put to policymakers, each addressed to a different authority.
>
> To SDAIA: publish an identifier schedule and a re-identification risk methodology, as HHS does for HIPAA.
>
> To SFDA: extend the "enhance, not replace" duty beyond device classification, keyed to clinical consequence.
>
> To SFDA again, and this is the one with the widest reach: workflow and administrative AI in hospitals — the fastest-growing category — sits outside every Saudi instrument, and no body validates its performance in any case.
>
> To the Ministry of Health and the Saudi Health Council: publish a minimum referral dataset. Response-time standards exist. A machine-checkable content standard does not. CBAHI imposes transfer-documentation requirements, but as accreditation criteria assessed by survey, not as something a system can apply.
>
> To the National Cybersecurity Authority: ECC-2 2024 was inspected across all one hundred and eight controls. It contains no AI provisions at all.

---

## 6:00 — 6:40 · What is unique, and what we do not claim

> Three things we would offer ITU as standards gaps. Y point three one seven two defines the preprocessing node with no privacy obligation attached to it. It supports multi-level pipelines but is silent on which node boundary a data-residency requirement should be enforced at — our split at the preprocessing boundary is a candidate pattern, because identifiers never cross it. And its policy node has no notion of advisory versus blocking enforcement, which scenario four shows is the distinction that decides whether human oversight is real.
>
> On limits, we are direct. Worldwide, only one of ten studies of this class of system showed any operational benefit — about eight hours a week of staff time. No study anywhere shows improved patient outcomes, so we do not claim any. Saudi referral acceptance also improved from seventy-four to ninety percent without AI. Our case is not that referral processing is failing.
>
> What is genuinely new is that no study of AI referral screening exists from the Gulf, or in Arabic, anywhere in the world literature.

---

## 6:40 — 6:50 · Close

*(Ending at 6:50 leaves margin against the 7:00 maximum. Do not fill it.)*

> The knowledge base, the code and the gap register are all in the repository, with a working link for every instrument. Thank you.

---

## If a judge adds a scenario live

They may do this — the organisers said so, and the submission template already contains their worked example about targeted advertising. The move is always the same three steps:

1. **Name the technical failure.** If targeted ads are appearing, data has leaked. Say that first.
2. **Query the knowledge base in front of them.** `python src/cli.py ask "..."` with whatever the scenario is about.
3. **Give the verdict either way.** If a binding instrument covers it, name it and cite it. If nothing does, say so and flag it as a new gap.

Never guess. "Let me check" and then actually checking is a stronger answer than a confident wrong one — and checking is the entire point of what you built.
