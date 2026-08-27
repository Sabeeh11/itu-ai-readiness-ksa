# Research Long-List — AI in Healthcare Policy Corpus (Saudi Arabia + International)

> **This is the research long-list, not the indexed corpus.** It records everything the
> literature search surfaced, including instruments that were considered and not indexed.
> The 29 instruments the analyser actually reads are in `data/corpus.json`, and the
> authoritative gap register with its G-numbering is `output/gap_report.json`.
> One item below — G8, the National Strategy for Data & AI not being publicly
> downloadable — is an observation about document availability rather than a governance
> gap at any pipeline node, so it is deliberately absent from the register. G11 was
> identified later and appears in the register but not in the table below.

ITU AI Readiness Hackathon KSA 2026 · health domain · compiled 26 August 2026

All documents below are **real, publicly available, and link-verified** unless marked otherwise. Two hosts resist automated access: `sdaia.gov.sa` blocks scrapers (use the `dgp.sdaia.gov.sa` sub-portal or the mirrors noted), and `nhic.gov.sa` intermittently robots-blocks (MOH mirrors given where needed).

Pipeline tags: **DATA** (sources/collection) · **INFRA** (edge/cloud reliability) · **PREP** (preprocessing/de-identification) · **VAL** (model validation/benchmarking) · **HITL** (human-in-the-loop/override) · **DIST** (distribution of outputs) · **UX** (end-user delivery) · **RESID** (data residency/sovereignty)

---

## 1. Saudi Arabia — National Level

