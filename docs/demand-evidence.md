# Evidence of Demand — Saudi Referral Processing

ITU AI Readiness Hackathon KSA 2026 · compiled 26 August 2026 · all sources fetched and verified

**Verdict: MODERATE.** Defensible, but only if framed precisely. The obvious framing ("Saudi referrals are slow, AI will speed them up") is contradicted by the data. The defensible framing is narrower and is set out at the end.

---

## 1. The system exists and is large

Saudi MOH operates a national e-referral programme, **"Ehalati" (إحالتي)**, run through the **Saudi Medical Appointments and Referrals Centre (SMARC)** / Medical Referrals Centre. Launched 2012; SMARC established 2019; unified platform inaugurated 19 May 2024 by Deputy Minister Abdulaziz Al-Rumaih, with the stated objective of reducing patient waiting lists.

- [MOH Referral Program FAQ](https://www.moh.gov.sa/en/Ministry/Structure/Programs/Referral/Pages/FAQ.aspx) — government primary source
- [SPA official announcement, 19 May 2024](https://www.spa.gov.sa/N2105612)

**Published volumes:**

| Period | Volume | Source |
|---|---|---|
| 2018–2021 | 1,607,009 referrals; **+55% growth** 2018→2021 | [IJIRMS 2022](https://ijirms.in/index.php/ijirms/article/view/1517) |
| 2020–2021 | 671,672 patients / 632,763 requests | [Frontiers Medicine 2024](https://www.frontiersin.org/journals/medicine/articles/10.3389/fmed.2024.1348442/full) |
| 2023–2024 | **755,145 e-referrals**, +19.34% vs 2020–21 | [Healthcare 2025](https://www.mdpi.com/2227-9032/13/16/1945) |

⚠️ **Service-level standards are inconsistent between sources.** The MOH FAQ gives emergency = max 24h, routine inpatient = 3 days, routine outpatient = 7 days. Healthcare (MDPI) 2025 gives emergency = 72h, routine inpatient = 2 weeks, routine outpatient = 4 weeks. Cite both and note the discrepancy, or cite MOH only and label it as such. Do not present one as settled.

---

## 2. ⭐ The load-bearing citation

**Aljerian NA, et al. "Saudi Medical Appointments and Referrals Center (SMARC) Performance Dynamic: A Comparative National Analysis of 2023–2024 Against Baseline Metrics." *Healthcare* 2025;13(16):1945.** DOI 10.3390/healthcare13161945 — https://www.mdpi.com/2227-9032/13/16/1945

Direct quote from the recommendations:

> "Strategic recommendations for system enhancement include expanding specialized workforce distribution across regions and **integrating AI tools for referral triage to optimize patient allocation, thereby reducing unnecessary transfers**."

**Why this is the strongest evidence available:** eight of the twelve authors are affiliated with the **Medical Referrals Centre, Ministry of Health** — the body that actually operates SMARC — including Nawfal A. Aljerian and Mohammed K. Alabdulaali. This is not an outside academic speculating. It is the operator of the national referral system, in a peer-reviewed journal, asking for AI referral triage.

The same paper confirms **triage today is manual**: non-accepted cases "are reviewed by SMARC medical referrals management for triaging and securing an appropriate receiving hospital"; life-saving cases are "comprehensively reviewed by an on-call consultant."

---

## 3. Problems that hold up

**Regional inequity — persistent across both study periods, the most durable problem statement:**

- 2020–21 acceptance: Eastern 83.70% vs **Riyadh lowest at 68.01%**
- 2023–24 by business unit: Eastern 95.65% vs **Central 85.43%**
- The gap survived a system-wide 16-point improvement

**Root cause of referral (convergent across three independent analyses):**

| Study | "Unavailable subspecialty/physician" as cause |
|---|---|
| Frontiers Medicine 2024 | 61.38% |
| IJIRMS 2022 | 55.8% (897,461 cases) |
| Cureus 2024 (emergency) | ~70% |

**Referral letter quality — real but stale (2007, n=330, Buraidah):** provisional diagnosis absent 50% · investigation results missing 52% · clinical examination absent 45% · treatment info absent 47% · history missing 36% · legible only 75% · **feedback report returned to PHC only 30%**. [J Family Community Med 2007](https://doaj.org/article/cfee3017b738479fad3356e922afc576)

No post-2015 Saudi study measuring referral letter completeness was found. State this openly — a referee will ask whether structured e-referral forms have since fixed it.

**Delays:** [Frontiers Health Services 2026 systematic review](https://www.frontiersin.org/journals/health-services/articles/10.3389/frhs.2025.1701062/full) (28 studies) finds "referral delays were common barriers." [Cureus 2026, KFSHRC Madinah](https://assets.cureus.com/uploads/original_article/pdf/475076/20260627-34763-rkycty.pdf) reduced ED-to-inpatient admission cycle 390 → 175 minutes; "delay in receiving unit" 42% of causes.

---

## 4. Counter-evidence — must be acknowledged in the report

1. **The system is fixing itself without AI.** Acceptance rose 74.13% → **90.19%** in three years. Rejection is now 9.81%, not the 25.87% of 2020–21.
2. **The highest-acuity tier is already at ceiling.** Life-saving referrals: **100% acceptance** in both periods. AI cannot improve the cases that matter most.
3. **The dominant problem is supply, not sorting.** 55–70% of referrals stem from missing specialist capacity. Triage cannot manufacture a subspecialist. The MOH-authored paper lists workforce distribution *first* and AI triage *second*.
4. **Real-time bed visibility already exists** in the May 2024 unified platform.
5. **No Vision 2030 numeric target.** All four HSTP documents were fetched and contain **no published KPI** for referral waiting time or processing time. Verified targets are life expectancy 74→80, 4 PHC visits/person/year, road deaths, health-security supplies. Do not claim you are closing a stated national target.
6. **The referral-quality premise is 19 years old** and predates e-referral.
7. **Saudi PHC waiting times are within benchmark** — median 23 minutes against a 20–30 min standard, n=9,211. [Springer 2023](https://link.springer.com/article/10.1007/s44229-023-00032-3). Undercuts any generic "patients wait too long" framing.

---

## 5. The global evidence ceiling — be honest about this

[Frontiers in Health Services 2026 systematic review](https://www.frontiersin.org/journals/health-services/articles/10.3389/frhs.2026.1797583/full) of NLP for outpatient referral triage:

- **Only 10 studies** worldwide met inclusion
- Countries: Netherlands, Chile, Canada, UK, Ireland, USA, Australia. **Zero from the Middle East, Gulf, or in Arabic**
- Performance: **AUC 0.83–0.96, F1 up to 0.91**
- **Only 1 of 10 showed operational benefit** — ~8 hours/week of referral assessment time saved
- Only 2 of 10 included prospective testing

**Best primary study:** [npj Digital Medicine 2025](https://www.nature.com/articles/s41746-025-01495-4) — 8,044 referral letters, 12 Dutch rheumatology clinics, external replication cohort of 831. **45.9% of rheumatoid arthritis cases surfaced in the top 5% of prioritised letters vs 13.1% under the existing waiting-time system (P<0.001).** The single most quotable efficacy figure available.

**No study anywhere has shown AI referral triage improves time-to-treatment or clinical outcomes.** Claim clinician time saved and better within-queue ranking. Do not claim outcomes.

**Supporting the de-identification stage:** [Automated De-Identification of Arabic Medical Records, ArabicNLP/ACL 2023](https://aclanthology.org/2023.arabicnlp-1.4/) — 17 sensitive entity types, **0.94–0.98 micro F1**, "in line with that achieved with manual de-identification by domain experts." Caveat: corpus is machine-translated i2b2, not native Arabic clinical text.

---

## 6. No AI referral triage exists in Saudi Arabia

- **Seha Virtual Hospital** (launched Feb 2022; 170+ hospitals, 480,000 annual capacity) — the [JMIR 2026 policy analysis](https://www.jmir.org/2026/1/e89276/PDF) describes **no AI use for triage, routing, or clinical text**.
- AI at SVH is **imaging, not text** — Deputy Minister Abdullah Al-Issa cites AI-driven X-ray and breast cancer detection. [Arab News, Feb 2025](https://www.arabnews.com/node/2589699/business-economy)
- [Systematic review of AI in Saudi healthcare](https://www.mdpi.com/2071-1050/18/2/905) (24 studies included) flags **minimal Arabic language processing capability** as a barrier.

**This is white space, and the operator has publicly asked for it.**

---

## 7. ⚠️ Do not use

- **Insurance claim denial rates / NPHIES figures** ("25% denials", "SAR 3bn annually") — every source traces to vendor marketing. No government statistic or peer-reviewed study exists.
- **"65% of Saudi ED visits are non-urgent"** — appears second-hand inside a systematic review; primary source not verified.

---

## 8. Recommended framing

**Do not pitch:** "Saudi referrals are slow, AI decides urgency faster." The data contradicts the premise.

**Pitch instead — and this is the recommended pivot:**

> **Automated completeness and appropriateness screening of referral documents at submission**, rather than urgency triage.

Why this framing is stronger:

- It matches the MOH-authored recommendation **verbatim** — "reducing unnecessary transfers" is *appropriateness*, not urgency.
- IJIRMS 2022, on 1.6M referrals, concludes the 55% growth is "potentially inflicting harm on the sustainability of high-quality health systems" and explicitly recommends "**assessing referral appropriateness to identify inefficiencies**."
- The 2007 completeness failure modes (50% no diagnosis, 52% no investigations, 30% feedback return) are exactly what a document-completeness classifier targets — and **if the problem has since been fixed, measuring that is itself a valid result**.
- It is unambiguously a document/text task, so the de-identification stage is load-bearing rather than decorative.
- It sidesteps every counter-argument above: it does not compete with the improving acceptance rate, does not touch the 100%-accepted life-saving tier, and does not claim to create specialist capacity.

The claim set becomes: clinician and coordinator time saved · better within-queue ranking · reduction in avoidable back-and-forth · **and an Arabic/Gulf evidence gap that no study in the world literature has addressed.**
