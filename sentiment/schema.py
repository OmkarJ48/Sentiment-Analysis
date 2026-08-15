"""Shared result type every backend must return."""
from __future__ import annotations

from dataclasses import dataclass, field


VALID_LABELS = ("positive", "neutral", "negative")


@dataclass(frozen=True)
class SentimentResult:
    """Uniform output contract for all backends.

    `scores` always carries all three labels (even if the model is binary,
    the backend must map its output onto this shape) and must sum to ~1.0,
    so callers never have to special-case a missing neutral bucket.
    """

    label: str
    scores: dict[str, float]
    backend: str
    rationale: str = ""

    def __post_init__(self) -> None:
        if self.label not in VALID_LABELS:
            raise ValueError(f"label must be one of {VALID_LABELS}, got {self.label!r}")

        missing = set(VALID_LABELS) - set(self.scores)
        if missing:
            raise ValueError(f"scores missing keys: {sorted(missing)}")

        total = sum(self.scores.values())
        if not (0.98 <= total <= 1.02):
            raise ValueError(f"scores must sum to ~1.0, got {total:.4f}: {self.scores}")

    def to_dict(self) -> dict:
        return {
            "label": self.label,
            "scores": dict(self.scores),
            "backend": self.backend,
            "rationale": self.rationale,
        }
