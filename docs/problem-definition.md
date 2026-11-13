# Problem Definition (Rule 7) — Anuvada

**Statement:** Kannada-English Text Translation Assistant (Theme 3: AI for Everyday Life)
**Core theme for all stages:** Language accessibility for everyday digital and civic life in Karnataka

## Target users
1. Kannada-medium students, parents and visitors who find English notices and forms hard (primary).
2. Non-Kannada students and staff who need to read Kannada signs and notices.
3. College office / activity cells that publish bilingual notices (secondary).

## Existing challenges
- Notices, forms and signage mix Kannada and English; readers miss important details.
- General translation tools need internet, send text to external servers, and don't help with photos of signs or full notices.
- Domain words (HoD, CIE, semester, fee receipt) are often mistranslated.
- Nobody checks quality for local use, so users can't judge how much to trust results.

## Proposed solution
A local web app that translates Kannada <-> English from text, voice, signboard photos (OCR) and notices, with auto language detection, a campus glossary, an online engine for speed and an offline open-source engine (NLLB-200) for privacy and no-internet use. Users can edit OCR/voice output before translating and download bilingual notices. Quality is measured on a fixed test set.

## Expected outcomes
- A user reads an unfamiliar sign or notice in seconds.
- Offices produce bilingual notices with one download.
- Works without internet and without sending text out in offline mode.
- Reported translation quality (chrF/BLEU on ~30 pairs) and OCR accuracy (on 10-15 signboards), with honest limits.

## How it grows
Stage 1: understand text. Stage 2: spot scam or fraud messages in Kannada/Kanglish/English and explain them. Stage 3: understand Kannada documents, extract key information and answer questions. See roadmap.md.
