# src/collect_pdfs.py
import json
from pathlib import Path

# assume `results` is the list returned by your search_papers call
# for demo, replace this by importing your search function and calling it
from semantic_search import search_papers
results = search_papers("deep learning", limit=20)

out_dir = Path("data/meta")
out_dir.mkdir(parents=True, exist_ok=True)
manifest_path = out_dir / "manifest.jsonl"

with manifest_path.open("w", encoding="utf-8") as f:
    for r in results:
        item = {
            "paperId": r.get("paperId"),
            "title": r.get("title"),
            "year": r.get("year"),
            "url": r.get("url"),
            "pdf_url": (r.get("openAccessPdf") or {}).get("url") or "",
            "open_status": (r.get("openAccessPdf") or {}).get("status"),
            "authors": [a.get("name") for a in r.get("authors", [])],
            "abstract": r.get("abstract") or ""
        }
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

print("Saved manifest to", manifest_path)
# quick summary
available = [r for r in results if (r.get("openAccessPdf") or {}).get("url")]
print("Direct PDF links found:", len(available))
for a in available[:10]:
    print("-", a.get("title"), "=>", (a.get("openAccessPdf") or {}).get("url"))
