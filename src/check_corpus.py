"""Report where each instrument's indexed text comes from, and flag any with none.

Provenance is decided by content, not location: fetch_corpus.py copies curated
extracts into data/text/ when an issuer blocks automated retrieval, so a file
sitting in data/text/ is not by itself evidence that the full document was
downloaded. Extracts declare themselves in their first line.
"""

import json
import pathlib

import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass
corpus = json.loads((ROOT / "data" / "corpus.json").read_text(encoding="utf-8"))

MARKER = "CURATED EXTRACT"

full, extract, missing = [], [], []

for doc in corpus["documents"]:
    body = ""
    for folder in ("text", "extracts"):
        path = ROOT / "data" / folder / f"{doc['id']}.txt"
        if path.exists():
            candidate = path.read_text(encoding="utf-8", errors="ignore")
            if len(candidate) > 200:
                body = candidate
                break
    if not body:
        missing.append(doc["id"])
    elif MARKER in body[:400]:
        extract.append((doc["id"], len(body)))
    else:
        full.append((doc["id"], len(body)))

print(f"Corpus: {len(corpus['documents'])} instruments\n")

print(f"  Full published text ......... {len(full)}")
for name, size in sorted(full):
    print(f"      {name:<22} {size:>9,} chars")

print(f"\n  Curated extract ............. {len(extract)}")
for name, size in sorted(extract):
    print(f"      {name:<22} {size:>9,} chars")

print(f"\n  No text at all .............. {len(missing)}")
for name in sorted(missing):
    print(f"      {name}   <-- indexed by metadata only")
if not missing:
    print("      (none - every instrument in the corpus has text)")

total = sum(s for _, s in full) + sum(s for _, s in extract)
print(f"\n  Indexed corpus: {total:,} characters across {len(full) + len(extract)} instruments.")
