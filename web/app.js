const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => document.querySelectorAll(sel);

const STEPS = [
  { id: "step-1", nextLabel: "Start assessment" },
  { id: "step-2", nextLabel: "Run assessment" },
  { id: "step-3", nextLabel: "See it on a document" },
  { id: "step-4", nextLabel: "View recommendations" },
  { id: "step-5", nextLabel: "Finish" },
];

let currentStep = 0;
let schema = null;
let methodology = null;
let overview = null;
let lastAssessment = null;
let expandedNode = null;

const TOUR = [
  {
    step: 0,
    title: "What is this prototype?",
    script: "This shows what Saudi healthcare needs before AI-assisted referral screening can be used responsibly. You will see working completeness checks, privacy controls, Y.3172 mapping, and citation-backed policy gaps.",
  },
  {
    step: 1,
    title: "Assess the referral workflow",
    script: "The Ehalati preset is preloaded. Configure how patient data is handled, where processing occurs, and whether outputs advise or block referrals.",
    action: () => applyPreset("referral_screening"),
  },
  {
    step: 2,
    title: "What the assessment found",
    script: "The workflow was mapped to Y.3172, 29 policy instruments were checked, and gaps were classified. Click any pipeline node to see its concerns.",
    action: () => { applyPreset("referral_screening"); return runAssessment(); },
  },
  {
    step: 3,
    title: "Why preprocessing matters",
    script: "Identifiers are removed on-premises before the screening service sees the text. Yet contextual phrases can still identify a patient. This is gap G4 in concrete form.",
  },
  {
    step: 4,
    title: "Recommendations and sources",
    script: "Each gap has a recommended owner — SDAIA, SFDA, MOH, or NCA. All sources are linked in the resources section.",
    action: () => { applyPreset("referral_blocking"); return runAssessment(); },
  },
];

let tourIndex = 0;

