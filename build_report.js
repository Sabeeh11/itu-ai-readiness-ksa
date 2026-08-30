const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell,
  WidthType, ShadingType, AlignmentType, BorderStyle, ExternalHyperlink,
} = require("docx");

const FULL = 9360;            // usable width, DXA, US Letter with 1.5cm margins
const HDR = "1F3864";
const ACCENT = "2E74B5";

const p = (text, o = {}) =>
  new Paragraph({
    spacing: { after: o.after ?? 120, line: 259 },
    alignment: o.align,
    indent: o.indent,
    children: [new TextRun({ text, bold: o.bold, italics: o.italics, size: o.size ?? 20, color: o.color })],
  });

const rich = (runs, o = {}) =>
  new Paragraph({ spacing: { after: o.after ?? 120, line: 259 }, indent: o.indent, children: runs });

const t = (text, o = {}) => new TextRun({ text, bold: o.bold, italics: o.italics, size: o.size ?? 20, color: o.color });

const link = (text, url) =>
  new ExternalHyperlink({ children: [new TextRun({ text, size: 16, color: ACCENT, underline: {} })], link: url });

const linkBody = (text, url) =>
  new ExternalHyperlink({ children: [new TextRun({ text, size: 20, color: ACCENT, underline: {} })], link: url });

const h1 = (text) =>
  new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 280, after: 140 },
    children: [new TextRun({ text, bold: true, size: 26, color: HDR })],
  });

const h2 = (text) =>
  new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 200, after: 100 },
    children: [new TextRun({ text, bold: true, size: 22, color: HDR })],
  });

const bullet = (text, o = {}) =>
  new Paragraph({
    numbering: { reference: "bul", level: 0 },
    spacing: { after: 60, line: 259 },
    children: [new TextRun({ text, size: o.size ?? 20, bold: o.bold })],
  });

const cell = (children, width, o = {}) =>
  new TableCell({
    width: { size: width, type: WidthType.DXA },
    shading: o.shade ? { type: ShadingType.CLEAR, fill: o.shade, color: "auto" } : undefined,
    margins: { top: 60, bottom: 60, left: 90, right: 90 },
    children,
  });

const hcell = (text, width) =>
  cell([new Paragraph({ children: [new TextRun({ text, bold: true, size: 18, color: "FFFFFF" })] })], width, { shade: HDR });

// ---------------------------------------------------------------- node table
const NODE_COLS = [900, 2600, 3400, 2460];
const nodeRows = [
  ["SRC", "Referral documents drafted at primary care and secondary facilities, plus supporting EHR extracts.",
   "IS0303 §8 (opt-out, treatment relationship); Law of Practicing Healthcare Professions Art. 21 (confidentiality); PDPL Implementing Regs Art. 26 (health data, minimum necessary); MOH Ehalati referral standards.",
   "G3 — no Saudi statute on electronic health records as such.\nG11 — no national standard defines what a complete referral must contain."],
  ["C", "On-premises intake gateway receiving drafted referrals before submission.",
   "NHIC Telehealth Application Guidelines (tier 3–4 infrastructure, in-Kingdom storage); NDMO Data Management Standards v1.5; NCA CCC-1:2020.",
   "G7 — the governing telehealth instrument lapsed 31 Dec 2021; the NHIC guidelines carry no version or date."],
  ["PP", "De-identification stage. Strips names, national ID, contact details, dates, MRNs. Emits de-identified clinical text.",
   "PDPL Implementing Regs Art. 26; SDAIA Guide for Controllers/Processors (direct and indirect identifiers, permanently); SDAIA Destruction/Anonymization Guideline; IS0303 §11 (re-identification risk assessment).",
   "G4 — HEADLINE. Anonymisation and risk assessment are mandated; no identifier schedule, threshold or method is published."],
  ["M", "Completeness classifier (field presence) and appropriateness classifier over de-identified text.",
   "SFDA MDS-G-010 (dataset composition, three-part validation) — applies only to medical devices; ITU FG-AI4H DEL7.4; DEL5.5; WHO AI-for-health ethics.",
   "G1 — document screening is not a device, so MDS-G010 does not bind it.\nG5 — nothing in KSA validates model accuracy."],
  ["P", "No auto-rejection. Appropriateness flags are advisory and routed to a named reviewer who may override. Thresholds versioned and auditable.",
   "SFDA MDS-G-010 (“enhance users' performance, not replace them”); IS0303 §8 (break-glass with audit trail); SDAIA AI Ethics Principles (non-binding).",
   "G2 — outside the device route there is no Saudi human-in-the-loop or override obligation at all."],
  ["D", "Returns the completeness report to the referring clinician; forwards appropriateness flags to the receiving coordinator.",
   "IS0303 §3 (permitted purposes, marketing prohibited); NDMO Interim Regulations (data sharing, in-Kingdom); NCA CCC-1:2020.",
   "G10 — NCA ECC-2:2024, inspected across all 108 controls, contains no AI provisions."],
  ["SINK", "Referring clinician's workstation (completeness prompts); receiving coordinator's queue (appropriateness flags).",
   "Law of Practicing Healthcare Professions Art. 18 (duty to explain); WHO guidance on large multi-modal models (non-binding).",
   "G6 — no governance of AI-output disclosure.\nG9 — nothing on Arabic dialect variation or accessibility in health AI."],
];

