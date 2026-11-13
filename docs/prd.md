# Product Requirements Document (PRD) — Anuvada

**Event:** CSE-HackSpark-2026, Stage 1 (Class-Level), 13 Nov 2026, 9:30 AM - 4:30 PM
**Theme:** 3 — AI for Everyday Life
**Problem statement:** Kannada-English Text Translation Assistant
**Core theme (Stages 1-3):** Language accessibility for everyday digital and civic life in Karnataka
**Team:** <Team name> · Leader: <name> · Mentor: <faculty guide>

## 1. Overview
Many people in coastal Karnataka read Kannada more comfortably than English, while campus notices, forms, apps and signage mix both. Anuvada translates Kannada <-> English from typed text, speech, signboard photos and campus notices, with an online engine for speed and an offline engine that works without internet.

## 2. Problem
- Notices, forms and signs are often in a language the reader finds hard.
- General translators handle Kannada unevenly and don't help with photos of signs or full notices.
- Many tools need internet and send your text to a server.
- Campus-specific words (HoD, semester, CIE, fee receipt) are often translated badly.

## 3. Target users
| User | Need |
|---|---|
| Kannada-medium students and visitors (primary) | Understand English notices, signs and forms quickly |
| Non-Kannada students and staff | Understand Kannada notices and signboards around campus and town |
| College office / TAC (secondary) | Publish bilingual notices with minimal effort |

## 4. Goals and non-goals
**Goals**
1. Working prototype: input -> detect -> translate -> output, in both directions.
2. Four input modes: text, voice, signboard photo, notice.
3. Works offline (NLLB) with online (Google) as the fast default.
4. Measured translation quality on a fixed test set (feeds Stage 2 test results).

**Non-goals (Stage 1)**
Accounts, database, mobile app, other Indian languages, Kanglish normalization, document layout preservation, claims of human-level quality.

## 5. User stories
- As a student, I type or paste text and get the translation with the language auto-detected.
- As a visitor, I photograph a Kannada signboard and read the English meaning.
- As a student, I speak a sentence and hear/read the translation.
- As a staff member, I paste a notice and download a bilingual version.
- As a user, I can switch to offline mode when the network is bad or the text is sensitive.

## 6. Functional requirements (MoSCoW)
| ID | Requirement | Priority |
|---|---|---|
| FR-1 | Text tab: auto-detect Kannada/English, translate, copy result | Must |
| FR-2 | Online engine (Google Translate via deep-translator) | Must |
| FR-3 | Long text split into sentences; line breaks preserved | Must |
| FR-4 | Friendly errors (empty input, engine failure, network down) | Must |
| FR-5 | Notice tab: paste or upload .txt/.pdf, side-by-side original/translation, bilingual download | Must |
| FR-6 | Signboard tab: upload/take photo, OCR (Kannada+English), translate | Should |
| FR-7 | Offline engine (NLLB-200 distilled 600M) with automatic fallback | Should |
| FR-8 | Voice tab: record, edit recognized text, translate | Should |
| FR-9 | "Listen" button (text-to-speech of result) | Could |
| FR-10 | Campus glossary applied before/after translation (e.g. HoD, CIE) | Should |
| FR-11 | History with CSV download (session only) | Could |
| FR-12 | Quality report (chrF/BLEU on test pairs) shown in the docs/slides | Should |

## 7. Non-functional requirements
- Text translation under 3 s online, under 10 s offline for a typical sentence (after model load).
- Offline model loaded once per session (`st.cache_resource`).
- Clear status of which engine is in use.
- Privacy notice when the online engine is selected.
- Works on a standard laptop CPU; no GPU needed.

## 8. Success metrics
| Metric | Target |
|---|---|
| chrF on 30-sentence eval set (offline engine) | Reported honestly; goal >= 45 |
| OCR character accuracy on 10-15 signboard photos | >= 80% on clear photos |
| Demo end-to-end without error | 100% on rehearsal |
| Fallback online -> offline triggers correctly | Pass with Wi-Fi off |

## 9. Rubric mapping (100 marks)
| Criterion | Marks | How we earn it |
|---|---|---|
| Problem Identification and Relevance | 15 | Local-language access in Mangaluru/Karnataka; Rule 7 definition |
| Innovation and Originality | 20 | Signboard OCR, offline engine, campus glossary, bilingual notice export (more than an API wrapper) |
| Technical Implementation | 25 | Engine abstraction with fallback, OCR pipeline, sentence splitting, evaluation |
| Working Prototype and Demonstration | 20 | Live demo of all tabs |
| Practical Feasibility and Impact | 10 | Free tools, offline, measured quality |
| Teamwork and Presentation | 10 | Roles + rehearsed 5-minute demo |

## 10. Deliverables (Stage 1)
Basic working prototype · source code · problem description · 5-minute demonstration.

## 11. Risks
| Risk | Mitigation |
|---|---|
| Looks like a thin Google Translate wrapper (Rule 8) | Lead the demo with signboard OCR, offline mode, glossary and the evaluation table |
| Venue Wi-Fi unreliable | Offline engine cached beforehand; auto-fallback |
| NLLB is 2.4 GB and slow on CPU | Download before the event; limit input length; show a spinner |
| Tesseract + Kannada pack missing on the demo laptop | Verify in setup; Signboard tab degrades with a clear message |
| Speech recognition needs internet | Mark Voice as online-only; keep it a Should |
| OCR errors on stylized signs | Allow editing the OCR text before translating |
| Machine translation mistakes | Show the source next to the output; add a quality disclaimer |

## 12. Stage roadmap (summary; details in roadmap.md)
Stage 1 translate -> Stage 2 detect scam/fraud messages in Kannada, Kanglish and English and explain warnings -> Stage 3 understand Kannada documents and extract key information with Q&A.
