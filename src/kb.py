"""
Knowledge base: chunking, indexing and retrieval over the policy corpus.

Retrieval is TF-IDF over character and word n-grams. This is a deliberate
choice, not a limitation: the hackathon requires that every output be traceable
back to a document in the knowledge base, and a sparse lexical index makes that
traceability exact and reproducible. There is no API key, no network call at
query time, and no stochastic component - the same query returns the same
citations on any machine.

An optional dense encoder can be enabled if sentence-transformers is installed
(see USE_DENSE). Retrieval quality improves marginally; auditability does not.
"""

from __future__ import annotations

import json
import pathlib
import re
from dataclasses import dataclass, field

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

ROOT = pathlib.Path(__file__).resolve().parent.parent
CORPUS_PATH = ROOT / "data" / "corpus.json"
TEXT_DIR = ROOT / "data" / "text"
EXTRACT_DIR = ROOT / "data" / "extracts"

# A chunk must score at least this to count as governing a concern.
# Calibrated so that a document merely mentioning a topic in passing does not
# count as governing it. Raising it finds more gaps; lowering it finds fewer.
COVERAGE_THRESHOLD = 0.12


@dataclass
class Chunk:
    doc_id: str
    text: str
    ordinal: int


@dataclass
class Citation:
    doc_id: str
    title: str
    issuer: str
    url: str
    score: float
    snippet: str
    binding: bool
    scope_limit: str | None = None
    currency_warning: str | None = None


@dataclass
class ConcernFinding:
    node: str
    concern: str
    covered: bool
    citations: list[Citation] = field(default_factory=list)
    gap_id: str | None = None
    gap_statement: str | None = None
    # A duty can be imposed without any published method for demonstrating
    # compliance. That is not coverage in any useful sense, and it is the
    # substance of gap G4, so it is tracked separately from `covered`.
    method_published: bool = True
    scoped_out: list[str] = field(default_factory=list)


def _is_prose(chunk: str) -> bool:
    """Reject table-of-contents fragments, dot leaders and page furniture."""
    if chunk.count(".") > len(chunk) * 0.12:      # dot leaders
        return False
    words = [w for w in re.findall(r"[A-Za-z]{3,}", chunk)]
    if len(words) < 25:                            # too little actual language
        return False
    digits = sum(c.isdigit() for c in chunk)
    return digits <= len(chunk) * 0.20


def _split(text: str, target: int = 900, overlap: int = 150) -> list[str]:
    """Split on paragraph boundaries, packing to roughly `target` characters."""
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    chunks: list[str] = []
    buf = ""
    for para in paras:
        if len(buf) + len(para) + 2 <= target:
            buf = f"{buf}\n\n{para}" if buf else para
        else:
            if buf:
                chunks.append(buf)
            if len(para) <= target:
                buf = para
            else:
                for i in range(0, len(para), target - overlap):
                    piece = para[i : i + target]
                    if piece.strip():
                        chunks.append(piece.strip())
                buf = ""
    if buf:
        chunks.append(buf)
    prose = [c for c in chunks if _is_prose(c)]
    return prose or chunks or [text[:target]]


