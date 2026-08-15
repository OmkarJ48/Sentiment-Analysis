"""Trainable backend: TF-IDF + Logistic Regression, scikit-learn only.

No pretrained weights to download — the model is trained locally from
data/sample_reviews.csv by scripts/train_sklearn.py and persisted with
joblib. This backend is unusable until that script has been run once.
"""
from __future__ import annotations

from pathlib import Path

import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer

from sentiment.preprocessing import clean_text
from sentiment.schema import SentimentResult

MODEL_PATH = Path(__file__).resolve().parent.parent.parent / "models" / "sklearn_tfidf_logreg.joblib"

_model_cache: dict[Path, Pipeline] = {}


def build_pipeline() -> Pipeline:
    return Pipeline(
        [
            (
                "tfidf",
                TfidfVectorizer(
                    preprocessor=clean_text,
                    ngram_range=(1, 2),
                    min_df=2,
                    sublinear_tf=True,
                ),
            ),
            (
                "clf",
                LogisticRegression(
                    max_iter=1000,
                    class_weight="balanced",
                ),
            ),
        ]
    )


def load_model(path: Path = MODEL_PATH) -> Pipeline:
    if path in _model_cache:
        return _model_cache[path]
    if not path.exists():
        raise FileNotFoundError(
            f"No trained model at {path}. Run `python scripts/train_sklearn.py` first."
        )
    model = joblib.load(path)
    _model_cache[path] = model
    return model


def analyze(text: str, model: Pipeline | None = None) -> SentimentResult:
    model = model or load_model()
    proba = model.predict_proba([text])[0]
    scores = dict(zip(model.classes_, (float(p) for p in proba)))
    label = max(scores, key=scores.get)

    return SentimentResult(
        label=label,
        scores=scores,
        backend="sklearn_tfidf_logreg",
        rationale=f"p({label})={scores[label]:.3f}",
    )
