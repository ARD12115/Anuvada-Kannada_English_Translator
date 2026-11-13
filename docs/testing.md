# Test Plan — Anuvada

## 1. Unit tests (pytest, mocked externals)
| Module | Cases |
|---|---|
| utils/lang | pure Kannada, pure English, mixed, digits/punctuation only, empty |
| utils/text | sentence split on `. ! ? ।`, keeps line breaks, very long text chunking |
| engines/online | calls provider with correct codes, retries once, raises `EngineUnavailableError` on failure |
| engines/offline | maps `kn->kan_Knda`, `en->eng_Latn`; lazy load; batch behaviour (mock model) |
| engines/router | preferred engine used; fallback triggered; `fell_back=True`; both fail -> friendly error |
| input/validators | wrong extension, wrong magic bytes, oversize, valid JPEG/PNG/PDF/TXT |
| input/ocr | missing Tesseract -> `OcrUnavailableError`; empty image -> empty result handled |
| input/documents | utf-8 .txt, text PDF, scanned PDF (empty) |
| glossary | term protected before, restored after; case handling |
| export | bilingual layout, UTF-8 safe |

## 2. Translation evaluation
1. Build `data/eval/pairs.csv` (id, direction, source, reference): ~15 KN->EN and ~15 EN->KN sentences covering notices, signs, campus terms, everyday phrases.
2. References written by Kannada-fluent teammates (note who).
3. Run `python -m src.evaluate data/eval/pairs.csv` for each engine; record chrF and BLEU.
4. List worst 5 sentences; add glossary entries or settings where it helps.
5. State the sample size when presenting results.

| Engine | Direction | chrF | BLEU | n |
|---|---|---|---|---|
| Online | KN->EN | | | 15 |
| Offline | KN->EN | | | 15 |

## 3. OCR evaluation
10-15 public signboard photos (clear, angled, low light). Hand-type ground truth, compute character accuracy, record which conditions fail.

## 4. Manual / demo tests
- Wi-Fi off: online fails -> offline fallback works.
- Tesseract missing: Signboard tab shows the banner, others still work.
- Mic denied: Voice tab explains and suggests typing.
- 6 MB image: rejected cleanly.
- Very long notice: progress shown, no crash.

## 5. Definition of done
All Must requirements pass, `pytest -q` green, evaluation table filled, two full rehearsals done.
