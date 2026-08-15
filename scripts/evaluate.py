"""Benchmarks every backend on two sets and prints a comparison table:

  1. data/holdout_test.csv  - template-generated, same distribution as
     training data. Expect near-perfect scores here; it mostly proves the
     pipeline works, not that the model generalizes.
  2. data/sanity_check.csv  - hand-written, out-of-distribution sentences
     (including negation and hedged/mixed cases) neither backend has seen.
     This is the number that actually means something.

Usage: python scripts/evaluate.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
from sklearn.metrics import accuracy_score, f1_score

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sentiment.analyzer import analyze, available_backends

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

DATASETS = {
    "holdout (in-distribution)": DATA_DIR / "holdout_test.csv",
    "sanity_check (out-of-distribution)": DATA_DIR / "sanity_check.csv",
}


def evaluate_backend(backend: str, df: pd.DataFrame) -> tuple[float, float]:
    predictions = []
    for text in df["text"]:
        try:
            predictions.append(analyze(text, backend=backend).label)
        except FileNotFoundError as exc:
            print(f"  skipping {backend}: {exc}")
            return float("nan"), float("nan")

    acc = accuracy_score(df["label"], predictions)
    f1 = f1_score(df["label"], predictions, average="macro")
    return acc, f1


def main() -> None:
    for dataset_name, path in DATASETS.items():
        if not path.exists():
            print(f"skipping {dataset_name}: {path} not found (run train_sklearn.py first)")
            continue

        df = pd.read_csv(path)
        print(f"\n=== {dataset_name} ({len(df)} examples) ===")
        print(f"{'backend':<25}{'accuracy':<12}{'macro F1':<12}")
        for backend in available_backends():
            acc, f1 = evaluate_backend(backend, df)
            print(f"{backend:<25}{acc:<12.3f}{f1:<12.3f}")


if __name__ == "__main__":
    main()
