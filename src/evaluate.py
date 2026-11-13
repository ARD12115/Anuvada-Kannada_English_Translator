import argparse
import csv
from collections import defaultdict
from pathlib import Path

from src.engines.offline import OfflineEngine
from src.engines.online import OnlineEngine
from src.models import Lang
from src.utils.lang import detect


def evaluate_pairs(rows: list[dict[str, str]], engine) -> list[dict[str, object]]:
    from sacrebleu.metrics import BLEU, CHRF

    grouped: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for row in rows:
        source = row["source"]
        src: Lang = "kn" if row["direction"].upper() in {"KN-EN", "KN->EN"} else "en"
        tgt: Lang = "en" if src == "kn" else "kn"
        hypothesis = engine.translate(source, src, tgt)
        grouped[row["direction"]].append((hypothesis, row["reference"]))
    results = []
    for direction, pairs in sorted(grouped.items()):
        hypotheses, references = zip(*pairs)
        results.append(
            {
                "direction": direction,
                "n": len(pairs),
                "chrf": CHRF().corpus_score(list(hypotheses), [list(references)]).score,
                "bleu": BLEU().corpus_score(list(hypotheses), [list(references)]).score,
            }
        )
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate a translation engine against a fixed CSV pair set.")
    parser.add_argument("pairs", type=Path)
    parser.add_argument("--engine", choices=("online", "offline"), default="online")
    args = parser.parse_args()
    with args.pairs.open(encoding="utf-8-sig", newline="") as pairs_file:
        rows = list(csv.DictReader(pairs_file))
    required = {"direction", "source", "reference"}
    if not rows or not required.issubset(rows[0]):
        parser.error("CSV must contain direction, source, and reference columns.")
    engine = OnlineEngine() if args.engine == "online" else OfflineEngine()
    print(f"Engine: {args.engine}; examples: {len(rows)}")
    for result in evaluate_pairs(rows, engine):
        print(
            f"{result['direction']}: chrF={result['chrf']:.2f} "
            f"BLEU={result['bleu']:.2f} n={result['n']}"
        )


if __name__ == "__main__":
    main()
