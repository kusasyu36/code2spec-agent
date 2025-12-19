from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class Hit:
    path: str          # repo relative path
    line_no: int       # 1-based
    line: str          # matched line
    context: str       # surrounding lines (formatted)

def search_files(
    files: list[Path],
    query: str,
    *,
    max_hits: int = 20,
    context_lines: int = 2,
    repo_root: Path | None = None,
) -> list[Hit]:
    """
    Search keyword occurrences and return evidence with line number + context.
    """
    if not query:
        return []

    hits: list[Hit] = []
    for fp in files:
        try:
            text = fp.read_text(encoding="utf-8", errors="replace").splitlines()
        except Exception:
            continue

        for idx, line in enumerate(text):
            if query in line:
                start = max(0, idx - context_lines)
                end = min(len(text), idx + context_lines + 1)

                # 文脈を “行番号付き” で整形
                ctx_lines = []
                for j in range(start, end):
                    ln = j + 1
                    prefix = ">>" if j == idx else "  "
                    ctx_lines.append(f"{prefix} {ln:4d}: {text[j]}")

                rel = str(fp)
                if repo_root is not None:
                    try:
                        rel = str(fp.relative_to(repo_root))
                    except Exception:
                        pass

                hits.append(
                    Hit(
                        path=rel,
                        line_no=idx + 1,
                        line=line,
                        context="\n".join(ctx_lines),
                    )
                )
                if len(hits) >= max_hits:
                    return hits
    return hits