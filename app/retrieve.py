from __future__ import annotations
from pathlib import Path
import re

def search_files(files: list[Path], query: str, max_hits: int = 20) -> list[dict]:
    pattern = re.compile(re.escape(query), re.IGNORECASE)
    hits = []
    for f in files:
        text = f.read_text(encoding="utf-8", errors="ignore")
        if pattern.search(text):
            # 先頭付近だけ抜粋
            idx = pattern.search(text).start()
            start = max(0, idx - 120)
            end = min(len(text), idx + 200)
            snippet = text[start:end].replace("\n", " ")
            hits.append({"path": str(f), "snippet": snippet})
        if len(hits) >= max_hits:
            break
    return hits