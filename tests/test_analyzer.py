import pytest

from sentiment.analyzer import analyze, available_backends, get_analyzer


def test_available_backends_lists_both():
    assert set(available_backends()) == {"vader", "sklearn"}


def test_unknown_backend_raises():
    with pytest.raises(ValueError):
        get_analyzer("gpt4")


def test_empty_text_raises():
    with pytest.raises(ValueError):
        analyze("   ", backend="vader")


def test_analyze_dispatches_to_vader():
    result = analyze("Great news, I'm thrilled!", backend="vader")
    assert result.backend == "vader"
