# Referral Screening Governance Gap Analyser

**ITU AI Readiness Hackathon — Kingdom of Saudi Arabia, 2026 · Health domain**

A knowledge-base application that maps an AI system onto the **ITU-T Y.3172** machine learning pipeline, checks each node against a corpus of real Saudi and international health-AI policy instruments, and reports where governance is absent, out of scope, or lacking a method.

---

## The use case

**AI-assisted completeness and appropriateness screening of medical referral documents.**

Before a referral is submitted through the national e-referral system, the tool reads the document and answers two questions:

1. **Is it complete?** Does it carry a provisional diagnosis, examination findings, investigation results, history and current treatment?
2. **Is it appropriate?** Does this patient need specialist transfer at all, and to the right specialty?

Referral documents contain names, national ID numbers, contact details and dates. A **de-identification stage runs inside the sending facility** before the model reads anything. Only de-identified text crosses the facility boundary.

### Why this use case

The Ministry of Health's own Medical Referrals Centre staff — eight of the twelve authors of [Healthcare 2025;13(16):1945](https://www.mdpi.com/2227-9032/13/16/1945) — recommend "integrating AI tools for referral triage to optimize patient allocation, thereby **reducing unnecessary transfers**." Saudi Arabia processed **755,145 e-referrals in 2023–24**, and triage today is manual.

It is deliberately **not a medical device**: it evaluates a document, it does not diagnose. That places it outside SFDA MDS-G-010's scope — which is exactly where the regulatory vacuum sits.

---

## What the software does

The knowledge base holds **29 real policy instruments** — Saudi national law and regulation, Saudi health-sector standards, and international guidance from WHO and ITU. Every one carries its issuer, binding status, node tags, and a working URL.

For each of the seven Y.3172 nodes, the analyser tests whether the governance concerns arising at that node are covered by a **binding, in-scope** instrument, and classifies what it finds:

| Classification | Meaning |
|---|---|
| **METHOD GAP** | An obligation exists — possibly binding and in scope — but no published method allows compliance to be demonstrated or audited. Tested *before* coverage, because a method gap is precisely the case where the duty does bind. |
| **SCOPE GAP** | A relevant binding instrument exists but its own stated scope excludes systems like this one |
| **POLICY GAP** | No binding instrument addresses the concern at all |
| **CURRENCY GAP** | The governing instrument has lapsed or carries no date |

The **scope gap** category is the one that matters most. A reader skimming the corpus will conclude that Saudi Arabia regulates health AI, because SFDA MDS-G-010 exists and is detailed and good. It simply does not apply to most of the AI actually being deployed in hospitals.

### Current result

**17 of 35 concerns** are governed by a binding, in-scope instrument. One further concern is governed by a duty for which **no method of compliance is published** — reported as `DUTY ONLY`, and the substance of the headline finding. **22 gaps** in the register: 20 at concern level, plus two corpus-level findings (G1, G3) and two instrument-currency findings that do not belong to any single node.

The shape matters more than the number. SRC and C are almost entirely covered — Saudi Arabia governs data collection, medical confidentiality, residency and infrastructure with real binding law. M is entirely uncovered and SINK almost entirely so. The finding is not that Saudi Arabia lacks AI rules; it is that **the rules stop exactly where the AI starts**.

---

## Running it

### Prerequisites

- **Python 3.10+** (3.11 or 3.12 recommended)
- No API keys, cloud accounts, or network access required at query time

### Web server (recommended for judges)

From the repository root:

```bash
# 1. Create a virtual environment (optional but recommended)
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the demo server
python3 src/demo_server.py
```

The server prints:

```
Saudi Health AI Readiness Assessor
Open http://localhost:8080
```

Open **http://localhost:8080** in your browser. The server binds to `127.0.0.1:8080` and serves the static UI plus JSON APIs from the local corpus.

**What you will see**

- A **5-step guided journey**: what this tool is → configure the referral workflow → results with Y.3172 coverage → proof on a synthetic referral → authority-specific recommendations
- **Start demo tour** in the header for presenter copy
- **Knowledge base** in the header for all 29 policy instruments, evidence, corpus search, scenarios, and the full pipeline matrix