async function api(path, opts = {}) {
  const res = await fetch(path, opts);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

function badge(status) {
  if (!status) return "";
  const cls = status.toLowerCase().replace(/ /g, "_");
  const label = (methodology?.status_meanings?.[cls] || status).split(".")[0];
  return `<span class="badge badge-${cls}" title="${methodology?.status_meanings?.[cls] || ""}">${cls.replace(/_/g, " ")}</span>`;
}

function showPanel(id) {
  $$(".panel").forEach((p) => p.classList.remove("active"));
  $(`#${id}`).classList.add("active");
}

function goToStep(index, { skipAction = false } = {}) {
  currentStep = Math.max(0, Math.min(index, STEPS.length - 1));
  const step = STEPS[currentStep];
  showPanel(step.id);
  updateStepper();
  $("#step-back").disabled = currentStep === 0;
  $("#step-next").textContent = currentStep === STEPS.length - 1 ? "Finish" : step.nextLabel;
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function updateStepper() {
  const m = methodology?.steps?.[currentStep];
  $("#stepper-label").textContent = `Step ${currentStep + 1} of ${STEPS.length} · ${m?.title || ""}`;
  $$(".stepper-dot").forEach((dot, i) => {
    dot.classList.toggle("active", i === currentStep);
    dot.classList.toggle("done", i < currentStep);
  });
}

function renderStepperTrack() {
  $("#stepper-track").innerHTML = methodology?.steps?.map((s, i) =>
    `<button type="button" class="stepper-dot${i === 0 ? " active" : ""}" data-step="${i}" title="${s.title}">${i + 1}</button>`
  ).join("") || "";
  $$(".stepper-dot").forEach((dot) => {
    dot.addEventListener("click", () => goToStep(Number(dot.dataset.step)));
  });
}

function renderExplainPanels() {
  methodology?.steps?.forEach((s, i) => {
    const el = $(`#explain-${i + 1}`);
    const sub = $(`#subtitle-${i + 1}`);
    if (sub) sub.textContent = s.subtitle;
    if (el) {
      el.innerHTML = `<h3>How this works</h3><p>${s.explain}</p>`;
      if (i === 2) {
        el.innerHTML += `<ol class="method-list">${methodology.how.map((h) => `<li>${h}</li>`).join("")}</ol>`;
      }
      if (i === 1) {
        el.innerHTML += `<p class="flow-hint">Workflow choices → activated concerns → policy corpus check</p>`;
      }
    }
  });
  $("#workflow-box").innerHTML = `<h3>${methodology.workflow.title}</h3><p>${methodology.workflow.body}</p>`;
  $("#insights-box").innerHTML = `<h3>${methodology.insights.title}</h3><p>${methodology.insights.body}</p>`;
  $("#insights-list").innerHTML = methodology.insights.items.map((item) => `<li>${item}</li>`).join("");
  $("#readiness-path-title").textContent = methodology.readiness_path.title;
  $("#readiness-path-body").textContent = methodology.readiness_path.body;
  if ($("#data-flow")) {
    $("#data-flow").innerHTML = `<h3>Intended data flow</h3><ol class="method-list">${methodology.data_flow.map((s) => `<li>${s}</li>`).join("")}</ol>`;
  }
}

function buildForm(fields, values) {
  const form = $("#assessment-form");
  form.innerHTML = "";
  for (const field of fields) {
    const div = document.createElement("div");
    div.className = "field";
    if (field.type === "boolean") {
      div.innerHTML = `<label><input type="checkbox" name="${field.id}" ${values[field.id] ? "checked" : ""}> ${field.label}</label>`;
    } else {
      const opts = (field.options || []).map((o) =>
        `<option value="${o.value}" ${values[field.id] === o.value ? "selected" : ""}>${o.label}</option>`
      ).join("");
      div.innerHTML = `<label>${field.label}<select name="${field.id}">${opts}</select></label>`;
    }
    form.appendChild(div);
  }
}

function readForm() {
  const values = {};
  for (const el of $$("#assessment-form [name]")) {
    if (el.type === "checkbox") values[el.name] = el.checked;
    else values[el.name] = el.value;
  }
  return values;
}

function applyPreset(presetId) {
  const preset = schema?.presets[presetId];
  if (!preset) return;
  buildForm(schema.fields, preset.values);
  const sel = $("#preset-select");
  if (sel) sel.value = presetId;
}

async function loadSchema() {
  schema = await api("/api/assessment/schema");
  const sel = $("#preset-select");
  sel.innerHTML = Object.entries(schema.presets).map(([id, p]) =>
    `<option value="${id}">${p.label}</option>`
  ).join("");
  sel.addEventListener("change", () => applyPreset(sel.value));
  applyPreset("referral_screening");
}

async function runAssessment() {
  const values = readForm();
  lastAssessment = await api("/api/assessment", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(values),
  });
  renderResults(lastAssessment);
  goToStep(2);
  return lastAssessment;
}

function renderFraming() {
  $("#results-framing").innerHTML = `
    <article class="card workflow-card"><h4>Referral workflow</h4><p>Completeness check, on-premises de-identification, advisory output to staff.</p></article>
    <article class="card insights-card"><h4>Assessment insights</h4><p>Pipeline coverage, material blockers, and authority-specific recommendations from 29 policy instruments.</p></article>`;
}

function renderLegend() {
  const meanings = methodology?.status_meanings || {};
  $("#status-legend").innerHTML = `<strong>Status legend:</strong> ` +
    Object.entries(meanings).map(([k, v]) =>
      `${badge(k)} <span class="legend-text">${v.split(".")[0]}</span>`
    ).join(" · ");
}

function renderPipeline(pipeline) {
  const nodes = pipeline.map((n) => {
    const expanded = expandedNode === n.node;
    const concerns = (n.concerns || []).map((c) => `
      <div class="concern-item">
        ${badge(c.gap_kind || c.status)}
        <strong>${c.concern_label}</strong>
        <div class="meta">${c.rationale}</div>
        ${c.gap_id ? `<div class="meta">Gap ${c.gap_id}${c.recommendation ? ` · ${c.recommendation}` : ""}</div>` : ""}
      </div>`).join("");
    return `
      <div class="pipe-node level${n.level} ${n.gap_count ? "has-gap" : ""} ${expanded ? "expanded" : ""}" data-node="${n.node}">
        <button type="button" class="pipe-btn">
          <span class="code">${n.node}</span>
          <span class="pipe-label">${n.label}</span>
          <span class="meta">${n.concern_count} concern(s) · ${n.gap_count} gap(s)</span>
        </button>
        ${expanded ? `<div class="pipe-concerns">${concerns || "<p class='meta'>No concerns activated for this node.</p>"}</div>` : ""}
      </div>`;
  }).join("");

  $("#pipeline-map").innerHTML = `
    <h3>Y.3172 pipeline <span class="tip" title="${methodology?.tooltips?.y3172 || ""}">?</span></h3>
    <p class="meta">Click a node to see all activated concerns. Level 1 boundary at PP — identifiers never cross to Level 2.</p>
    <div class="pipeline">${nodes}</div>
    <div class="level-boundary"><span>Level 1 (on-premises)</span><span>Level 2 (cloud / model)</span></div>`;

  $$(".pipe-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const node = btn.closest(".pipe-node").dataset.node;
      expandedNode = expandedNode === node ? null : node;
      renderPipeline(pipeline);
    });
  });
}

