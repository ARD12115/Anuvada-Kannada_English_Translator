#!/usr/bin/env bash
set -euo pipefail
source .venv/bin/activate
python -m streamlit run src/ui/app.py