const nodeTable = new Table({
  columnWidths: NODE_COLS,
  width: { size: FULL, type: WidthType.DXA },
  rows: [
    new TableRow({ tableHeader: true, children: [
      hcell("Node", NODE_COLS[0]), hcell("Our solution", NODE_COLS[1]),
      hcell("Mapped documents (policies, regulations, standards)", NODE_COLS[2]),
      hcell("Gap identified", NODE_COLS[3])] }),
    ...nodeRows.map((r, i) => new TableRow({ children: [
      cell([new Paragraph({ children: [new TextRun({ text: r[0], bold: true, size: 18 })] })], NODE_COLS[0], { shade: i % 2 ? "F2F5FA" : undefined }),
      cell([new Paragraph({ children: [new TextRun({ text: r[1], size: 16 })] })], NODE_COLS[1], { shade: i % 2 ? "F2F5FA" : undefined }),
      cell([new Paragraph({ children: [new TextRun({ text: r[2], size: 16 })] })], NODE_COLS[2], { shade: i % 2 ? "F2F5FA" : undefined }),
      cell(r[3].split("\n").map((line) => new Paragraph({ spacing: { after: 40 }, children: [new TextRun({ text: line, size: 16, color: "9C1F1F" })] })), NODE_COLS[3], { shade: i % 2 ? "F2F5FA" : undefined }),
    ] })),
  ],
});

// ------------------------------------------------------- readiness dimensions
const DIM_COLS = [2500, 3000, 3860];
const dimRows = [
  ["D10 — AI & Policies\n(factors: Sandbox, Deployment)",
   "The entire contribution. The report's own example of a horizontal generic policy is “the privacy rules of usage of data in model training in healthcare”, and it lists “data sovereignty metrics: policies related to ownership and movement of data” as a metric.",
   "We map every Y.3172 node to binding instruments and classify what is missing into method, scope, policy and currency gaps. Five recommendations are addressed to SDAIA, SFDA, MOH, the Saudi Health Council and NCA respectively."],
  ["D4 — Contextualization & Regional Impact\n(factors: Data, Research, Deployment)",
   "Measures whether solutions are adapted with regional inputs, and identifies gaps for local industry to address.",
   "Every instrument in the knowledge base is Saudi except seven international references (WHO ×2, FG-AI4H ×3, HIPAA, and Y.3172 itself) used deliberately for contrast. The HIPAA comparison converts an absence into an actionable recommendation. No Gulf or Arabic study exists in the world literature on this task."],
  ["D7 — Strategy Alignment\n(factor: Standards)",
   "Coordination of AI integration across distributed institutions; the interoperability gap appears in the intent description passed between service providers.",
   "The gaps fall to five separate bodies — SDAIA (G4), SFDA (G1/G5), MOH and Saudi Health Council (G3/G11), NCA (G10), NHIC (G7). No single authority owns non-device health AI, which is why the vacuum persists. Our gap register is addressed institution by institution."],
  ["D9 — Impacts of Humans in AI Integration\n(factor: Sandbox)",
   "Measures the referral of AI decisions back to domain experts to guarantee accountability of the decision.",
   "Scenario S4 tests exactly this and finds the obligation absent. We compare our advisory design against a compliant competitor that auto-rejects with no human review, and show both are equally lawful today."],
  ["D11 — AI for Inclusion\n(factor: Sandbox)",
   "Accessibility, language coverage, and edge-versus-cloud privacy (“standalone edge with no data leakage to the cloud vs cloud with data transferred”).",
   "G9 records that nothing addresses Arabic dialect variation or accessibility in health AI. Our Level 1 / Level 2 split at the PP boundary is precisely the standalone-edge privacy pattern the dimension measures."],
];

