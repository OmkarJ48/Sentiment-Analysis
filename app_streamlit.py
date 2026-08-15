"""Streamlit UI for the free/local sentiment analysis prototype.

Run: streamlit run app_streamlit.py
"""
from __future__ import annotations

import streamlit as st

from sentiment.analyzer import analyze, available_backends
from sentiment.backends.sklearn_backend import MODEL_PATH

st.set_page_config(page_title="Sentiment Analysis (Free/Local)", page_icon="💬")

st.title("Sentiment Analysis — Free & Local")
st.caption(
    "Runs entirely offline: VADER (rule-based) or a TF-IDF + Logistic "
    "Regression model trained locally. No paid API, no API key."
)

backends = available_backends()
if not MODEL_PATH.exists():
    st.warning(
        f"No trained sklearn model found at `{MODEL_PATH.name}`. "
        "Run `python scripts/train_sklearn.py` to enable that backend. "
        "VADER works without it."
    )

backend = st.selectbox("Backend", backends, index=0)
text = st.text_area("Text to analyze", height=150, placeholder="Type or paste a sentence...")

if st.button("Analyze", type="primary") and text.strip():
    try:
        result = analyze(text, backend=backend)
    except FileNotFoundError as exc:
        st.error(str(exc))
    else:
        label_color = {"positive": "green", "neutral": "gray", "negative": "red"}[result.label]
        st.markdown(f"### Label: :{label_color}[{result.label.upper()}]")
        st.caption(result.rationale)
        st.bar_chart(result.scores)
        st.json(result.to_dict())
