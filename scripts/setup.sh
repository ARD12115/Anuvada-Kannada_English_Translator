#!/usr/bin/env bash
set -euo pipefail
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cp -n .env.example .env || true
# Pre-download the offline model (~2.4 GB). Do this BEFORE the event, on good Wi-Fi.
python - <<'PY'
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
name = "facebook/nllb-200-distilled-600M"
AutoTokenizer.from_pretrained(name)
AutoModelForSeq2SeqLM.from_pretrained(name)
print("Offline model cached.")
PY
command -v tesseract >/dev/null || echo "WARNING: Tesseract not found. Install it plus the Kannada pack (see docs/onboarding.md)."
echo "Setup done. Run: streamlit run src/ui/app.py"
