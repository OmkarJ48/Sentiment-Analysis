import pytest

from sentiment.schema import SentimentResult


def test_valid_result_constructs():
    result = SentimentResult(
        label="positive",
        scores={"positive": 0.7, "neutral": 0.2, "negative": 0.1},
        backend="vader",
    )
    assert result.label == "positive"
    assert result.to_dict()["backend"] == "vader"


def test_rejects_invalid_label():
    with pytest.raises(ValueError):
        SentimentResult(
            label="mixed",
            scores={"positive": 0.5, "neutral": 0.3, "negative": 0.2},
            backend="vader",
        )


def test_rejects_missing_score_key():
    with pytest.raises(ValueError):
        SentimentResult(
            label="positive",
            scores={"positive": 0.8, "negative": 0.2},
            backend="vader",
        )


def test_rejects_scores_not_summing_to_one():
    with pytest.raises(ValueError):
        SentimentResult(
            label="positive",
            scores={"positive": 0.9, "neutral": 0.9, "negative": 0.9},
            backend="vader",
        )
