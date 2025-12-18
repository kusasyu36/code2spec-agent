from __future__ import annotations
from datetime import datetime
from pathlib import Path

def render_spec(out_path: Path, repo_path: Path, top_files: list[str], hits: list[dict]) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)

    lines = []
    lines.append(f"# 仕様書（自動生成）")
    lines.append("")
    lines.append(f"- 対象リポジトリ: `{repo_path}`")
    lines.append(f"- 生成日時: {datetime.now().isoformat(timespec='seconds')}")
    lines.append("")
    lines.append("## 1. 目的")
    lines.append("このドキュメントは、コードベースをスキャンして推定した仕様のたたき台です。")
    lines.append("")
    lines.append("## 2. 主要ファイル（候補）")
    for p in top_files[:10]:
        lines.append(f"- `{p}`")
    lines.append("")
    lines.append("## 3. 検索結果（Evidence）")
    if not hits:
        lines.append("- （ヒットなし）")
    else:
        for h in hits:
            lines.append(f"- `{h['path']}`: {h['snippet']}")
    lines.append("")
    lines.append("## 4. Mermaid（仮）")
    lines.append("```mermaid")
    lines.append("flowchart LR")
    lines.append("  User-->CLI[code2spec CLI]")
    lines.append("  CLI-->Scan[Scan repo]")
    lines.append("  Scan-->Search[Search]")
    lines.append("  Search-->Spec[Generate spec.md]")
    lines.append("```")
    lines.append("")

    out_path.write_text("\n".join(lines), encoding="utf-8")