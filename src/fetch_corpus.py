"""
Download the policy corpus and extract text.

Some issuers block automated access (SDAIA's main host runs a WAF; NHIC
intermittently robots-blocks). Those documents are marked fetchable: false in
corpus.json and are represented by curated extracts in data/extracts/ instead,
so the knowledge base is complete either way. Which documents were fetched
live and which came from extracts is recorded in the manifest, because the
provenance matters for an audit.
"""

import json
import pathlib
import sys
import time

import requests
from pypdf import PdfReader

ROOT = pathlib.Path(__file__).resolve().parent.parent
CORPUS = ROOT / "data" / "corpus.json"
RAW = ROOT / "data" / "raw"
TEXT = ROOT / "data" / "text"
EXTRACTS = ROOT / "data" / "extracts"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0 Safari/537.36"
}


def pdf_to_text(path: pathlib.Path) -> str:
    try:
        reader = PdfReader(str(path))
        return "\n".join((page.extract_text() or "") for page in reader.pages)
    except Exception as exc:  # noqa: BLE001
        print(f"    ! text extraction failed: {exc}")
        return ""


def fetch(doc: dict) -> tuple[str, str]:
    """Return (text, provenance)."""
    doc_id = doc["id"]
    extract_path = EXTRACTS / f"{doc_id}.txt"

    if doc.get("fetchable"):
        raw_path = RAW / f"{doc_id}.pdf"
        if raw_path.exists():
            text = pdf_to_text(raw_path)
            if len(text) > 500:
                return text, "cached"
        try:
            resp = requests.get(doc["url"], headers=HEADERS, timeout=60)
            resp.raise_for_status()
            raw_path.write_bytes(resp.content)
            text = pdf_to_text(raw_path)
            if len(text) > 500:
                print(f"    fetched {len(resp.content):,} bytes, {len(text):,} chars")
                return text, "fetched"
            print("    ! fetched but no extractable text (scanned or JS-rendered)")
        except Exception as exc:  # noqa: BLE001
            print(f"    ! fetch failed: {exc}")

    if extract_path.exists():
        print("    using curated extract")
        return extract_path.read_text(encoding="utf-8"), "extract"

    print("    ! NO TEXT AVAILABLE - document will be indexed by metadata only")
    return "", "metadata_only"


def main() -> None:
    for directory in (RAW, TEXT, EXTRACTS):
        directory.mkdir(parents=True, exist_ok=True)

    corpus = json.loads(CORPUS.read_text(encoding="utf-8"))
    manifest = []

    for doc in corpus["documents"]:
        print(f"[{doc['id']}] {doc['title'][:70]}")
        text, provenance = fetch(doc)

        # Only fetched text is written here. Copying a curated extract into
        # data/text/ would shadow data/extracts/ at query time, so a later
        # correction to the extract would be silently ignored - which is
        # exactly what happened once. Extracts are read from their own
        # directory and are never duplicated.
        if text and provenance in ("fetched", "cached"):
            (TEXT / f"{doc['id']}.txt").write_text(text, encoding="utf-8")
        else:
            stale = TEXT / f"{doc['id']}.txt"
            if stale.exists():
                stale.unlink()
        manifest.append(
            {
                "id": doc["id"],
                "provenance": provenance,
                "chars": len(text),
                "url": doc["url"],
            }
        )
        if provenance == "fetched":
            time.sleep(1)  # be polite to government hosts

    (ROOT / "data" / "manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )

    fetched = sum(1 for m in manifest if m["provenance"] in ("fetched", "cached"))
    print(f"\n{fetched}/{len(manifest)} documents with full text.")
    print(f"Manifest written to data/manifest.json")


if __name__ == "__main__":
    sys.exit(main())
