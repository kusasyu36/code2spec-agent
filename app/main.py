from __future__ import annotations
import argparse
from pathlib import Path

from app.ingest import iter_text_files, DEFAULT_TEXT_EXTS, DEFAULT_EXCLUDE_DIRS
from app.retrieve import search_files
from app.render import render_spec

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", type=str, required=True, help="Target repo path (local)")
    ap.add_argument("--out", type=str, default="docs/spec.md", help="Output spec path")
    ap.add_argument("--query", type=str, default="TODO", help="Search keyword for evidence")

    ap.add_argument("--context", type=int, default=2, help="Context lines around each hit")
    ap.add_argument("--max-hits", type=int, default=20, help="Max number of evidence hits")
    ap.add_argument("--max-files", type=int, default=5000, help="Max files to scan")
    ap.add_argument("--max-bytes", type=int, default=1_000_000, help="Max file size to read")

    # デフォルトは「よくあるテキスト拡張子」に限定（速い）
    ap.add_argument("--all-exts", action="store_true", help="Scan any file that decodes as UTF-8 (slower)")
    args = ap.parse_args()

    repo = Path(args.repo).expanduser().resolve()
    out = Path(args.out).expanduser().resolve()

    allow_exts = None if args.all_exts else set(DEFAULT_TEXT_EXTS)

    files = iter_text_files(
        repo,
        max_files=args.max_files,
        max_bytes=args.max_bytes,
        exclude_dirs=set(DEFAULT_EXCLUDE_DIRS),
        allow_exts=allow_exts,
    )

    top_files = [str(p.relative_to(repo)) for p in files[:50]]

    hits = search_files(
        files,
        args.query,
        max_hits=args.max_hits,
        context_lines=args.context,
        repo_root=repo,
    )

    render_spec(out, repo, top_files, hits, query=args.query)
    print(f"[OK] spec generated: {out}")

if __name__ == "__main__":
    main()