function renderResults(data) {
  $("#results-empty").classList.add("hidden");
  $("#results-content").classList.remove("hidden");
  renderFraming();
  renderLegend();

  const corpusNote = overview
    ? `<span class="meta">Saudi corpus overall: ${overview.governed}/${overview.total_concerns} concerns governed across the full knowledge base</span>`
    : "";

  $("#executive-summary").innerHTML = `
    <h3>${data.readiness_summary}</h3>
    <p>${data.executive_summary}</p>
    <p><strong>This workflow assessment:</strong>
       ${data.counts.activated} concerns activated ·
       <strong>${data.counts.covered}</strong> covered ·
       <strong>${data.counts.duty_only}</strong> duty only ·
       <strong>${data.counts.gaps}</strong> gaps</p>
    ${corpusNote}
    <p class="disclaimer">${data.disclaimer}</p>`;

  $("#material-blockers").innerHTML = data.material_blockers.length
    ? `<h3>Top material blockers</h3>` + data.material_blockers.map((b) => `
        <div class="finding-row">
          ${badge(b.gap_kind || b.status)}
          <strong>${b.node_label} / ${b.concern_label}</strong>
          <div class="meta">${b.statement || b.rationale}</div>
          ${b.recommendation ? `<div>→ ${b.recommendation}</div>` : ""}
          ${b.authority ? `<div class="meta">Authority: ${b.authority}</div>` : ""}
        </div>`).join("")
    : "";

  renderPipeline(data.pipeline);
}

function renderDocument(doc, title, highlightRemoved) {
  const patient = doc.patient.map(([k, v]) =>
    `<tr class="${highlightRemoved && v.includes("REMOVED") ? "removed" : ""}"><th>${k}</th><td>${v}</td></tr>`
  ).join("");
  const clinical = doc.clinical.map((c) =>
    `<tr class="${c.absent ? "absent" : ""}"><th>${c.field}</th><td>${c.value}</td></tr>`
  ).join("");
  return `
    <div class="doc-panel">
      <h4>${title}</h4>
      <table class="doc-table">
        <tr><th>Reference</th><td>${doc.ref}</td></tr>
        <tr><th>Date</th><td>${doc.date}</td></tr>
        ${patient}
        <tr><th>Facility</th><td>${doc.referring.facility}</td></tr>
        <tr><th>Physician</th><td>${doc.referring.physician}</td></tr>
        <tr><th>Specialty requested</th><td>${doc.requested.specialty} (${doc.requested.urgency})</td></tr>
        ${clinical}
      </table>
      <h5>Clinician free text</h5>
      <pre class="doc-text">${doc.free_text}</pre>
    </div>`;
}

