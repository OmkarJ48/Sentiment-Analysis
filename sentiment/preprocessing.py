"""Text normalization shared by every backend that needs it.

VADER is tuned on raw text (it reads punctuation and casing as signal), so
it must never be run through this. Only the sklearn backend, which sees
each token as an opaque TF-IDF feature, needs cleaning.
"""
from __future__ import annotations

import re

_URL_RE = re.compile(r"https?://\S+|www\.\S+")
_NON_ALPHA_RE = re.compile(r"[^a-z0-9'\s]")
_WHITESPACE_RE = re.compile(r"\s+")


def clean_text(text: str) -> str:
    text = text.lower()
    text = _URL_RE.sub(" ", text)
    text = _NON_ALPHA_RE.sub(" ", text)
    text = _WHITESPACE_RE.sub(" ", text).strip()
    return text
