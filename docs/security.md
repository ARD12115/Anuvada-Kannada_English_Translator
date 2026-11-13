# Security and Privacy — Anuvada

Translated text can include personal details (names, phone numbers, notices with student data). Treat input as sensitive.

## 1. Principles
1. Be honest about where text goes: the online engine and speech/TTS send data to Google services.
2. Offer a fully offline path (NLLB + Tesseract) for sensitive text.
3. Store nothing by default; history is session-only.

## 2. Threats and controls
| # | Threat | Control |
|---|---|---|
| 1 | Text leaves the device unexpectedly | Privacy note beside the engine selector; offline mode; Voice/Listen labeled "online" |
| 2 | Malicious uploads (images, PDFs, huge files) | Validate extension + magic bytes (JPEG `FF D8`, PNG `89 50 4E 47`, PDF `%PDF`); `MAX_UPLOAD_MB`; image dimension cap; page cap for PDFs |
| 3 | XSS via translated/OCR text | Render with `st.text`/`st.write`; no `unsafe_allow_html` on user content |
| 4 | Code injection | No `eval`/`exec`/`pickle` on user data; no shell calls with user strings (OCR via library API only) |
| 5 | PII in logs | Log events and counts only; never source or translated text |
| 6 | Temp audio/image files persist | Process from bytes; if temp files needed, delete in `finally` |
| 7 | Resource exhaustion (very long text, huge images) | Character cap, image resize, per-request timeout, one translation at a time per session |
| 8 | Supply chain / model integrity | Install from PyPI via requirements; load models only by official Hugging Face name; pin versions after it works |
| 9 | Secrets in repo | No keys needed in Stage 1; `.env` gitignored |
| 10 | Real photos/notices in git | `data/samples/*` gitignored; eval images must be your own or permitted |
| 11 | Mic access | Browser permission prompt only; no recording stored |

## 3. Responsible use
- Machine translation can be wrong. Show the disclaimer, show the source beside the result, and don't use it for legal, medical or emergency decisions.
- Photographing people or private documents without consent is not supported: signboards and public notices only.
- Be transparent about quality: report chrF/BLEU with the test-set size.

## 4. Pre-demo checklist
- [ ] `.env` and personal samples not in git
- [ ] `grep -rn unsafe_allow_html src` returns nothing for user content
- [ ] Upload validation tests pass
- [ ] Privacy note visible when online engine selected
- [ ] Demo uses public signboards and non-sensitive text

## 5. Future (Stage 2/3)
Rate limiting and caching if APIs/LLMs are added, PII redaction before sending to cloud models, consent flows, audit logging of model prompts without personal data, abuse handling for scam-detection content.