async function showReferral(index) {
  const data = await api(`/api/referrals/${index}`);
  $("#referral-detail").innerHTML = `
    <div class="referral-header">
      <h3>${data.ref}</h3>
      <p>Completeness: ${data.completeness.present}/${data.completeness.total} clinical fields
         ${data.completeness.missing_fields.length ? `(missing: ${data.completeness.missing_fields.join(", ")})` : ""}</p>
      <p>${data.deidentification.direct_identifiers_removed} direct identifiers removed ·
         ${data.residual_risk.candidate_count} quasi-identifier(s) survive</p>
    </div>
    <div class="referral-columns">
      ${renderDocument(data.document_before, "Before de-identification", false)}
      ${renderDocument(data.document_after, "After de-identification", true)}
    </div>
    ${data.residual_risk.candidates.map((c) => `
      <div class="finding-row flagged">
        ${badge("method_gap")} "${c.snippet}" — ${c.reason}
      </div>`).join("")}
    <p class="disclaimer">This illustrates gap G4: Saudi law requires permanent anonymisation but publishes no method to adjudicate residual risk. ${data.completeness.note}</p>`;
}

async function loadOverview() {
  overview = await api("/api/overview");
  $("#overview-stats").innerHTML = `
    <div class="stat"><strong>${overview.corpus_documents}</strong> policy instruments</div>
    <div class="stat"><strong>${overview.governed}/${overview.total_concerns}</strong> concerns governed in corpus</div>
    <div class="stat"><strong>${overview.gap_count}</strong> gap findings</div>
    <div class="stat"><span class="headline">${overview.headline}</span></div>`;
  $("#pipeline-headline").textContent = overview.headline;
}

function renderSourcesPreview(items, targetId, limit = 5) {
  const el = $(targetId);
  if (!el) return;
  el.innerHTML = items.slice(0, limit).map((item) => `
    <div class="finding-row">
      ${item.kind ? badge(item.kind) : ""}
      <strong>${item.title || item.claim}</strong>
      <div class="meta">${item.issuer || item.source || ""}${item.url ? ` · <a href="${item.url}" target="_blank">source</a>` : ""}</div>
    </div>`).join("");
}

async function loadSourcesPreview() {
  const [evidence, corpus] = await Promise.all([api("/api/evidence"), api("/api/corpus")]);
  const evidenceItems = evidence.items.map((item) => ({
    kind: item.kind,
    claim: item.claim,
    source: item.source,
    url: item.url,
  }));
  renderSourcesPreview(evidenceItems, "#sources-preview-list", 4);
  const corpusItems = corpus.documents.map((d) => ({
    title: d.title,
    issuer: d.issuer,
    url: d.url,
  }));
  renderSourcesPreview(corpusItems, "#sources-step5-list", 6);
}

async function loadEvidence() {
  const data = await api("/api/evidence");
  $("#evidence-list").innerHTML = data.items.map((item) => `
    <div class="finding-row">
      ${badge(item.kind)}
      <strong>${item.claim}</strong>
      <div class="meta">${item.source}${item.url ? ` · <a href="${item.url}" target="_blank">source</a>` : ""}</div>
    </div>`).join("");
  $("#future-validation").innerHTML = `<h3>Future validation path</h3><ul>` +
    data.future_validation.map((s) => `<li>${s}</li>`).join("") + `</ul>`;
}

async function loadCoverage() {
  const data = await api("/api/coverage");
  $("#coverage-matrix").innerHTML = data.nodes.map((node) => `
    <div class="card">
      <h3>${node.node} — ${node.label}</h3>
      ${node.concerns.map((c) => `
        <div class="finding-row">
          ${badge(c.status)} <strong>${c.concern_label}</strong>
          <div class="meta">${c.citations.map((x) => x.doc_id).join(", ") || "—"}</div>
        </div>`).join("")}
    </div>`).join("");
}

