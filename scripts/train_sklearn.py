"""Trains the TF-IDF + Logistic Regression backend and saves it to disk.

Usage: python scripts/train_sklearn.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import joblib
import pandas as pd
from sklearn.model_selection import train_test_split

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sentiment.backends.sklearn_backend import MODEL_PATH, build_pipeline

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "sample_reviews.csv"


def main() -> None:
    df = pd.read_csv(DATA_PATH)

    train_df, test_df = train_test_split(
        df, test_size=0.2, random_state=42, stratify=df["label"]
    )

    pipeline = build_pipeline()
    pipeline.fit(train_df["text"], train_df["label"])

    train_acc = pipeline.score(train_df["text"], train_df["label"])
    test_acc = pipeline.score(test_df["text"], test_df["label"])
    print(f"train accuracy: {train_acc:.3f}")
    print(f"test accuracy:  {test_acc:.3f}")

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)
    print(f"saved model to {MODEL_PATH}")

    test_df.to_csv(DATA_PATH.parent / "holdout_test.csv", index=False)
    print(f"saved holdout split to {DATA_PATH.parent / 'holdout_test.csv'}")


if __name__ == "__main__":
    main()
