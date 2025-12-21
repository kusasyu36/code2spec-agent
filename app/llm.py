# app/llm.py
from __future__ import annotations

import os

from dotenv import load_dotenv
from google import genai

# このリポジトリ直下の .env を読み込む（GitHubには上げない）
load_dotenv()

def _get_api_key() -> str:
    # どちらの名前でもOKにする（あなたの状況に合わせる）
    return (
        os.getenv("GOOGLE_API_KEY")
        or os.getenv("GEMINI_API_KEY")
        or ""
    )

def gemini_generate(prompt: str, model: str = "gemini-2.5-flash") -> str:
    """
    Geminiにテキスト生成を依頼して、生成テキストを返す最小関数。
    - APIキーは .env から読む（GitHubに上げない）
    """
    api_key = _get_api_key()
    if not api_key:
        raise RuntimeError(
            "API key is missing. Put GOOGLE_API_KEY=... or GEMINI_API_KEY=... in .env"
        )

    client = genai.Client(api_key=api_key)
    resp = client.models.generate_content(model=model, contents=prompt)
    return getattr(resp, "text", "") or ""