| # | Document | Issuer / Date | Link | Pipeline |
|---|---|---|---|---|
| 1.1 | **AI Ethics Principles** v1.0 — 7 principles across a 4-stage AI lifecycle; 4 risk tiers incl. prohibited | SDAIA, Sept 2023 | [PDF](https://dgp.sdaia.gov.sa/wps/wcm/connect/4c56ed1c-1b82-447d-ac29-638f5f99c12e/ai-principles-EN.pdf?MOD=AJPERES) | DATA, PREP, VAL, HITL, DIST |
| 1.2 | AI Ethics Principles, 2025 edition | SDAIA, 2025 | [link](https://sdaia.gov.sa/en/SDAIA/about/Documents/ai-principles.pdf) *(partially verified — WAF)* | as above |
| 1.3 | AI Adoption Framework | SDAIA, 2024/25 | [link](https://sdaia.gov.sa/en/SDAIA/about/Files/AIAdoptionFramework.pdf) *(partially verified)* | DATA, VAL, HITL |
| 1.4 | Generative AI Guidelines for Government Entities | SDAIA, Jan 2024 / 2025 ed. | [link](https://sdaia.gov.sa/en/SDAIA/about/Files/GenAIGuidelinesForGovernmentENCompressed.pdf) *(partially verified)* | DATA, HITL, DIST, UX |
| 1.5 | Generative AI Guidelines for the Public | SDAIA, 2024/25 | [link](https://sdaia.gov.sa/en/SDAIA/about/Files/GenerativeAIPublicEN.pdf) *(partially verified)* | DIST, UX |
| 1.6 | **Personal Data Protection Law (PDPL)** — health data explicitly sensitive | Royal Decree M/19 (2021), amended M/148 (2023) | [full text](https://dgp.sdaia.gov.sa/wps/portal/pdp/knowledgecenter/details/PDPL) | DATA, PREP, RESID |
| 1.7 | **PDPL Implementing Regulations — Article 26 is health-specific**: requires MOH-issued controls, segregated access hierarchies, documentation of *all* processing stages, and **minimum necessary processing** | SDAIA, in force Sept 2023, enforced Sept 2024 | [full text](https://dgp.sdaia.gov.sa/wps/portal/pdp/knowledgecenter/details/PDPL2) | DATA, PREP, HITL, RESID |
| 1.8 | Regulation on Personal Data Transfer Outside the Kingdom | SDAIA, 2023 amd. 2024 | [link](https://dgp.sdaia.gov.sa/wps/portal/pdp/knowledgecenter/details/RegulationonPersonalDataTransferOutsidetheKingdom) | RESID, INFRA |
| 1.9 | **Guide to the PDPL for Controllers and Processors** — anonymisation must remove direct *and indirect* identifiers permanently; the anonymisation process itself stays in scope; health data barred from marketing even with consent | SDAIA, v1.0 Dec 2023 | [PDF](https://dgp.sdaia.gov.sa/wps/wcm/connect/f579bc32-fda8-47bd-bc6f-66b8cb77985c/ENG-Guide+to+the+saudi+PDP+law+for+controllersprocessors.pdf?MOD=AJPERES) | PREP, DATA, RESID |
| 1.10 | **Guideline for Personal Data Destruction, Anonymization and Pseudonymization** (Arabic only) — names generalization, aggregation, masking, encryption, coding. **No k-anonymity, no risk methodology** → see G4 | SDAIA | [full text](https://dgp.sdaia.gov.sa/wps/portal/pdp/knowledgecenter/details/PersonalDataDestruction) | PREP |
| 1.11 | **National Data Governance Interim Regulations** — 4 classification levels; *"personal data shall be stored and processed within the Kingdom's territory"* | NDMO/SDAIA, v1 June 2020 | [PDF (MoF mirror)](https://www.mof.gov.sa/en/generalservcies/open-data/Documents/PoliciesEn.pdf) | DATA, PREP, RESID, DIST |
| 1.12 | **Data Management and Personal Data Protection Standards** — 15 domains incl. Data Quality, Data Sharing & Interoperability, Data Classification | NDMO, v1.5 Jan 2021 | [PDF (KSU mirror)](https://dmo.ksu.edu.sa/sites/dmo.ksu.edu.sa/files/imce_images/policiesen001.pdf) | DATA, PREP, INFRA, DIST |
| 1.13 | Health Sector Transformation Program Delivery Plan — commits to AI decision support, unified EHR, national health database | Vision 2030 HSTP, Sept 2021 | [PDF](https://www.vision2030.gov.sa/media/0wop2tds/hstp_eng.pdf) | DATA, UX (strategy) |
| 1.14 | National Strategy for Data & AI (NSDAI) | SDAIA, 2020 | [landing](https://sdaia.gov.sa/en/SDAIA/SdaiaStrategies/Pages/NationalStrategyForDataAndAI.aspx) — **no downloadable full text, see G8** | — |

## 2. Saudi Arabia — Health Sector Specific

| # | Document | Issuer / Date | Link | Pipeline |
|---|---|---|---|---|
| 2.1 | ⭐ **Guidance on AI/ML Technologies Based Medical Devices** (MDS-G-010) — prevalence-matched normal/abnormal dataset ratios; multi-centre sourcing; demographic alignment; **test sets must not be public**; 3-part evidence (clinical association + analytical + clinical validation); *"enhance users' performance, not replace them"*; post-market performance monitoring | SFDA, v1.0, 29 Nov 2022 | [PDF](https://www.sfda.gov.sa/sites/default/files/2023-01/MDS-G010ML.pdf) | DATA, PREP, VAL, HITL, UX |
| 2.2 | **Guidance on Digital Health Products** (MDS-G-027) — 8 categories incl. SaMD, mHealth, telemedicine, wearables, AI/ML; decision pathway for what counts as a regulated device | SFDA, v1.0, 11 Aug 2025 | [PDF](https://www.sfda.gov.sa/sites/default/files/2025-08/MDS-G027.pdf) | DATA, UX, DIST |
| 2.3 | Guidance on Software as a Medical Device (MDS-G23) — adopts IMDRF N10/N12/N23 as *considerations*, not requirements | SFDA, v1.0, 9 Apr 2018 | [PDF](https://www.sfda.gov.sa/sites/default/files/2020-03/MDS_G23.pdf) | VAL, INFRA |
| 2.4 | Pre-Market Cybersecurity of Medical Devices (MDS-G38) — ISO 14971 alignment | SFDA, 18 Jun 2019 | [PDF](https://sfda.gov.sa/sites/default/files/2019-10/MDS-G38.pdf) | INFRA, DATA |
| 2.5 | Post-Market Cybersecurity of Medical Devices (MDS-G37) — NIST CSF lifecycle | SFDA, 18 Jun 2019 | [PDF](https://www.sfda.gov.sa/sites/default/files/2019-10/MDS-G37.pdf) | INFRA, DIST |
| 2.6 | ⭐ **Saudi Health Information Exchange Policies** (IS0303) — §8 patient opt-out, treatment-relationship access, **break-glass emergency access with audit trail**; §3 marketing use prohibited; §11 **de-identified release requires ethics committee approval + re-identification risk assessment + data use agreement** | SHC/NHIC, v1.0, 21 Apr 2016 | [PDF](https://nhic.gov.sa/standards/Policies/IS0303-Saudi-Health-Information-Exchange-Policies-v1.0.pdf) · [MOH mirror](https://www.moh.gov.sa/en/Ministry/ehealthstd/Documents/eHealth%20Standards%20Files/Policies/IS0303%20Saudi%20Health%20Information%20Exchange%20Policies%20v1.0.pdf) | DATA, PREP, HITL, DIST |
| 2.7 | Saudi HIE Testing and Certification Policies (IS0304) — ISO/IEC 17025 labs + 17065 certification, 4-year conformity certificates. **Interoperability conformance only, not model accuracy** → G5 | MOH SCMO, v1.0, 22 Feb 2015 | [PDF](https://www.moh.gov.sa/en/Ministry/ehealthstd/Documents/eHealth%20Standards%20Files/Policies/IS0304%20Saudi%20Health%20Information%20Exchange%20Testing%20and%20Certification%20Policies%20v1.0.pdf) | VAL (conformance), INFRA |
| 2.8 | ⭐ **Telehealth Application Guidelines** — *"data storage should be hosted within Saudi Arabia's geographical boundaries"*; **tier 3–4 infrastructure for critical cases**; disaster recovery; RBAC; covers AI and blockchain as emerging tech | NHIC/SHC, undated | [PDF](https://nhic.gov.sa/standards/Telehealth/Telehealth-Application-Guidelines.pdf) | INFRA, RESID, DATA, UX, DIST |
| 2.9 | Governing Rules of Telehealth (Executive + Establishing Rules) | NHIC/SHC | [executive](https://nhic.gov.sa/standards/Telehealth/the-governing-rules-of-telehealth-english-executive-rules.pdf) · [establishing](https://nhic.gov.sa/standards/Telehealth/the-governing-rules-of-telehealth-english-establishing-rules.pdf) *(partially verified)* | HITL, UX |
| 2.10 | Legal Regulations for Telehealth Services — ⚠️ **states validity through 31 Dec 2021, no successor found** → G7 | MOH DHCOE, Royal Order 47455 | [PDF](https://www.moh.gov.sa/en/Ministry/Rules/Documents/Legal-Regulations-for-Telehealth-Services.pdf) | HITL, UX, DATA |
| 2.11 | ⭐ **Law of Practicing Healthcare Professions — Article 21**: statutory medical confidentiality, with closed exceptions (criminal death reporting, epidemic reporting, competence defence, **written patient consent**, judicial order). Article 18: duty to explain treatment | Royal Decree M/59 | [PDF](https://www.moh.gov.sa/en/Ministry/Rules/Documents/Law-of-Practicing-Healthcare-Professions.pdf) | DATA, DIST, HITL |
| 2.12 | Implementing Regulations of the Health Law — **verified to contain nothing on medical records or data confidentiality** → evidence for G3 | MOH, 29 Aug 2003 | [PDF](https://www.moh.gov.sa/en/Ministry/Rules/Documents/002.pdf) | — |
| 2.13 | ⭐ **Cloud Cybersecurity Controls (CCC-1:2020)** — CSPs must provide services *"from within the KSA, including systems used for storage, processing, and disaster recovery centers"* | NCA, ed. 1, 2020 | [PDF](https://cdn.nca.gov.sa/ar/ccc-en.pdf) | INFRA, RESID |
| 2.14 | Essential Cybersecurity Controls (ECC-2:2024) — 108 main controls. **Verified to contain nothing on AI** → G10. Localisation moved out to NDMO | NCA, v2, 2024 | [PDF](https://cdn.nca.gov.sa/api/files/public/upload/86e09090-44e4-481f-bc28-355673607654_ECC--2024-EN.pdf) | INFRA, RESID |
| 2.15 | Cloud Computing Service Provisioning Regulations v4 | CST, Decision 506/1445, Oct 2023 | [decision page](https://www.cst.gov.sa/en/regulations-and-licenses/decisions/Regulation-1482) | INFRA, RESID |
| 2.16 | Guidelines for IoT (non-binding) — device verification, input data validation, retention aligned to KSA rules | CST, 1st ed. July 2023 | [PDF](https://www.cst.gov.sa/-/media/cst-website-app/data/media/files/Guidelines_for_IoT_en) | DATA, INFRA, PREP |

## 3. International / Reference

| # | Document | Issuer / Date | Link | Pipeline |
|---|---|---|---|---|
| 3.1 | ⭐ **Ethics and governance of AI for health** — 6 consensus principles | WHO, 28 Jun 2021 | [landing + PDF](https://www.who.int/publications/i/item/9789240029200) | DATA, VAL, HITL, DIST, UX |
| 3.2 | ⭐ **Guidance on large multi-modal models** — the citable authority for any LLM component | WHO, 18 Jan 2024 | [landing + PDF](https://www.who.int/publications/i/item/9789240084759) | DATA, VAL, HITL, DIST, UX |
| 3.3 | Global strategy on digital health 2020–2027 | WHO, ext. ed. Dec 2025 | [landing](https://www.who.int/publications/i/item/9789240116870) | INFRA, DATA |
| 3.4 | FG-AI4H publication catalogue (~36 deliverables) | ITU/WHO | [catalogue](https://www.itu.int/pub/T-FG-AI4H) | — |
| 3.5 | FG-AI4H DEL0 — overview and index of DEL1–DEL10.24 | ITU-T, Sept 2023 | [PDF](https://www.itu.int/dms_pub/itu-t/opb/fg/T-FG-AI4H-2023-10-PDF-E.pdf) | — |
| 3.6 | ⭐ **DEL7.4 Clinical evaluation of AI for health** — 4 phases: model design → algorithmic validation → clinical validation → deployment monitoring with algorithmic audits | ITU-T, Mar 2023 | [PDF](https://www.itu.int/dms_pub/itu-t/opb/fg/T-FG-AI4H-2023-3-PDF-E.pdf) | VAL, HITL, INFRA, UX |
| 3.7 | **DEL5.5 Data handling** — lifecycle governance, encryption in transit/at rest, RBAC, undisclosed test data stays undisclosed, audit logging | ITU-T, Mar 2023 | [PDF](https://www.itu.int/dms_pub/itu-t/opb/fg/T-FG-AI4H-2023-8-PDF-E.pdf) | DATA, PREP, INFRA, VAL |
| 3.8 | ⭐ **HIPAA De-identification Guidance** — Expert Determination + Safe Harbor 18-identifier list. Use as the benchmark against which G4 is measured | HHS OCR, 2012, upd. Feb 2025 | [page](https://www.hhs.gov/hipaa/for-professionals/special-topics/de-identification/index.html) | PREP |

Worth pulling next: FG-AI4H **DEL5.4** (training and test data specification) and **DEL2.2** (good practices for manufacturers and regulators).

---

## 4. Confirmed Gaps

Each was searched from multiple angles and found absent. **These are the findings the submission is built on** — every one maps to an empty cell in the Y.3172 node table.

| # | Gap | Node affected |
|---|---|---|
| **G1** | **No Saudi health-sector AI governance policy.** SFDA MDS-G010 reaches only AI that qualifies as a *regulated medical device*. A hospital-deployed triage LLM, an administrative AI, or non-device clinical decision support falls outside it and outside everything else. MOH, SHC and NHIC have issued nothing. | whole pipeline |
| **G2** | **No general human-in-the-loop or clinician-override obligation** outside the device route. MDS-G010's "enhance, not replace" and IS0303's break-glass audit are the only hooks; SDAIA's principles are non-binding and sector-neutral. | **P** |
| **G3** | **No Saudi statutory instrument on electronic health records.** Confidentiality rests on Art. 21 of a professional-duty law and PDPL Art. 26. The Health Law Implementing Regulations contain nothing — verified by inspection. | **SRC** |
| **G4** | **No Saudi health de-identification standard with a quantitative methodology.** No k-anonymity, no ℓ-diversity, no hashing spec, no Safe Harbor equivalent. IS0303 §11 requires a re-identification risk assessment but **does not say how to conduct one**. | **PP** |
| **G5** | **No Saudi benchmarking or independent validation regime for health-AI model performance.** IS0304 certifies interoperability conformance only. No national test set, no accredited AI-performance assessment body. | **M** |
| **G6** | **No governance of AI output distribution to patients** — no disclosure requirement that AI was involved, nothing on patient-facing generative health content. | **D / SINK** |
| **G7** | **Currency gap in telehealth regulation** — MOH regulations lapsed 31 Dec 2021 with no successor; NHIC guidelines carry no version or date. Both actively cited. | **C / INFRA** |
| **G8** | **NSDAI full text is not publicly downloadable** — transparency/accessibility gap. | strategy |
| **G9** | **Nothing on Arabic dialect variation or accessibility in health AI** — no governing document on vocabulary variation across Arabic-speaking populations, or on hearing/mobility impairment in health AI. Directly serves the AI-for-Inclusion dimension the organisers said submissions are under-serving. | **SINK / UX** |
| **G10** | **AI is absent from the national cybersecurity baseline.** ECC-2:2024 verified across all 108 controls — no AI content. Neither does CCC-1:2020. Health AI inherits generic cloud controls with no AI-specific security requirement. | **INFRA** |

## 5. Notes for building the RAG store

- **Fetching:** `sdaia.gov.sa` blocks scrapers — use `dgp.sdaia.gov.sa`, the MoF and KSU mirrors for NDMO, and MOH mirrors for NHIC. `sfda.gov.sa`, `cdn.nca.gov.sa`, `cst.gov.sa`, `vision2030.gov.sa`, `who.int`, `itu.int` all serve reliably.
- **Language:** the SDAIA anonymisation guideline and PDPL Executive Regulations are Arabic-only. Hackathon rules permit Arabic sources with English explanation — and the absence of an English de-identification guide is itself a finding.
- **Strongest node coverage:** MDS-G010 (M) · IS0303 (SRC + D) · NHIC Telehealth Guidelines (C + INFRA + RESID) · NCA CCC-1 (cloud) · PDPL Implementing Regs Art. 26 (PP).
- **Weakest:** validation (G5), override (G2), output distribution (G6) — three empty cells landing cleanly on **M**, **P** and **SINK**.
- **Threshold-backing rule:** organisers require every criterion or threshold to trace to a real document. MDS-G010 supplies dataset-composition criteria; DEL7.4 supplies the validation-phase structure. Anything past those two must be cited internationally or declared a gap.
