# Spec (draft)

- Generated: 2025-12-19 15:29:36
- Repo: `/Users/s-kusaba/projects/code2spec-agent`
- Query: `argparse`

## Overview
This document is automatically generated from the repository contents.
It lists candidate important files and evidence snippets found by keyword search.

## Candidate important files (first 50)
- `.env.example`
- `README.md`
- `app/__init__.py`
- `app/ingest.py`
- `app/main.py`
- `app/render.py`
- `app/retrieve.py`
- `docs/spec.md`
- `requirements.txt`

## Evidence (keyword hits)
Each hit includes file path, line number, and surrounding context.

### Hit 1
- File: `app/main.py`
- Line: `2`

```text
      1: from __future__ import annotations
>>    2: import argparse
      3: from pathlib import Path
      4: 
```

### Hit 2
- File: `app/main.py`
- Line: `10`

```text
      8: 
      9: def main():
>>   10:     ap = argparse.ArgumentParser()
     11:     ap.add_argument("--repo", type=str, required=True, help="Target repo path (local)")
     12:     ap.add_argument("--out", type=str, default="docs/spec.md", help="Output spec path")
```

### Hit 3
- File: `docs/spec.md`
- Line: `18`

```text
     16: ## 3. 検索結果（Evidence）
     17: - `/Users/s-kusaba/projects/code2spec-agent/app/ingest.py`: from __future__ import annotations from pathlib import Path  DEFAULT_EXCLUDE_DIRS = {     ".git", ".venv", "node_modules", "__pycache__", ".pytest_cache", ".mypy_cache",     "dist", "build", ".next", ".cache" } DEFAU
>>   18: - `/Users/s-kusaba/projects/code2spec-agent/app/main.py`: from __future__ import annotations import argparse from pathlib import Path  from app.ingest import iter_text_files from app.retrieve import search_files from app.render import render_spec  def main():     ap = argpa
     19: - `/Users/s-kusaba/projects/code2spec-agent/app/render.py`: from __future__ import annotations from datetime import datetime from pathlib import Path  def render_spec(out_path: Path, repo_path: Path, top_files: list[str], hits: list[dict]) -> None:     out_path.parent.mkdir(p
     20: - `/Users/s-kusaba/projects/code2spec-agent/app/retrieve.py`: from __future__ import annotations from pathlib import Path import re  def search_files(files: list[Path], query: str, max_hits: int = 20) -> list[dict]:     pattern = re.compile(re.escape(query), re.IGNORECASE)     
```
