from sentiment.backends import vader_backend


def test_positive_text():
    result = vader_backend.analyze("I absolutely love this, it's fantastic!")
    assert result.label == "positive"
    assert result.backend == "vader"


def test_negative_text():
    result = vader_backend.analyze("This is terrible and I hate it.")
    assert result.label == "negative"


def test_neutral_text():
    result = vader_backend.analyze("The package arrives on Tuesday.")
    assert result.label == "neutral"


def test_scores_sum_to_one():
    result = vader_backend.analyze("A reasonably plain sentence.")
    assert abs(sum(result.scores.values()) - 1.0) < 0.02
