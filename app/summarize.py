from __future__ import annotations

from typing import Any, Dict, List

from app.llm import gemini_generate


def summarize_with_evidence(
    repo_path: str,
    top_files: List[str],
    hits: List[Dict[str, Any]],
    model: str = "gemini-2.5-flash",
) -> str:
    """
    検索ヒット（Evidence）を元に、仕様の要約セクションをLLMで生成する。
    ルール：
    - Evidence に無いことは断定しない
    - 重要な主張は (根拠: file:Lx-Ly) の形で Evidence を根拠として添える
    """
    # LLMに渡すEvidenceを軽く整形（長くなりすぎ防止）
    compact_hits = []
    for h in hits[:20]:
        # 想定キー: path / line / snippet / context など（実装により違ってOK）
        path = str(h.get("path", ""))
        line = str(h.get("line", ""))
        snippet = (h.get("snippet") or h.get("text") or "").strip()
        if not snippet:
            # contextがある場合はそれを使う
            ctx = h.get("context") or ""
            snippet = str(ctx).strip()
        compact_hits.append({"path": path, "line": line, "snippet": snippet[:400]})

    prompt = f"""
あなたはソフトウェア仕様書作成の担当です。
対象リポジトリ: {repo_path}

候補主要ファイル:
{chr(10).join("- " + f for f in top_files[:50])}

Evidence（検索ヒット、最大20件）:
{compact_hits}

タスク:
- このEvidenceだけを根拠に「仕様の要約」を日本語で作ってください。
- 断定する文には必ず根拠を付けてください。
  形式: （根拠: app/main.py:L2 など）
- Evidenceに無いことは断定せず、推測なら「推測」と明記。

出力は Markdown で、以下の見出しを必ず含める：
## LLM要約
### 目的
### 入出力（CLI引数など）
### 処理の流れ
### 主要モジュール
### 制約・注意点
""".strip()

    return gemini_generate(prompt, model=model).strip()