class KnowledgeBase:
    def __init__(self) -> None:
        self.corpus = json.loads(CORPUS_PATH.read_text(encoding="utf-8"))
        self.docs = {d["id"]: d for d in self.corpus["documents"]}
        self.node_concerns: dict[str, list[str]] = self.corpus["node_concerns"]
        self.concern_queries: dict[str, str] = self.corpus.get("concern_queries", {})
        self.known_gaps: dict[str, dict] = self.corpus["known_gaps"]
        self.chunks: list[Chunk] = []
        self._build()

    def _load_text(self, doc_id: str) -> str:
        for directory in (TEXT_DIR, EXTRACT_DIR):
            path = directory / f"{doc_id}.txt"
            if path.exists():
                body = path.read_text(encoding="utf-8")
                if len(body) > 200:
                    return body
        doc = self.docs[doc_id]
        return " ".join(
            [doc["title"], doc["issuer"], " ".join(doc.get("concerns", []))]
        )

    def _build(self) -> None:
        for doc_id in self.docs:
            for ordinal, piece in enumerate(_split(self._load_text(doc_id))):
                self.chunks.append(Chunk(doc_id=doc_id, text=piece, ordinal=ordinal))

        self.vectorizer = TfidfVectorizer(
            sublinear_tf=True,
            ngram_range=(1, 2),
            min_df=1,
            stop_words="english",
            lowercase=True,
        )
        self.matrix = self.vectorizer.fit_transform([c.text for c in self.chunks])

    # ------------------------------------------------------------------ query

    def search(
        self, query: str, k: int = 5, node: str | None = None
    ) -> list[Citation]:
        vec = self.vectorizer.transform([query])
        scores = cosine_similarity(vec, self.matrix).ravel()

        order = np.argsort(-scores)
        out: list[Citation] = []
        seen: set[str] = set()

        for idx in order:
            score = float(scores[idx])
            if score <= 0:
                break
            chunk = self.chunks[idx]
            doc = self.docs[chunk.doc_id]
            if node and node not in doc.get("nodes", []):
                continue
            if chunk.doc_id in seen:
                continue
            seen.add(chunk.doc_id)
            out.append(
                Citation(
                    doc_id=chunk.doc_id,
                    title=doc["title"],
                    issuer=doc["issuer"],
                    url=doc["url"],
                    score=round(score, 4),
                    snippet=chunk.text[:280].replace("\n", " ").strip(),
                    binding=bool(doc.get("binding")),
                    scope_limit=doc.get("scope_limit"),
                    currency_warning=doc.get("currency_warning"),
                )
            )
            if len(out) >= k:
                break
        return out

    # --------------------------------------------------------------- coverage

    def concern_finding(self, node: str, concern: str) -> ConcernFinding:
        """Decide whether a concern at a node is governed.

        Coverage rests on the curated `governs` list each instrument carries in
        corpus.json, not on retrieval score. That is deliberate. Once the real
        full-text documents are indexed, a single relevant sentence inside a
        190,000-character PDF no longer out-scores topically adjacent noise, so
        lexical similarity stopped being a sound test of whether an obligation
        exists. Worse, it failed in both directions: it missed Article 21 of the
        Law of Practicing Healthcare Professions on medical confidentiality, and
        it wrongly credited IS0303 with supplying a de-identification method it
        does not supply - which would have destroyed the central finding.

        So the legal judgement is made once, explicitly, in a data file any
        reviewer can open and challenge. Retrieval's job is to supply the
        supporting passage and its citation. An instrument only governs a
        concern if it is binding, not scope-limited, and declares the concern.
        """
        query = self.concern_queries.get(concern, concern.replace("_", " "))
        hits = [
            c
            for c in self.search(query, k=4, node=node)
            if c.score >= COVERAGE_THRESHOLD
        ]

        def applies(doc):
            return node in doc.get("nodes", []) and concern in doc.get("governs", [])

        governing = [
            i for i, doc in self.docs.items()
            if applies(doc) and doc.get("binding") and not doc.get("scope_limit")
        ]

        # Binding instruments that are squarely on point but whose own stated
        # scope excludes this system. Derived from the corpus for the same
        # reason coverage is: a top-k retrieval result is not evidence about
        # what an instrument's scope clause says.
        scoped_out = [
            i for i, doc in self.docs.items()
            if applies(doc) and doc.get("binding") and doc.get("scope_limit")
        ]

        # A governed duty with no published method of compliance.
        method_published = not any(
            concern in self.docs[i].get("governs_without_method", [])
            for i in governing
        )

        # Surface the governing instruments first, and make sure they appear
        # even when retrieval did not rank them - the citation should point at
        # the instrument that actually carries the obligation.
        cited = {c.doc_id for c in hits}
        for doc_id in governing:
            if doc_id not in cited:
                extra = self.search(query, k=8)
                found = next((c for c in extra if c.doc_id == doc_id), None)
                if found is None:
                    doc = self.docs[doc_id]
                    found = Citation(
                        doc_id=doc_id, title=doc["title"], issuer=doc["issuer"],
                        url=doc["url"], score=0.0,
                        snippet="(governs this concern by curated assignment; "
                                "no single passage retrieved for this query)",
                        binding=True, scope_limit=None,
                        currency_warning=doc.get("currency_warning"),
                    )
                hits.insert(0, found)
        hits.sort(key=lambda c: (c.doc_id not in governing, -c.score))

        gap_id = gap_statement = None
        for gid, gap in self.known_gaps.items():
            if gap["node"] == node and self._gap_matches(concern, gap["statement"]):
                gap_id, gap_statement = gid, gap["statement"]
                break

        return ConcernFinding(
            node=node,
            concern=concern,
            covered=bool(governing),
            citations=hits[:4],
            gap_id=gap_id,
            gap_statement=gap_statement,
            method_published=method_published,
            scoped_out=scoped_out,
        )

    @staticmethod
    def _gap_matches(concern: str, statement: str) -> bool:
        words = {w for w in concern.split("_") if len(w) > 3}
        lowered = statement.lower()
        aliases = {
            "deidentification": ("anonymis", "de-identif", "re-identif"),
            "reidentification": ("re-identif", "anonymis"),
            "anonymisation": ("anonymis",),
            "override": ("override", "human-in-the-loop"),
            "oversight": ("human-in-the-loop", "override"),
            "benchmarking": ("validat", "benchmark"),
            "certification": ("validat", "benchmark"),
            "validation": ("validat", "benchmark"),
            "disclosure": ("disclosure", "communicat"),
            "accessibility": ("accessibility", "dialect", "arabic"),
            "language": ("dialect", "arabic"),
            "residency": ("residen",),
            "referral": ("referral",),
            "provenance": ("electronic health records",),
            "security": ("cybersecurity",),
        }
        for word in words:
            if word in lowered:
                return True
            for key, needles in aliases.items():
                if word.startswith(key[:6]) and any(n in lowered for n in needles):
                    return True
        return False

    def node_report(self, node: str) -> list[ConcernFinding]:
        return [self.concern_finding(node, c) for c in self.node_concerns[node]]

    def full_report(self) -> dict[str, list[ConcernFinding]]:
        return {node: self.node_report(node) for node in self.node_concerns}
