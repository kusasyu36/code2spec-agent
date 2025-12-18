from __future__ import annotations
import argparse
from pathlib import Path

from app.ingest import iter_text_files
from app.retrieve import search_files
from app.render import render_spec

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", type=str, required=True, help="Target repo path")
    ap.add_argument("--out", type=str, default="docs/spec.md", help="Output spec path")
    ap.add_argument("--query", type=str, default="TODO", help="Search keyword for evidence")
    args = ap.parse_args()

    repo = Path(args.repo).expanduser().resolve()
    out = Path(args.out).expanduser().resolve()

    files = iter_text_files(repo)
    top_files = [str(p.relative_to(repo)) for p in files[:50]]

    hits = search_files(files, args.query, max_hits=20)
    render_spec(out, repo, top_files, hits)

    print(f"[OK] spec generated: {out}")

if __name__ == "__main__":
    main()