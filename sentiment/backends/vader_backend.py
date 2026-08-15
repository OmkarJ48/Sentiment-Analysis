"""Rule-based backend: VADER, via the vaderSentiment package.

Zero training, zero download, instant startup. This is the offline floor
every other backend is measured against.
"""
from __future__ import annotations

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from sentiment.schema import SentimentResult

_analyzer = SentimentIntensityAnalyzer()


def analyze(text: str) -> SentimentResult:
    polarity = _analyzer.polarity_scores(text)

    compound = polarity["compound"]
    if compound >= 0.05:
        label = "positive"
    elif compound <= -0.05:
        label = "negative"
    else:
        label = "neutral"

    return SentimentResult(
        label=label,
        scores={
            "positive": polarity["pos"],
            "neutral": polarity["neu"],
            "negative": polarity["neg"],
        },
        backend="vader",
        rationale=f"compound={compound:.3f}",
    )
