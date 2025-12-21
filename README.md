# code2spec-agent

Generate a draft specification (`spec.md`) from an existing repository by:
1) listing important files (first 50 text files), and
2) collecting evidence by keyword search.

## Requirements
- Python 3.x

## Setup (macOS)
```bash
git clone https://github.com/kusasyu36/code2spec-agent.git
cd code2spec-agent
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

## LLM summary を付けて仕様書を作る（ターミナルだけ）

1) 仮想環境を有効化
source .venv/bin/activate

2) APIキー（どちらか1つの名前でOK）
このリポジトリ直下に .env を作って、どちらかを書いてください（GitHubには上げない）
GOOGLE_API_KEY=xxxx
または
GEMINI_API_KEY=xxxx

3) 生成（LLM要約つき）
OUT="$(mktemp /tmp/spec.XXXXXX)"
python -m app.main --repo . --query "argparse" --context 2 --out "$OUT" --llm
mkdir -p docs
cp "$OUT" docs/spec.md

4) 出力確認
sed -n '1,60p' docs/spec.md