const dimTable = new Table({
  columnWidths: DIM_COLS,
  width: { size: FULL, type: WidthType.DXA },
  rows: [
    new TableRow({ tableHeader: true, children: [
      hcell("Dimension (and mapped factor)", DIM_COLS[0]),
      hcell("What the dimension measures", DIM_COLS[1]),
      hcell("How this submission addresses it", DIM_COLS[2])] }),
    ...dimRows.map((r, i) => new TableRow({ children: [
      cell(r[0].split("\n").map((l, j) => new Paragraph({ spacing: { after: 30 }, children: [new TextRun({ text: l, size: 16, bold: j === 0 })] })), DIM_COLS[0], { shade: i % 2 ? "F2F5FA" : undefined }),
      cell([new Paragraph({ children: [new TextRun({ text: r[1], size: 16 })] })], DIM_COLS[1], { shade: i % 2 ? "F2F5FA" : undefined }),
      cell([new Paragraph({ children: [new TextRun({ text: r[2], size: 16 })] })], DIM_COLS[2], { shade: i % 2 ? "F2F5FA" : undefined }),
    ] })),
  ],
});

// ------------------------------------------------------------------ scenarios
const scen = (id, title, kind, steps, finding) => [
  rich([t(`${id}. ${title}  `, { bold: true, size: 20 }), t(`[${kind}]`, { italics: true, size: 16, color: "666666" })], { after: 60 }),
  ...steps.map((s, i) => rich([t(`Step ${i + 1}. `, { bold: true, size: 18 }), t(s, { size: 18 })], { after: 50, indent: { left: 260 } })),
  rich([t("Knowledge base finding. ", { bold: true, size: 18, color: "9C1F1F" }), t(finding, { size: 18 })], { after: 180, indent: { left: 260 } }),
];

// ---------------------------------------------------------------- appendix KB
const CORPUS = JSON.parse(fs.readFileSync("data/corpus.json", "utf8"));
const KB = CORPUS.documents
  .slice()
  .sort((a, b) => a.issuer.localeCompare(b.issuer) || a.title.localeCompare(b.title))
  .map((d) => [d.issuer, d.title + (d.year ? ` (${d.year})` : ""), d.url]);

const KB_COLS = [1700, 4400, 3260];
const kbTable = new Table({
  columnWidths: KB_COLS,
  width: { size: FULL, type: WidthType.DXA },
  rows: [
    new TableRow({ tableHeader: true, children: [hcell("Issuer", KB_COLS[0]), hcell("Instrument", KB_COLS[1]), hcell("Reference link", KB_COLS[2])] }),
    ...KB.map((r, i) => new TableRow({ children: [
      cell([new Paragraph({ children: [new TextRun({ text: r[0], size: 15 })] })], KB_COLS[0], { shade: i % 2 ? "F2F5FA" : undefined }),
      cell([new Paragraph({ children: [new TextRun({ text: r[1], size: 15 })] })], KB_COLS[1], { shade: i % 2 ? "F2F5FA" : undefined }),
      cell([new Paragraph({ children: [link(r[2].length > 62 ? r[2].slice(0, 62) + "…" : r[2], r[2])] })], KB_COLS[2], { shade: i % 2 ? "F2F5FA" : undefined }),
    ] })),
  ],
});

const FILL = (label) =>
  rich([t(`${label}: `, { bold: true }), t("[ TO COMPLETE ]", { color: "B00000", bold: true })], { after: 60 });

