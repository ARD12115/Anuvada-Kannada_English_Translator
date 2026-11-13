# Tickets — Stage 1 build plan

Window: 9:30 AM - 4:30 PM (~7 hours). If starting late, cut from the bottom (Could, then Should). Times are time-boxes.

| ID | Ticket | Priority | Est. | Done when |
|---|---|---|---|---|
| T-01 | Setup: venv, requirements, Streamlit shell with tabs | Must | 20m | App opens with 5 tabs |
| T-02 | Language detection + sentence splitter (+ tests) | Must | 30m | Kannada/English detected; line breaks kept |
| T-03 | Online engine + router + error handling | Must | 40m | KN<->EN works, friendly errors |
| T-04 | Text tab UI (direction, copy, engine badge) | Must | 30m | Matches design.md |
| T-05 | Notice tab: paste/.txt/.pdf, side-by-side, bilingual download | Must | 50m | File downloads with both languages |
| T-06 | Glossary (20-30 campus terms) | Should | 25m | Terms translate consistently |
| T-07 | Offline engine (NLLB) + automatic fallback | Should | 50m | Works with Wi-Fi off |
| T-08 | Signboard tab: validation, OCR, editable text, translate | Should | 55m | Sample sign -> English |
| T-09 | Voice tab (STT, editable, translate) | Should | 35m | Spoken sentence translated |
| T-10 | Evaluation: 30 pairs + 10-15 signboards, results table | Should | 50m | Table in slides |
| T-11 | Listen (TTS), History + CSV | Could | 30m | Buttons work |
| T-12 | Slides/problem description + demo rehearsal x2 | Must | 45m | Under 5 minutes |

## Suggested split (3-4 people)
- A: T-03, T-07 (engines, router)
- B: T-08, T-09 (OCR, voice)
- C: T-02, T-05, T-06 (text utils, notice, glossary)
- D: T-01, T-04, then T-10 and T-12 (UI, evaluation, slides)

## Cut line
Minimum demo-able Stage 1: T-01 to T-05 + T-12. Add T-07 and T-08 first for the best impression.

## Pre-event homework (if allowed)
Install Tesseract + Kannada pack and cache the NLLB model beforehand (large downloads). Write code during the event.
