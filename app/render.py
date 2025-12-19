from __future__ import annotations

from pathlib import Path
from datetime import datetime
from typing import Iterable

from app.retrieve import Hit

def render_spec(out: Path, repo: Path, top_files: list[str], hits: list[Hit], query: str) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines: list[str] = []

    lines += [
        "# Spec (draft)",
        "",
        f"- Generated: {now}",
        f"- Repo: `{repo}`",
        f"- Query: `{query}`",
        "",
        "## Overview",
        "This document is automatically generated from the repository contents.",
        "It lists candidate important files and evidence snippets found by keyword search.",
        "",
        "## Candidate important files (first 50)",
    ]
    for f in top_files:
        lines.append(f"- `{f}`")

    lines += [
        "",
        "## Evidence (keyword hits)",
        "Each hit includes file path, line number, and surrounding context.",
        "",
    ]

    if not hits:
        lines += [
            "_No hits found._",
            "",
        ]
    else:
        for i, h in enumerate(hits, start=1):
            lines += [
                f"### Hit {i}",
                f"- File: `{h.path}`",
                f"- Line: `{h.line_no}`",
                "",
                "```text",
                h.context,
                "```",
                "",
            ]

    out.write_text("\n".join(lines), encoding="utf-8")