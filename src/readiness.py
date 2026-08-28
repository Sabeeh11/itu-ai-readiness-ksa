"""ITU AI Readiness Report 2.0 factor and dimension mappings for this submission."""

from __future__ import annotations

FACTORS = [
    {
        "id": "data",
        "label": "Data",
        "contribution": "strong",
        "summary": "De-identification stage, health data residency, and the anonymisation method gap (G4).",
    },
    {
        "id": "research",
        "label": "Research",
        "contribution": "limited",
        "summary": "No Gulf/Arabic referral-screening study exists; the evidence base is cited honestly.",
    },
    {
        "id": "deployment",
        "label": "Deployment Support",
        "contribution": "moderate",
        "summary": "Level 1/Level 2 split at PP; infrastructure and cloud residency mapped to C and D.",
    },
    {
        "id": "standards",
        "label": "Standards",
        "contribution": "strong",
        "summary": "Y.3172 node mapping and three proposed standardisation gaps.",
    },
    {
        "id": "open_source",
        "label": "Open Source and Code",
        "contribution": "moderate",
        "summary": "Analyser and knowledge base published for inspection and reuse.",
    },
    {
        "id": "sandbox",
        "label": "Sandbox Environments",
        "contribution": "strong",
        "summary": "Five evaluation scenarios function as a policy sandbox (S2, S4 headline).",
    },
]

DIMENSIONS = [
    {
        "id": "D4",
        "label": "Contextualization and Regional Impact",
        "factors": ["Data", "Research", "Deployment"],
        "measures": "Regional inputs, local instruments, and adoption of indigenous solutions.",
        "addressed": (
            "29 instruments, predominantly Saudi; HIPAA included only as a methodological contrast for G4. "
            "No Gulf or Arabic referral-screening study exists anywhere in the literature."
        ),
    },
    {
        "id": "D7",
        "label": "Strategy Alignment",
        "factors": ["Standards"],
        "measures": "Coordination across distributed institutions and domains.",
        "addressed": (
            "Gaps fall to five separate bodies — SDAIA, SFDA, MOH, Saudi Health Council, and NCA. "
            "No single authority owns non-device health AI."
        ),
    },
    {
        "id": "D9",
        "label": "Impacts of Humans in AI Integration",
        "factors": ["Sandbox"],
        "measures": "Referral of AI decisions back to domain experts.",
        "addressed": (
            "Scenario S4 tests automated rejection with no human review and finds it lawful today. "
            "The referral preset imposes voluntary oversight constraints."
        ),
    },
    {
        "id": "D10",
        "label": "AI and Policies",
        "factors": ["Sandbox", "Deployment"],
        "measures": "Policies for AI and AI for policy extrapolation.",
        "addressed": (
            "The entire contribution: node-by-node mapping, gap classification, and five "
            "authority-specific recommendations. Scenarios extrapolate policy interventions."
        ),
    },
    {
        "id": "D11",
        "label": "AI for Inclusion",
        "factors": ["Sandbox"],
        "measures": "Accessibility, language coverage, and edge-vs-cloud privacy.",
        "addressed": (
            "G9 records no Arabic dialect or disability-access requirements. "
            "The Level 1/Level 2 split at PP is a candidate edge-privacy pattern."
        ),
    },
]

STANDARDS_GAPS = [
    "Y.3172 defines the PP node with no attached privacy obligation.",
    "Y.3172 is silent on which node boundary enforces data residency — PP split is a candidate pattern.",
    "Y.3172's P node has no notion of advisory versus blocking enforcement.",
]


def readiness_payload() -> dict:
    return {
        "factors": FACTORS,
        "dimensions": DIMENSIONS,
        "standards_gaps": STANDARDS_GAPS,
    }
