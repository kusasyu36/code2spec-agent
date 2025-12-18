# code2spec-agent

Generate a draft spec (Markdown) from a code repository with evidence snippets.

## Quickstart
```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install python-dotenv rich

python -m app.main --repo . --out docs/spec.md --query "import"