const doc = new Document({
  numbering: { config: [{ reference: "bul", levels: [{ level: 0, format: "bullet", text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 340, hanging: 200 } } } }] }] },
  styles: { default: { document: { run: { font: "Calibri", size: 20 } } } },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 900, bottom: 900, left: 1080, right: 1080 } } },
    children: [
      new Paragraph({ spacing: { after: 60 }, border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: HDR } },
        children: [new TextRun({ text: "AI Readiness Hackathon – KSA Final Submission", bold: true, size: 30, color: HDR })] }),
      p("Health domain · ITU-T Y.3172 machine learning pipeline · AI Readiness Framework 2.0", { italics: true, color: "666666", after: 200 }),

      FILL("Team name"), FILL("Members name"),
      rich([t("Solution name: ", { bold: true }), t("Referral Screening Governance Gap Analyser")], { after: 60 }),
      FILL("Contact details"),
      rich([t("Repository: ", { bold: true }), linkBody("GitHub link", "https://github.com/Sabeeh11/itu-ai-readiness-ksa")], { after: 60 }),
      rich([t("Demo video: ", { bold: true }), t("[ TO COMPLETE — link, 7 min max ]", { color: "B00000", bold: true })], { after: 240 }),

      h1("1. Introduction"),
      p("Saudi Arabia operates a national electronic medical referral programme, Ehalati, through the Saudi Medical Appointments and Referrals Centre. It processed 755,145 referrals in 2023–24, a 19.34% increase over 2020–21, and triage within it remains a manual process: cases that are not accepted are reviewed by referrals management staff, and life-saving cases are reviewed by an on-call consultant. In a 2025 peer-reviewed analysis of that system, twelve authors — eight of them affiliated with the Ministry of Health's Medical Referrals Centre, the body that operates it — recommended “integrating AI tools for referral triage to optimize patient allocation, thereby reducing unnecessary transfers.”"),
      p("This submission takes that recommendation literally. It proposes an AI system that screens referral documents for completeness and appropriateness before submission, and it treats the governance of that system as the primary object of study rather than an afterthought."),
      p("The contribution is therefore twofold. First, a use case mapped node by node onto the ITU-T Y.3172 machine learning pipeline. Second, and more importantly, a knowledge base of 29 real Saudi and international policy instruments mapped to those same nodes, together with a software tool that identifies where governance is absent, out of scope, or lacking a method by which compliance could be demonstrated. The system is deliberately designed so that it is not a regulated medical device — which is precisely where the regulatory vacuum in Saudi health AI is found."),

      h1("2. Description of the use case and gaps in existing solutions"),
      h2("2.1 The problem"),
      p("Referrals arrive incomplete. The most recent Saudi study measuring referral letter quality (n=330, Buraidah) found that 50% carried no provisional diagnosis, 52% no investigation results, 45% no examination findings and 47% no treatment information; only 30% received a feedback report in return. Separately, and consistently across three independent national analyses, between 55% and 70% of Saudi referrals arise because the sending facility lacks the required subspecialty — a capacity problem that no triage system can solve, but one that makes every avoidable referral more costly. A national analysis of 1.6 million referrals concluded that 55% growth over three years is “potentially inflicting harm on the sustainability of high-quality health systems” and recommended assessing referral appropriateness to identify inefficiencies."),
      h2("2.2 Existing solutions and their gaps"),
      p("Screening today is manual and human. A coordinator reads the referral and forms a judgement. This is accurate but does not scale, is applied inconsistently across regions, and produces no structured record of why a referral was returned. A persistent regional disparity in acceptance — Eastern region 95.65% against Central 85.43% in 2023–24, a gap that survived a system-wide sixteen-point improvement — is consistent with either inconsistent application of screening criteria or with regional differences in specialist capacity. The published data does not distinguish them."),
      p("Internationally, natural language processing has been applied to referral triage, but thinly. A 2026 systematic review found only ten studies worldwide, achieving AUC 0.83–0.96, of which only one demonstrated an operational benefit (approximately eight hours per week of assessment time saved). No study anywhere demonstrates improved time-to-treatment or clinical outcomes. Not one of the ten came from the Middle East, the Gulf, or was conducted in Arabic."),
      h2("2.3 Our solution and what it claims"),
      p("The system reads a draft referral and returns a completeness score naming the specific fields absent, together with an advisory appropriateness flag. Nothing is auto-rejected; every flag is routed to a named human reviewer who may override it without justification. Because referral documents contain names, national ID numbers, contact details and dates of birth, a de-identification stage runs inside the sending facility before the model reads anything, and only de-identified text crosses the facility boundary."),
      p("We claim reviewer time saved, more consistent application of screening criteria across regions, and a structured record of return reasons. We do not claim improved clinical outcomes, because no evidence in the world literature supports such a claim for this class of system."),
      p("The addressed gaps in existing solutions and the evaluation scenarios in section 4 correspond directly: inconsistency across regions is tested by S3, the absence of a content standard by S5, and the risk of automated rejection without human review by S4.", { italics: true }),

      h2("2.4 The software submitted"),
      p("The analyser is delivered in two forms over one engine. A command-line tool prints the node-by-node coverage matrix, the gap register and the five evaluation scenarios. A browser interface presents the same analysis as a five-step assessment: a proposed health AI system is described through fifteen structured questions — advisory or blocking enforcement, named human reviewer, documented override path, audit trail, deployment location, regulatory route — and the analyser activates the governance concerns that that design raises, tests each against the corpus, and returns the resulting gaps grouped by the authority that owns them. The referral system described in this submission is one profile among many the tool accepts; a second built-in profile reproduces scenario S4, the competitor that rejects referrals automatically with no human review."),
      p("Two design decisions carry the evidential weight. First, whether an instrument governs a given concern is a curated legal judgement recorded per document in the governs field of data/corpus.json, not an inference from retrieval score. Retrieval supplies the supporting passage and its citation; it does not decide the question. An earlier version inferred coverage from similarity alone and failed in both directions — missing Article 21 of the Law of Practicing Healthcare Professions on medical confidentiality, and simultaneously crediting IS0303 with a de-identification method it does not contain. A judgement recorded in a data file can be opened and contested line by line; a similarity threshold cannot be argued with. Second, retrieval is Term Frequency-Inverse Document Frequency (TF-IDF): no API key, no network at query time and no stochastic component, so the same query returns the same citations on any machine. Every assessment is stamped with a hash of the corpus file, so any result can be tied to the exact evidence base that produced it."),
      p("The repository carries a self-test of 71 checks asserting that every command runs, that the figures printed on screen are the figures written in this report, and that all sample referral data is unmistakably synthetic. The tool returns a policy-readiness assessment against the included corpus. It is not legal advice, regulatory approval, or evidence of clinical safety, and it says so on every result it produces."),

      h1("3. Mapped documents"),
      h2("3.1 Mapping to the ITU-T Y.3172 machine learning pipeline"),
      p("The pipeline is distributed across two levels. SRC, C and PP execute on-premises inside the sending facility (Level 1); M, P and D may execute in a cloud region (Level 2). Because identifiers are removed at PP, they never cross the level boundary — data residency is satisfied structurally rather than by contract. The final column records where no binding, in-scope instrument governs the node.", { after: 140 }),
      nodeTable,
      p(""),
      p("Reading the final column: seven nodes, and every one carries at least one gap. Four are material enough to state as recommendations in section 5.", { italics: true, after: 60 }),
      p("Whether an instrument governs a given concern is a curated legal judgement, recorded per document in data/corpus.json and open to challenge. Retrieval over the indexed full text supplies the supporting passage and its citation; it does not decide the question. This matters: lexical similarity alone both missed Article 21 of the Law of Practicing Healthcare Professions on medical confidentiality, and wrongly credited IS0303 with supplying a de-identification method it does not contain.", { italics: true, size: 18, after: 160 }),

      h2("3.2 Mapping to the AI Readiness factors and dimensions"),
      p("Five dimensions are mapped in depth rather than all thirteen in outline. The submission's centre of gravity is Dimension 10, and the mapping deliberately extends past the data and model dimensions.", { after: 140 }),
      dimTable,
      p(""),
      p("On the six foundational factors: this submission contributes primarily to Standards (conformance to Y.3172 and identification of two candidate extensions), Sandbox (the evaluation scenarios in section 4 are a policy sandbox — they extrapolate the effect of regulatory interventions against a simulated timeline), Data (the de-identification stage and the anonymisation gap that governs it) and Open Source (the analyser and the full knowledge base are published under an open licence).", { after: 160 }),

      h1("4. Evaluation scenarios"),
      p("Five scenarios. One establishes baseline operation; three probe situations in which the system, or a competitor, behaves in a way that is lawful but troubling; one anticipates a question a judge may add. In each case the knowledge base is queried and the answer is traced to a named instrument, or the absence of one is reported as a gap.", { after: 160 }),
      ...scen("S1", "Baseline deployment", "operational",
        ["The screening system is deployed across primary care centres in one health cluster.",
         "Referring clinicians receive non-blocking prompts naming the fields missing from a draft referral.",
         "After six months, the proportion of referrals arriving with a diagnosis, examination findings and investigation results has risen."],
        "Coverage is real but uneven. Obligations at SRC and C are binding and largely complete. Obligations at M and SINK are either scope-limited to medical devices or entirely absent, and PP carries the headline method gap. 17 of 35 governance concerns are covered by a binding, in-scope instrument; one further concern is governed by a duty for which no method of compliance is published."),
      ...scen("S2", "The re-identification that nobody can adjudicate", "controversy",
        ["A referral's free-text history reads: “Patient is the brother of the mayor of [a town of 4,000] and was seen after the municipal council meeting.”",
         "The de-identification stage removes name, national ID, phone, address, date of birth and MRN. No direct identifier remains.",
         "The sentence about the mayor's brother is not a direct identifier and is retained. The text passes to the model in a cloud region.",
         "A privacy officer asks whether this text was lawfully de-identified before it left the facility."],
        "The question is unanswerable on the current record. SDAIA's Guide requires removal of direct AND indirect identifiers “in a way that permanently makes it impossible to identify the Data Subject”, and IS0303 §11 requires a re-identification risk assessment before release. Neither defines an identifier schedule, a risk threshold, or a method. The operator cannot demonstrate compliance and the regulator cannot audit it. Gap G4."),
      ...scen("S3", "Automating an existing inequity", "controversy",
        ["An audit after eight months compares appropriateness flag rates by originating facility type.",
         "Referrals from small rural centres are flagged as potentially inappropriate at roughly three times the rate of those from urban teaching hospitals.",
         "The model was trained on historical acceptance decisions. Rural referrals were historically rejected more often — predominantly for incomplete documentation, not clinical inappropriateness.",
         "The model has learned to treat documentation poverty as clinical inappropriateness. Rural patients face further delay, widening a disparity already visible in national data."],
        "Nothing binding required anyone to detect this. SDAIA's AI Ethics Principles name Fairness but are non-binding and sector-neutral. SFDA MDS-G-010 requires demographically aligned, multi-centre reference datasets — but applies only to medical devices, which this is not. No Saudi instrument requires subgroup performance reporting for non-device health AI. Gaps G1 and G5."),
      ...scen("S4", "The competitor who does not ask", "judge curveball",
        ["A vendor offers a rival product to the same health cluster.",
         "It automatically rejects any referral scoring below a completeness threshold, returning it without human review.",
         "The threshold was chosen by the vendor. It is unpublished and cites no clinical source.",
         "A patient with an atypical, poorly documented but clinically urgent presentation is auto-rejected twice before a clinician sees the referral."],
        "This is lawful in Saudi Arabia today. Outside the medical-device route there is no obligation for human-in-the-loop, none to make AI enforcement advisory rather than blocking, none to justify a threshold against a published clinical source, and none to disclose that AI made the decision. Our system imposes all four constraints voluntarily; a competitor imposing none is equally compliant. Gap G2 at its sharpest — good practice is optional and the market does not reward it."),
      ...scen("S5", "Complete by whose standard?", "controversy",
        ["A referring clinician disputes a completeness score, arguing the referral contained everything clinically necessary.",
         "The receiving coordinator disagrees.",
         "Both ask what the national standard for referral content actually is."],
        "No published minimum referral dataset exists. MOH publishes referral urgency categories and response-time standards through Ehalati, but not content standards. CBAHI accreditation standards do impose patient-transfer documentation requirements — but as accreditation criteria assessed by periodic survey, not as a published, machine-checkable content specification. Any completeness model must therefore derive its own criteria. Gap G11."),

      h1("5. Findings and recommendations"),
      p("The analyser classifies 22 gaps into four kinds, because each calls for a different remedy. A policymaker can act on “publish a method” far more readily than on “there is no policy”.", { after: 140 }),
      bullet("G4 — a duty without a method (SDAIA). Saudi Arabia mandates permanent anonymisation of health data and mandates a re-identification risk assessment, while publishing neither an identifier schedule nor a risk methodology. Recommendation: publish both, as HHS does for HIPAA."),
      bullet("G2 — no oversight duty outside the device route (SFDA / MOH). Clinical AI that is not a regulated medical device carries no human-in-the-loop obligation anywhere in Saudi law. Recommendation: extend an “enhance, not replace” duty keyed to clinical consequence rather than device classification."),
      bullet("G1 and G5 — the fastest-growing category is unregulated and unvalidated (SFDA). Workflow, administrative and non-diagnostic decision-support AI sits outside every Saudi instrument, and no body validates model performance in any case. Recommendation: a validation regime keyed to clinical impact."),
      bullet("G11 — completeness has no machine-checkable referent (MOH / Saudi Health Council). Referral response-time standards exist; a published minimum referral dataset does not. CBAHI accreditation standards impose transfer-documentation requirements, but as criteria assessed by periodic survey rather than a specification a system can apply. Recommendation: publish a minimum referral dataset."),
      bullet("G10 — AI is absent from the national cybersecurity baseline (NCA). ECC-2:2024 was inspected across all four domains and 108 controls and contains no AI provisions."),
      p(""),
      h2("5.1 Standards gaps proposed to ITU"),
      bullet("Y.3172 defines the PP node without attaching any privacy obligation to it. A companion specification for de-identification at PP, carrying a measurable re-identification threshold, would close G4 generically rather than nation by nation."),
      bullet("Y.3172 supports multi-level pipeline distribution but is silent on which node boundary a data-residency requirement should be enforced at. The Level 1 / Level 2 split at the PP boundary is a candidate pattern: identifiers never cross, so residency is satisfied structurally rather than contractually."),
      bullet("Y.3172's P node carries no notion of advisory versus blocking enforcement — a distinction that determines whether human oversight is real, as scenario S4 demonstrates."),

      h2("5.2 Knowledge base scalability"),
      p("The knowledge base is structured so that jurisdiction is a field, not an assumption. Adding a country means adding its instruments with node tags; the coverage analysis, the gap classification and the scenarios run unchanged. The cross-jurisdiction contrast that produces the G4 finding — Saudi duty against HIPAA method — is the same operation applied to two corpora, and generalises to any pair of jurisdictions. The assessment interface already accepts an arbitrary health AI profile rather than this one, so extending the tool to a new system is a matter of answering its questions differently, and extending it to a new country is a matter of adding instruments."),

      h2("5.3 Limitations stated openly"),
      bullet("The Saudi referral-completeness evidence is from 2007 and predates the e-referral rollout. No post-2015 Saudi study measuring referral letter completeness was located; whether the problem persists is an open question, and measuring it is itself a valid result."),
      bullet("Referral acceptance rose from 74.13% to 90.19% between 2020–21 and 2023–24 without AI, and life-saving referrals are already accepted 100% of the time. The case for this system is not that referral processing is failing."),
      bullet("20 of the 29 instruments are indexed from their full published text, retrieved directly from the issuing authority. The remaining nine are represented by curated extracts of their verified operative provisions, either because the issuer's site blocks automated retrieval or because the reference is a landing page rather than a document. Provenance is recorded per document in data/manifest.json."),
      bullet("The published service-level standards for referral response differ between the MOH website and the peer-reviewed literature. Both are cited; neither is presented as settled."),

      new Paragraph({ pageBreakBefore: true, spacing: { after: 100 },
        children: [new TextRun({ text: "Appendix A — Knowledge base", bold: true, size: 26, color: HDR })] }),
      p("29 instruments, all real and publicly available. This appendix is generated directly from data/corpus.json, so it cannot drift from the corpus the analyser reads. Node tags, binding status and per-document governance concerns are held in data/corpus.json in the repository. This appendix does not count toward the page limit.", { italics: true, after: 140 }),
      kbTable,
      p(""),
      p("Evidence sources for section 2 (referral volumes, acceptance rates, letter quality, and the systematic review of NLP referral triage) are listed in demand-evidence.md in the repository, each with a verified link.", { italics: true, size: 16 }),
    ],
  }],
});

Packer.toBuffer(doc).then((b) => {
  fs.writeFileSync("ITU_AI_Readiness_Submission.docx", b);
  console.log("written:", b.length, "bytes");
});
