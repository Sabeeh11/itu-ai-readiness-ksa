"""Published evidence items for the use-case justification view."""

from __future__ import annotations

EVIDENCE_ITEMS = [
    {
        "kind": "measured",
        "claim": "755,145 e-referrals processed in 2023–24",
        "source": "Healthcare 2025;13(16):1945",
        "url": "https://www.mdpi.com/2227-9032/13/16/1945",
    },
    {
        "kind": "measured",
        "claim": "Referral acceptance rose from 74.13% to 90.19% between 2020–21 and 2023–24",
        "source": "Healthcare 2025;13(16):1945",
        "url": "https://www.mdpi.com/2227-9032/13/16/1945",
    },
    {
        "kind": "measured",
        "claim": "50% of referral letters carried no provisional diagnosis in the last Saudi completeness study (2007, n=330)",
        "source": "J Family Community Med 2007",
        "url": "https://doaj.org/article/cfee3017b738479fad3356e922afc576",
    },
    {
        "kind": "measured",
        "claim": "Eight of twelve authors of the 2025 SMARC analysis work at the MOH Medical Referrals Centre",
        "source": "Healthcare 2025;13(16):1945",
        "url": "https://www.mdpi.com/2227-9032/13/16/1945",
    },
    {
        "kind": "proposed",
        "claim": "Integrating AI tools for referral triage to optimize patient allocation",
        "source": "MOH Medical Referrals Centre recommendation, Healthcare 2025",
        "url": "https://www.mdpi.com/2227-9032/13/16/1945",
    },
    {
        "kind": "proposed",
        "claim": "Reviewer time saved and more consistent screening criteria across regions",
        "source": "Project claim — not yet measured in Saudi Arabia",
        "url": None,
    },
    {
        "kind": "limitation",
        "claim": "No post-2015 Saudi study measuring referral letter completeness was located",
        "source": "Project literature search, August 2026",
        "url": None,
    },
    {
        "kind": "limitation",
        "claim": "No Gulf or Arabic NLP referral-triage study exists in the world literature",
        "source": "Frontiers Health Services 2026 systematic review",
        "url": "https://www.frontiersin.org/journals/health-services/articles/10.3389/frhs.2026.1797583/full",
    },
    {
        "kind": "limitation",
        "claim": "No study anywhere demonstrates improved clinical outcomes from NLP referral triage",
        "source": "Frontiers Health Services 2026 systematic review",
        "url": "https://www.frontiersin.org/journals/health-services/articles/10.3389/frhs.2026.1797583/full",
    },
    {
        "kind": "limitation",
        "claim": "No public Saudi referral-letter corpus with completeness labels exists",
        "source": "SMARC data available only by institutional request",
        "url": "https://www.frontiersin.org/journals/public-health/articles/10.3389/fpubh.2024.1337138/full",
    },
]


def evidence_payload() -> dict:
    return {
        "items": EVIDENCE_ITEMS,
        "future_validation": [
            "Obtain appropriately governed SMARC/MOH referral data under research approval",
            "Publish a national minimum referral dataset (addresses G11)",
            "Establish clinician-labelled completeness and appropriateness ground truth",
            "Perform external validation and subgroup reporting before operational claims",
        ],
    }
