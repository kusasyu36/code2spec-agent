from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from app.retrieve import Hit
from app.llm import gemini_generate


def _clip(s: str, max_len: int) -> str:
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    if len(s) <= max_len:
        return s
    return s[: max_len - 1] + "…"


def summarize_hits(
    hits: list[Hit],
    query: str,
    model: str = "gemini-2.5-flash",
    max_hits: int = 12,
    max_context_chars_per_hit: int = 600,
) -> str:
    """
    Evidence（検索ヒット）を元に、LLMで“仕様書の概要”をMarkdownで作る。
    ルール：根拠のない推測は禁止。Evidenceに書いてあることだけを要約する。
    """
    if not hits:
        return "_(LLM summary) No evidence hits, so nothing to summarize._"

    use_hits = hits[:max_hits]

    # LLMに渡す「根拠」部分を作る（ファイル名と行番号つき）
    evidence_blocks: list[str] = []
    for i, h in enumerate(use_hits, start=1):
        ctx = _clip(h.context, max_context_chars_per_hit)
        evidence_blocks.append(
            f"[{i}] {h.path}:{h.line_no}\n{ctx}"
        )

    evidence_text = "\n\n".join(evidence_blocks)

    prompt = f"""
あなたはソフトウェア仕様書作成アシスタントです。
以下の Evidence（検索結果の抜粋）“だけ”を根拠に、仕様の要約を Markdown で書いてください。
根拠のない推測・捏造は禁止です。分からないことは「不明」と書いてください。

# 目的
- 検索クエリ: {query}

# 出力フォーマット（必ずこの見出しを使う）
## Summary
(このリポジトリが何をするものかを2〜4行)

## What it can do
- 箇条書き（最大6個）

## Key components
- 主要ファイルやモジュールを箇条書きで（最大8個）
- それぞれに根拠として (app/xxx.py:行番号) のように引用を付ける

## Notes / Limits
- 不明点、前提、限界を書いてください

# Evidence
{evidence_text}
""".strip()

    try:
        out = gemini_generate(prompt, model=model).strip()
        return out if out else "_(LLM summary) Empty response._"
    except Exception as e:
        # 失敗しても落とさない（デモとして“動き続ける”のが大事）
        return f"_(LLM summary unavailable: {type(e).__name__}: {e})_"