Press `Ctrl+C` in the terminal to stop the server.

No API keys, no network at query time, no LLM.

### Command-line tools

```bash
pip install -r requirements.txt

python3 src/fetch_corpus.py          # download the corpus (see note below)
python3 src/cli.py coverage          # node-by-node coverage matrix
python3 src/cli.py gaps              # the gap register with recommendations
python3 src/cli.py scenarios         # list evaluation scenarios
python3 src/cli.py run S2            # run one scenario against the knowledge base
python3 src/cli.py ask "re-identification risk assessment"

python3 src/referral_demo.py         # the argument, on a document
python3 src/referral_demo.py 1       # one referral, in full
python3 src/selftest.py              # checks: nothing crashes, figures match the report
```

### The referral demo

`referral_demo.py` runs a synthetic referral through the PP node and shows what survives. It removes every direct identifier — national ID, phone, MRN, registration number, dates, names — and then reads what is left.

Three of the four samples still carry phrases that identify the patient: *"brother of the mayor of Al-Quwayiyah"*, *"the only dialysis technician at the Al-Lith unit"*, *"father works at the crossing"*. The fourth carries none, so the flagging is discriminating rather than indiscriminate.

The de-identification stage does not fail. It removes everything expressible as a rule. What defeats it is a sentence a clinician wrote to explain themselves — and no rule reaches that.

Whether those documents are lawfully anonymised is the question G4 says nobody can answer. All patient data is synthetic; identifiers use a reserved block that cannot collide with real Saudi National ID numbers.

