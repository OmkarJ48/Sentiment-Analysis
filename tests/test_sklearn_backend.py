import pytest

from sentiment.backends import sklearn_backend


@pytest.fixture(scope="module")
def trained_model():
    if not sklearn_backend.MODEL_PATH.exists():
        pytest.skip("model not trained; run scripts/train_sklearn.py first")
    return sklearn_backend.load_model()


def test_predicts_valid_label(trained_model):
    result = sklearn_backend.analyze("This was a wonderful experience.", model=trained_model)
    assert result.label in {"positive", "neutral", "negative"}
    assert result.backend == "sklearn_tfidf_logreg"


def test_scores_sum_to_one(trained_model):
    result = sklearn_backend.analyze("An average, unremarkable product.", model=trained_model)
    assert abs(sum(result.scores.values()) - 1.0) < 0.02


def test_missing_model_raises_clear_error(tmp_path):
    missing_path = tmp_path / "does_not_exist.joblib"
    with pytest.raises(FileNotFoundError):
        sklearn_backend.load_model(path=missing_path)
