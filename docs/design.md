# Design Document — Anuvada UI/UX

Single-page Streamlit app with tabs. Large text for projectors and good Kannada rendering.

## 1. Principles
- Show the engine in use and whether a fallback happened.
- Always show source next to result.
- Let users fix OCR/voice output before translating.
- Fail softly: a broken tab never breaks the others.

## 2. Layout
```
+--------------------------------------------------------------+
| Anuvada  ಅನುವಾದ — Kannada <-> English                         |
| Engine: (o) Online  ( ) Offline      [privacy note]          |
+--------------------------------------------------------------+
| [Text] [Voice] [Signboard] [Notice] [History]                |
+----------------------------+---------------------------------+
| Input                      | Output                          |
| [ text area ]              | Detected: Kannada -> English    |
| Direction: Auto v          | [ translated text ]             |
| [ Translate ]              | [Copy] [Listen]                 |
+----------------------------+---------------------------------+
| Disclaimer: machine translation, check important text.       |
+--------------------------------------------------------------+
```

## 3. Tabs
| Tab | Elements | Notes |
|---|---|---|
| Text | `st.text_area`, direction selector (Auto/KN->EN/EN->KN), Translate, Copy, Listen | Auto-detect shown as a caption |
| Voice | `st.audio_input` (or recorder), language select, recognized text box (editable), Translate | Online-only badge |
| Signboard | `st.camera_input` / `st.file_uploader` (jpg/png), image preview, OCR text box (editable), Translate | If Tesseract missing: banner with fix steps |
| Notice | Paste area or upload .txt/.pdf, two columns (original / translation), Download bilingual .txt | Preserves line breaks |
| History | Table of session translations, CSV download, Clear | Session only |

## 4. States
| State | Behaviour |
|---|---|
| Empty | Placeholder: "Type or paste Kannada or English text" |
| Loading | Spinner with engine name; first offline run says "Loading model (first time is slow)" |
| Success | Output + engine badge |
| Fallback | Info bar: "Online engine unavailable, used offline model" |
| OCR empty | "No text found. Try a clearer, closer photo." |
| Mic/network error | Clear message and a suggestion to type instead |

## 5. Kannada rendering
Use Streamlit's default font stack (browser handles Kannada). For exported PDFs (if added) embed Noto Sans Kannada. Test with long conjunct characters.

## 6. Accessibility
Don't use color alone for status; add icons/text. Keep touch targets large for the camera flow on phones.

## 7. Copy
Short, plain English and Kannada labels for primary buttons if time permits (e.g. "Translate / ಅನುವಾದಿಸಿ").
