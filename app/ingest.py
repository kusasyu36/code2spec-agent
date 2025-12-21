from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

DEFAULT_EXCLUDE_DIRS = {
    ".git", ".venv", "venv", "__pycache__", ".pytest_cache", ".mypy_cache",
    "node_modules", "dist", "build", ".DS_Store",
    "docs",
}

DEFAULT_TEXT_EXTS = {
    ".py", ".md", ".txt", ".json", ".yaml", ".yml", ".toml",
    ".ini", ".cfg", ".sh", ".bash", ".zsh", ".js", ".ts",
    ".html", ".css", ".env", ".example"
}

def _is_under_excluded_dir(path: Path, repo: Path, exclude_dirs: set[str]) -> bool:
    try:
        rel = path.relative_to(repo)
    except ValueError:
        return True
    parts = set(rel.parts)
    return any(d in parts for d in exclude_dirs)

def _looks_text_file(path: Path, max_bytes: int, allow_exts: set[str] | None) -> bool:
    if not path.is_file():
        return False
    if path.stat().st_size > max_bytes:
        return False
    if allow_exts is not None and path.suffix.lower() not in allow_exts:
        return False
    # 軽いテキスト判定：先頭だけUTF-8で読めるか
    try:
        with path.open("rb") as f:
            head = f.read(4096)
        head.decode("utf-8")
        return True
    except Exception:
        return False

def iter_text_files(
    repo: Path,
    *,
    max_files: int = 5000,
    max_bytes: int = 1_000_000,
    exclude_dirs: set[str] | None = None,
    allow_exts: set[str] | None = None,
) -> list[Path]:
    """
    Collect text-like files under repo.
    - exclude_dirs: directories to skip
    - allow_exts: if provided, only these extensions are included
    """
    repo = repo.resolve()
    exclude_dirs = exclude_dirs or set(DEFAULT_EXCLUDE_DIRS)
    allow_exts = allow_exts  # None = accept any ext (but still text-decodable)

    results: list[Path] = []
    for p in repo.rglob("*"):
        if len(results) >= max_files:
            break
        if _is_under_excluded_dir(p, repo, exclude_dirs):
            continue
        if _looks_text_file(p, max_bytes=max_bytes, allow_exts=allow_exts):
            results.append(p)

    # 安定して再現できるようにソート
    results.sort()
    return results