async function loadReadiness() {
  const data = await api("/api/readiness");
  $("#factors-grid").innerHTML = data.factors.map((f) => `
    <article class="card">
      <h4>${f.label} <span class="badge badge-${f.contribution === "strong" ? "covered" : "proposed"}">${f.contribution}</span></h4>
      <p>${f.summary}</p>
    </article>`).join("");
  $("#dimensions-list").innerHTML = data.dimensions.map((d) => `
    <div class="card">
      <h4>${d.id}: ${d.label}</h4>
      <p class="meta">Factors: ${d.factors.join(", ")}</p>
      <p><em>${d.measures}</em></p>
      <p>${d.addressed}</p>
    </div>`).join("");
  $("#standards-gaps").innerHTML = data.standards_gaps.map((s) => `<li>${s}</li>`).join("");
}

async function loadReferrals() {
  const data = await api("/api/referrals");
  const sel = $("#referral-select");
  sel.innerHTML = data.referrals.map((r) =>
    `<option value="${r.index}">${r.ref} — ${r.specialty}</option>`
  ).join("");
  sel.onchange = () => showReferral(sel.value);
  showReferral(1);
}

async function loadScenarios() {
  const data = await api("/api/scenarios");
  $("#scenario-list").innerHTML = data.scenarios.map((s) => `
    <article class="card scenario-card" data-id="${s.id}">
      <h4>${s.id}: ${s.title}</h4>
      <p class="meta">[${s.kind}]</p>
      <p>${s.question}</p>
    </article>`).join("");
  $$(".scenario-card").forEach((card) => {
    card.addEventListener("click", async () => {
      const result = await api(`/api/scenarios/${card.dataset.id}`);
      const detail = $("#scenario-detail");
      detail.classList.remove("hidden");
      detail.innerHTML = `
        <h3>${result.scenario.id}: ${result.scenario.title}</h3>
        <ol>${result.scenario.steps.map((s) => `<li>${s}</li>`).join("")}</ol>
        <p><strong>Question:</strong> ${result.scenario.question}</p>
        <p><strong>Finding:</strong> ${result.expected_finding}</p>
        <p>${result.unmet_count} of ${result.total_count} concerns ungoverned or without a published method.</p>`;
    });
  });
}

async function loadGaps() {
  const data = await api("/api/gaps");
  $("#gaps-by-authority").innerHTML = Object.entries(data.by_authority).map(([auth, gaps]) => `
    <div class="card">
      <h3>${auth}</h3>
      ${gaps.map((g) => `
        <div class="finding-row">
          ${badge(g.kind.toLowerCase().replace(/ /g, "_"))}
          <strong>${g.gap_id || ""} ${g.node_label} / ${g.concern_label}</strong>
          <p>${g.statement}</p>
          <p class="meta">→ ${g.recommendation}</p>
        </div>`).join("")}
    </div>`).join("");
}

async function doSearch(query) {
  if (!query) return;
  const data = await api(`/api/search?q=${encodeURIComponent(query)}`);
  $("#search-results").innerHTML = data.hits.length
    ? data.hits.map((h) => `
        <div class="finding-row">
          <strong>${h.doc_id}</strong> score=${h.score} ${h.binding ? badge("covered") : badge("proposed")}
          <p>${h.title}</p>
          <p class="meta">${h.snippet}…</p>
          <a href="${h.url}" target="_blank">${h.url}</a>
        </div>`).join("")
    : `<p class="empty">No matching passage.</p>`;
}

