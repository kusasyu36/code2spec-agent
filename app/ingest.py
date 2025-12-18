from __future__ import annotations
from pathlib import Path

DEFAULT_EXCLUDE_DIRS = {
    ".git", ".venv", "node_modules", "__pycache__", ".pytest_cache", ".mypy_cache",
    "dist", "build", ".next", ".cache"
}
DEFAULT_EXCLUDE_EXTS = {
    ".png", ".jpg", ".jpeg", ".gif", ".pdf", ".zip", ".tar", ".gz", ".7z",
    ".pt", ".pth", ".ckpt", ".onnx", ".bin", ".dylib", ".so"
}

def iter_text_files(repo: Path,
                    exclude_dirs=DEFAULT_EXCLUDE_DIRS,
                    exclude_exts=DEFAULT_EXCLUDE_EXTS,
                    max_bytes: int = 400_000) -> list[Path]:
    repo = repo.resolve()
    files: list[Path] = []
    for p in repo.rglob("*"):
        if p.is_dir():
            continue
        rel_parts = set(p.relative_to(repo).parts)
        if any(d in rel_parts for d in exclude_dirs):
            continue
        if p.suffix.lower() in exclude_exts:
            continue
        try:
            if p.stat().st_size > max_bytes:
                continue
        except FileNotFoundError:
            continue
        files.append(p)
    return sorted(files)

def read_file(path: Path, encoding: str = "utf-8") -> str:
    try:
        return path.read_text(encoding=encoding, errors="ignore")
    except Exception:
        return ""