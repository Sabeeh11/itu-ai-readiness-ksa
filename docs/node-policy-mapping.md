# The Y.3172 Node × Policy Mapping

**Use case:** AI-assisted completeness and appropriateness screening of medical referral documents, Saudi hospital setting.

## What the system does

Primary care clinics send referral documents to specialist hospitals through the national e-referral system. Before a referral is submitted, the system reads the document and answers two questions:

1. **Is it complete?** Does it carry a provisional diagnosis, examination findings, investigation results, history and current treatment — the fields a receiving specialist needs in order to accept and act?
2. **Is it appropriate?** Does this patient need transfer to a specialist at all, or is this a case the sending facility can manage — and if transfer is warranted, is the receiving specialty the right one?

Output is a completeness score with the specific missing fields named, and an appropriateness flag routed to a human reviewer. Nothing is auto-rejected.

## Why this framing

- The Ministry of Health's own Medical Referrals Centre staff, in [Healthcare 2025;13(16):1945](https://www.mdpi.com/2227-9032/13/16/1945), recommend "integrating AI tools for referral triage to optimize patient allocation, thereby **reducing unnecessary transfers**." Appropriateness — not urgency — is what was asked for.
- [IJIRMS 2022](https://ijirms.in/index.php/ijirms/article/view/1517), analysing 1.6M referrals, recommends "assessing referral appropriateness to identify inefficiencies."
- The measured failure modes are documentary: 50% of referral letters carried no provisional diagnosis, 52% no investigation results, 45% no examination findings ([J Family Community Med 2007](https://doaj.org/article/cfee3017b738479fad3356e922afc576)).
- It avoids the counter-arguments that sink an urgency-triage pitch: acceptance rates are already improving without AI, life-saving referrals are already accepted 100% of the time, and the majority root cause is missing specialist capacity, which no triage system can create.

## The privacy design

Referral documents contain patient names, national ID / Iqama numbers, phone numbers, addresses, dates of birth and medical record numbers. A de-identification stage inside the sending facility strips these before the model reads anything. The model sees de-identified clinical text only. What leaves the facility is a case reference, a completeness score, the list of missing fields, and an appropriateness flag.

## Why it is deliberately not a medical device

The system evaluates the quality and routing of a *document*. It does not diagnose, treat, or predict disease. That places it outside SFDA MDS-G-010's scope — which is precisely where the regulatory vacuum sits. The gaps are the subject matter, not an inconvenience.

## Levels

SRC, C and PP run on-premises inside the sending facility (**Level 1**). M, P, D may run in a cloud region (**Level 2**). Only de-identified text crosses that boundary — which is what makes the Saudi data-residency rules satisfiable by architecture rather than by promise.

---

## The mapping table

| Node | What it is in our solution | Governing documents (real, linked) | Gap |
|---|---|---|---|
| **SRC**<br>Source | Referral documents drafted at primary care and secondary facilities, plus supporting EHR extracts | **IS0303 §8** — patient opt-out, access requires a treatment relationship ([link](https://nhic.gov.sa/standards/Policies/IS0303-Saudi-Health-Information-Exchange-Policies-v1.0.pdf))<br>**Law of Practicing Healthcare Professions, Art. 21** — statutory medical confidentiality ([link](https://www.moh.gov.sa/en/Ministry/Rules/Documents/Law-of-Practicing-Healthcare-Professions.pdf))<br>**PDPL Implementing Regs Art. 26** — health data controls, minimum necessary ([link](https://dgp.sdaia.gov.sa/wps/portal/pdp/knowledgecenter/details/PDPL2))<br>**MOH Ehalati referral standards** ([link](https://www.moh.gov.sa/en/Ministry/Structure/Programs/Referral/Pages/FAQ.aspx)) | **G3** — no Saudi statute on electronic health records as such. Confidentiality rests on a professional-duty article, not a records standard.<br>**G11 (new)** — no published national standard defines what a *complete* referral document must contain. The MOH page sets time standards, not content standards. Without a content standard, "completeness" has no legal referent. |
| **C**<br>Collector | On-premises intake gateway that receives drafted referrals before submission to the national system | **NHIC Telehealth Application Guidelines** — tier 3–4 infrastructure for critical cases, disaster recovery, in-Kingdom storage ([link](https://nhic.gov.sa/standards/Telehealth/Telehealth-Application-Guidelines.pdf))<br>**NDMO Data Management Standards v1.5** — data operations and quality ([link](https://dmo.ksu.edu.sa/sites/dmo.ksu.edu.sa/files/imce_images/policiesen001.pdf))<br>**NCA CCC-1:2020** — in-Kingdom processing and DR ([link](https://cdn.nca.gov.sa/ar/ccc-en.pdf)) | **G7** — the governing telehealth instrument lapsed 31 Dec 2021 with no successor; the NHIC guidelines carry no version number or date. Both are actively relied upon. |
| **PP**<br>Preprocessor | **The de-identification stage.** Strips names, national ID / Iqama, contact details, dates, MRNs. Emits de-identified clinical text | **PDPL Implementing Regs Art. 26** — minimum necessary processing, documented at all stages<br>**SDAIA Guide for Controllers/Processors** — anonymisation must remove direct *and indirect* identifiers permanently ([link](https://dgp.sdaia.gov.sa/wps/wcm/connect/f579bc32-fda8-47bd-bc6f-66b8cb77985c/ENG-Guide+to+the+saudi+PDP+law+for+controllersprocessors.pdf?MOD=AJPERES))<br>**SDAIA Destruction / Anonymization / Pseudonymization Guideline** — generalization, masking, coding ([link](https://dgp.sdaia.gov.sa/wps/portal/pdp/knowledgecenter/details/PersonalDataDestruction))<br>**IS0303 §11** — re-identification risk assessment required before release | ⚠️ **G4 — the headline gap.** Saudi law *requires* permanent anonymisation and *requires* a re-identification risk assessment, but **no instrument states how to measure either**. No identifier schedule, no k-anonymity, no ℓ-diversity, no risk threshold. Benchmark: **HIPAA Safe Harbor's 18 identifiers plus Expert Determination** ([link](https://www.hhs.gov/hipaa/for-professionals/special-topics/de-identification/index.html)). A duty with no method can be neither complied with nor audited. |
| **M**<br>Model | Completeness classifier (field presence detection) and appropriateness classifier over de-identified referral text | **SFDA MDS-G-010** — dataset composition, three-part validation evidence ([link](https://www.sfda.gov.sa/sites/default/files/2023-01/MDS-G010ML.pdf)) — *applies only if the system is a medical device*<br>**ITU FG-AI4H DEL7.4** — four-phase clinical evaluation ([link](https://www.itu.int/dms_pub/itu-t/opb/fg/T-FG-AI4H-2023-3-PDF-E.pdf))<br>**ITU FG-AI4H DEL5.5** — data handling ([link](https://www.itu.int/dms_pub/itu-t/opb/fg/T-FG-AI4H-2023-8-PDF-E.pdf))<br>**WHO Ethics and governance of AI for health** ([link](https://www.who.int/publications/i/item/9789240029200)) | ⚠️ **G1 + G5.** Document screening is not a medical device, so MDS-G010 does not bind it — and nothing else does. Separately **G5**: IS0304 certifies interoperability conformance but nothing in Saudi Arabia certifies model accuracy. No national test set, no accredited assessment body. |
| **P**<br>Policy | No referral is auto-rejected or auto-downgraded. Every appropriateness flag is advisory and routed to a named human reviewer, who may override without justification. Completeness prompts are non-blocking. Thresholds fixed, versioned and auditable | **SFDA MDS-G-010** — *"enhance users' performance, not replace them"*<br>**IS0303 §8** — break-glass emergency access permitted with audit trail and review<br>**SDAIA AI Ethics Principles** — Accountability & Responsibility, Humanity ([link](https://dgp.sdaia.gov.sa/wps/wcm/connect/4c56ed1c-1b82-447d-ac29-638f5f99c12e/ai-principles-EN.pdf?MOD=AJPERES)) — *non-binding* | ⚠️ **G2.** Outside the medical-device route there is **no Saudi obligation** for human-in-the-loop or clinician override in clinical AI. SDAIA's principles are non-binding and sector-neutral. Our system imposes this constraint on itself voluntarily; nothing requires it, and nothing would prevent a competing vendor from auto-rejecting referrals. |
| **D**<br>Distributor | Returns the completeness report to the referring clinician; forwards appropriateness flags to the receiving facility's referral coordinator | **IS0303 §3** — permitted purposes; marketing use prohibited<br>**IS0303** — feedback reporting to referring facility<br>**NDMO Interim Regulations** — data sharing sub-regulation, in-Kingdom storage ([link](https://www.mof.gov.sa/en/generalservcies/open-data/Documents/PoliciesEn.pdf))<br>**NCA CCC-1:2020** — cloud residency | **G10** — NCA ECC-2:2024, read across all 108 controls, contains no AI provisions whatsoever. An AI system handling health data inherits generic cloud controls with no AI-specific security requirement. |
| **SINK**<br>Target | The referring clinician's workstation (completeness prompts) and the receiving coordinator's queue (appropriateness flags) | **WHO guidance on large multi-modal models** ([link](https://www.who.int/publications/i/item/9789240084759)) — international only<br>**SDAIA Generative AI Guidelines for Government Entities** — non-binding | ⚠️ **G6 + G9.** Nothing in Saudi Arabia governs how an AI-derived judgement about a clinician's own documentation is communicated to that clinician, or whether AI involvement must be disclosed. **G9**: no instrument addresses Arabic dialect and vocabulary variation, or accessibility for hearing or mobility impairment, in health AI. |

---

## What this table demonstrates

Seven nodes. Every one carries at least one gap. Five are severe enough to state as findings for policymakers, each addressed to a different authority.

**1. G4 (PP) — a duty without a method.** Saudi Arabia mandates anonymisation of health data and mandates a re-identification risk assessment, without publishing how to perform either. Neither the regulated party nor the regulator can determine compliance.
*Recommendation: publish an identifier schedule and a re-identification risk methodology, as HHS does for HIPAA.*

**2. G2 (P) — no oversight duty outside the device route.** Clinical AI that is not a regulated medical device carries no human-in-the-loop obligation anywhere in Saudi law.
*Recommendation: extend an "enhance, not replace" duty beyond device classification, keyed to clinical consequence.*

**3. G1 + G5 (M) — the fastest-growing category is unregulated and unvalidated.** Workflow, administrative and non-diagnostic decision-support AI sits outside every Saudi instrument, and no body validates model performance in any case.
*Recommendation: a validation regime keyed to clinical impact rather than device classification.*

**4. G11 (SRC) — completeness has no machine-checkable referent.** No published minimum referral dataset defines what a referral document must contain. CBAHI accreditation standards impose transfer-documentation requirements, but as survey-assessed criteria rather than an applicable specification. The MOH sets time standards for referral response but not content standards for referral submission. Any completeness model must therefore derive its own criteria — which is precisely the unsourced-threshold problem the hackathon warns against.
*Recommendation: publish a minimum referral dataset, as several national health systems do.*

## Standards gaps to propose to ITU

- **Y.3172 defines the PP node without attaching any privacy obligation to it.** A companion specification for de-identification at PP — with a measurable re-identification threshold — would close G4 generically rather than nation by nation.
- **Y.3172 supports multi-level pipeline distribution but is silent on which node boundary a data-residency requirement should be enforced at.** Our Level 1 / Level 2 split at the PP boundary is a candidate pattern: identifiers never cross, so residency is satisfied structurally rather than contractually.
- **Y.3172's P node has no notion of a non-blocking advisory policy.** The standard describes policies that constrain model output before it reaches a SINK, but not the distinction between advisory and blocking enforcement — a distinction that determines whether human oversight is real.