async function loadCorpus() {
  const data = await api("/api/corpus");
  $("#corpus-count").textContent = `${data.count} instruments (${data.saudi_count} Saudi)`;
  $("#corpus-table tbody").innerHTML = data.documents.map((d) => `
    <tr>
      <td>${d.issuer}</td>
      <td>${d.title}</td>
      <td>${d.binding ? "Yes" : "No"}</td>
      <td>${d.provenance}</td>
      <td><a href="${d.url}" target="_blank">link</a></td>
    </tr>`).join("");
}

function exportJson(data, filename) {
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = filename;
  a.click();
}

function showRefPanel(id) {
  $$(".panel").forEach((p) => p.classList.remove("active"));
  const panel = $(`#${id}`);
  panel.classList.add("active");
  if (!panel.querySelector(".back-to-demo")) {
    const back = document.createElement("button");
    back.type = "button";
    back.className = "btn back-to-demo";
    back.textContent = "← Back to demo";
    back.addEventListener("click", hideRefPanels);
    panel.prepend(back);
  }
  $("#step-footer").classList.add("hidden");
}

function hideRefPanels() {
  $("#step-footer").classList.remove("hidden");
  goToStep(currentStep);
}

async function handleStepNext() {
  if (currentStep === 1) {
    await runAssessment();
    return;
  }
  if (currentStep < STEPS.length - 1) {
    goToStep(currentStep + 1);
  }
}

function startTour() {
  tourIndex = 0;
  $("#tour-overlay").classList.remove("hidden");
  renderTourStep();
}

async function renderTourStep() {
  const step = TOUR[tourIndex];
  $("#tour-step").textContent = `Step ${tourIndex + 1} of ${TOUR.length}`;
  $("#tour-title").textContent = step.title;
  $("#tour-script").textContent = step.script;
  goToStep(step.step, { skipAction: true });
  if (step.action) await step.action();
}

async function init() {
  methodology = await api("/api/methodology");
  renderStepperTrack();
  renderExplainPanels();
  updateStepper();

  $("#step-back").addEventListener("click", () => goToStep(currentStep - 1));
  $("#step-next").addEventListener("click", handleStepNext);
  $("#run-assessment").addEventListener("click", runAssessment);
  $("#export-assessment").addEventListener("click", () => {
    if (lastAssessment) exportJson(lastAssessment, "assessment.json");
  });
  $("#export-corpus").addEventListener("click", async () => {
    exportJson(await api("/api/corpus/export"), "knowledge_base.json");
  });
  $("#search-btn").addEventListener("click", () => doSearch($("#search-input").value));
  $("#search-input").addEventListener("keydown", (e) => {
    if (e.key === "Enter") doSearch($("#search-input").value);
  });
  $$(".ref-links button").forEach((btn) => {
    btn.addEventListener("click", () => showRefPanel(btn.dataset.ref));
  });
  $("#view-sources-btn").addEventListener("click", () => showRefPanel("corpus"));
  $("#view-all-sources").addEventListener("click", () => showRefPanel("corpus"));
  $("#view-all-sources-5").addEventListener("click", () => showRefPanel("corpus"));
  document.querySelector(".ref-dropdown")?.addEventListener("toggle", (e) => {
    if (!e.target.open) hideRefPanels();
  });

  $("#tour-btn").addEventListener("click", startTour);
  $("#tour-close").addEventListener("click", () => $("#tour-overlay").classList.add("hidden"));
  $("#tour-prev").addEventListener("click", () => {
    if (tourIndex > 0) { tourIndex--; renderTourStep(); }
  });
  $("#tour-next").addEventListener("click", async () => {
    if (tourIndex < TOUR.length - 1) { tourIndex++; await renderTourStep(); }
    else $("#tour-overlay").classList.add("hidden");
  });

  await loadSchema();
  await loadOverview();
  await loadSourcesPreview();
  loadEvidence();
  loadCoverage();
  loadReadiness();
  loadReferrals();
  loadScenarios();
  loadGaps();
  loadCorpus();
}

document.addEventListener("DOMContentLoaded", init);
