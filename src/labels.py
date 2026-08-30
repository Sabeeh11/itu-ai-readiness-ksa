"""Human-readable labels for Y.3172 nodes and governance concerns."""

from __future__ import annotations

# Standard ITU-T Y.3172 node names (what the letter codes mean).
NODE_NAMES: dict[str, str] = {
    "SRC": "Source",
    "C": "Collector",
    "PP": "Preprocessor",
    "M": "Model",
    "P": "Policy",
    "D": "Distributor",
    "SINK": "Target",
}

# Use-case role of each node in this referral-screening deployment.
NODE_LABELS: dict[str, str] = {
    "SRC": "Referral drafted at clinic",
    "C": "On-premises intake gateway",
    "PP": "De-identification (on-premises)",
    "M": "Completeness and appropriateness models",
    "P": "Advisory policy and human review",
    "D": "Distribution to clinicians and coordinators",
    "SINK": "Clinician and coordinator workstations",
}

NODE_DESCRIPTIONS: dict[str, str] = {
    "SRC": "Referral documents and supporting clinical extracts are created at the sending facility.",
    "C": "Infrastructure that receives drafted referrals before national submission.",
    "PP": "De-identification runs inside the facility; identifiers must not cross the Level 1 boundary.",
    "M": "Proposed classifiers score completeness and appropriateness over de-identified text.",
    "P": "Outputs are advisory; a named reviewer may override without justification.",
    "D": "Completeness reports and appropriateness flags are returned to authorised recipients.",
    "SINK": "Referring clinicians and receiving coordinators see prompts and flags.",
}

CONCERN_LABELS: dict[str, str] = {
    "consent": "Patient consent",
    "medical_confidentiality": "Medical confidentiality",
    "lawful_basis": "Lawful basis for processing",
    "data_provenance": "Data provenance and lineage",
    "referral_content_standard": "Referral content standard",
    "infrastructure_reliability": "Infrastructure reliability",
    "availability": "System availability",
    "data_residency": "Data residency",
    "cybersecurity": "Cybersecurity controls",
    "input_validation": "Input validation",
    "anonymisation": "Permanent anonymisation",
    "deidentification_method": "De-identification method",
    "reidentification_risk": "Re-identification risk assessment",
    "minimum_necessary": "Minimum necessary processing",
    "indirect_identifiers": "Indirect identifiers",
    "model_validation": "Model validation",
    "dataset_composition": "Dataset composition",
    "benchmarking": "Benchmarking",
    "accuracy_certification": "Accuracy certification",
    "bias_evaluation": "Bias evaluation",
    "human_oversight": "Human oversight",
    "override": "Clinician override",
    "advisory_vs_blocking": "Advisory vs blocking enforcement",
    "threshold_justification": "Threshold justification",
    "audit_trail": "Audit trail",
    "permitted_purposes": "Permitted purposes",
    "data_sharing": "Data sharing",
    "marketing_prohibition": "Marketing prohibition",
    "ai_security": "AI-specific security",
    "ai_disclosure": "AI disclosure",
    "patient_communication": "Patient communication",
    "language_accessibility": "Arabic language accessibility",
    "impairment_accessibility": "Disability accessibility",
    "duty_to_explain": "Duty to explain",
    "corpus_level_finding": "Corpus-level finding",
    "instrument_currency": "Instrument currency",
}

STATUS_LABELS = {
    "covered": "Covered",
    "duty_only": "Duty only",
    "no_cover": "No cover",
    "scope_gap": "Scope gap",
    "policy_gap": "Policy gap",
    "method_gap": "Method gap",
    "currency_gap": "Currency gap",
}

AUTHORITY_BY_GAP: dict[str, str] = {
    "G1": "SFDA",
    "G2": "SFDA / MOH",
    "G3": "MOH / Saudi Health Council",
    "G4": "SDAIA",
    "G5": "SFDA",
    "G6": "MOH / SDAIA",
    "G7": "NHIC / MOH",
    "G9": "MOH / SDAIA",
    "G10": "NCA",
    "G11": "MOH / Saudi Health Council",
}


def concern_label(concern: str) -> str:
    return CONCERN_LABELS.get(concern, concern.replace("_", " ").title())


def node_name(node: str) -> str:
    return NODE_NAMES.get(node, node)


def node_label(node: str) -> str:
    return NODE_LABELS.get(node, node)
