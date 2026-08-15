"""Single entry point callers use instead of importing a backend directly.

Keeps callers (the Streamlit app, tests, scripts) decoupled from which
backend answered — swap "vader" for "sklearn" without touching call sites.
"""
from __future__ import annotations

from typing import Callable

from sentiment.backends import sklearn_backend, vader_backend
from sentiment.schema import SentimentResult

_BACKENDS: dict[str, Callable[[str], SentimentResult]] = {
    "vader": vader_backend.analyze,
    "sklearn": sklearn_backend.analyze,
}


def available_backends() -> list[str]:
    return list(_BACKENDS)


def get_analyzer(backend: str) -> Callable[[str], SentimentResult]:
    try:
        return _BACKENDS[backend]
    except KeyError:
        raise ValueError(
            f"Unknown backend {backend!r}. Available: {available_backends()}"
        ) from None


def analyze(text: str, backend: str = "vader") -> SentimentResult:
    if not text or not text.strip():
        raise ValueError("text must be non-empty")
    return get_analyzer(backend)(text)
