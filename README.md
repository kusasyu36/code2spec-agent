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