**On fetching.** `fetch_corpus.py` downloads the real PDFs. Several Saudi government hosts block automated access (SDAIA's main site runs a WAF; NHIC robots-blocks intermittently), and some corporate or sandboxed networks block them all. Where a document cannot be fetched, the system falls back to a **curated extract** in `data/extracts/` containing that instrument's verified operative provisions, clearly labelled as an extract with its source URL. Provenance for every document is recorded in `data/manifest.json`, because for an audit it matters which text was read live and which was summarised.

### How coverage is decided, and why not by search

Whether an instrument governs a given concern is a **curated legal judgement**, recorded per document in the `governs` field of `data/corpus.json`. Retrieval supplies the supporting passage and its citation. It does not decide the question.

This was not the original design. Coverage was first inferred from retrieval score alone, which worked acceptably against short summaries and broke as soon as the real full-text instruments were indexed: a decisive sentence inside a 190,000-character PDF no longer outranks topically adjacent noise. It failed in both directions — missing Article 21 of the Law of Practicing Healthcare Professions on medical confidentiality, and simultaneously crediting IS0303 with supplying a de-identification method it does not contain, which would have quietly destroyed the central finding.

Making the judgement explicit is the stronger position. It sits in a data file any reviewer can open and contest, line by line. A similarity threshold cannot be argued with.

The same applies to gap *classification*. Whether an on-point instrument is scope-limited is read from the corpus, not from what retrieval happened to surface — an earlier version derived it from the top-k hits and misclassified two M-node findings as policy gaps purely because one instrument had no extract file to match against.

Retrieval itself is Term Frequency-Inverse Document Frequency (TF-IDF): no API key, no network at query time, no stochastic component. The same query returns the same citations on any machine. Concerns are searched using descriptive phrasings held in `corpus.json` rather than bare slugs — searching `human_oversight` misses the instrument that says *"enhance users' performance, not replace them"*, which is precisely the wording that matters.

---

## Evaluation scenarios

| | Scenario | Kind |
|---|---|---|
| **S1** | Baseline deployment | operational |
| **S2** | The re-identification that nobody can adjudicate | controversy |
| **S3** | Automating an existing inequity | controversy |
| **S4** | The competitor who does not ask | judge curveball |
| **S5** | The referral that was complete by whose standard? | controversy |

**S2** is the headline. A referral's free text reads *"patient is the brother of the mayor of [a town of 4,000]"*. Every direct identifier is stripped. Was the text lawfully anonymised? SDAIA requires removal of direct **and indirect** identifiers "in a way that permanently makes it impossible to identify the Data Subject"; IS0303 requires a re-identification risk assessment. Neither publishes an identifier schedule, a risk threshold, or a method. **The operator cannot demonstrate compliance and the regulator cannot audit it.**

**S4** asks whether a competitor may auto-reject referrals with no human review, no published threshold and no disclosure. The answer is yes — nothing prohibits any of it. Good practice in Saudi health AI is currently optional.

---

## Headline findings for policymakers

**G4 — a duty without a method (PP node).** Saudi Arabia mandates permanent anonymisation of health data and mandates a re-identification risk assessment, while publishing neither an identifier schedule nor a risk methodology. *Recommendation: publish both, as HHS does for HIPAA.*

**G2 — no oversight duty outside the device route (P node).** Clinical AI that is not a regulated medical device carries no human-in-the-loop obligation anywhere in Saudi law. *Recommendation: extend an "enhance, not replace" duty keyed to clinical consequence rather than device classification.*

**G1 + G5 — the fastest-growing category is unregulated and unvalidated (M node).** Workflow, administrative and non-diagnostic decision-support AI sits outside every Saudi instrument, and no body validates model performance in any case. *Recommendation: a validation regime keyed to clinical impact.*

**G11 — completeness has no machine-checkable referent (SRC node).** MOH publishes referral *response-time* standards through Ehalati but no published minimum referral dataset. CBAHI accreditation standards do impose patient-transfer documentation requirements — but as criteria assessed by periodic survey, not as a specification a system can apply. *Recommendation: publish a minimum referral dataset.*

**G10 — AI is absent from the national cybersecurity baseline (D node).** NCA ECC-2:2024 was inspected across all 108 controls and contains no AI provisions.

## Standards gaps to propose to ITU

- **Y.3172 defines the PP node with no privacy obligation attached.** A companion specification for de-identification at PP, with a measurable re-identification threshold, would close G4 generically rather than nation by nation.
- **Y.3172 supports multi-level distribution but is silent on which node boundary a data-residency requirement should be enforced at.** The Level 1 / Level 2 split at the PP boundary is a candidate pattern: identifiers never cross, so residency is satisfied structurally rather than contractually.
- **Y.3172's P node has no notion of advisory versus blocking enforcement** — a distinction that determines whether human oversight is real.

---

## Layout

```
data/corpus.json       29 instruments: issuer, binding status, node tags, URLs,
                       governs[] (which concerns each instrument actually
                       governs), known gaps, search phrasings
data/assessment_rules.json  form fields, presets, concern activation rules
data/extracts/         curated extracts for documents that cannot be fetched
data/scenarios.json    the five evaluation scenarios
web/                   browser demo (index.html, styles.css, app.js)
src/demo_server.py     Flask API + static file server
src/assessor.py        deterministic governance-readiness assessment
src/fetch_corpus.py    download and text-extract the corpus
src/check_corpus.py    report text provenance per instrument
src/kb.py              chunking, indexing, retrieval, per-concern coverage
src/gapfinder.py       gap classification and recommendations
src/cli.py             command-line demo interface
output/gap_report.json machine-readable gap register
```

## Honest limitations

- The completeness evidence base for Saudi referral letters is from **2007** (n=330, Buraidah) and predates the e-referral rollout. No post-2015 Saudi study measuring referral letter completeness was located. Whether the problem persists is an open question — and measuring it is itself a valid result.
- Globally, only **1 of 10** studies in the [2026 systematic review of NLP referral triage](https://www.frontiersin.org/journals/health-services/articles/10.3389/frhs.2026.1797583/full) demonstrated operational benefit (~8 hours/week of assessment time). **No study anywhere shows improved time-to-treatment or clinical outcomes.** This project claims saved reviewer time and better within-queue ranking. It does not claim outcomes.
- Referral acceptance rose from 74.13% to 90.19% between 2020–21 and 2023–24 **without** AI. The case for this system is not that referral processing is failing.
- **Zero studies exist from the Gulf or in Arabic**, and no Arabic referral corpus is publicly available. That is the originality claim and also the principal limitation.
