---
name: translation-eval
description: Runs and interprets translation quality evaluation (chrF/BLEU) and OCR accuracy for Anuvada.
---
# Procedure
1. Use `data/eval/pairs.csv` (columns: id, direction, source, reference).
2. Score each engine with sacrebleu: chrF (primary, better for Kannada's rich morphology) and BLEU (secondary).
3. Report per direction and overall; list the worst 5 sentences with source, output, reference.
4. For OCR: compare against hand-typed ground truth; report character accuracy per image.
5. Never claim quality beyond the size of the eval set; state the sample size.
