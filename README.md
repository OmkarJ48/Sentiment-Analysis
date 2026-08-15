# Sentiment Analysis — Free & Local Prototype

A working sentiment analysis prototype that runs entirely offline, with
**no paid LLM API and no API key required**. Two backends, one contract:

- **VADER** — rule-based, zero training, zero download, instant startup.
- **TF-IDF + Logistic Regression** (scikit-learn) — trained locally on a
  bundled dataset, persisted with `joblib`.

Both return the same `SentimentResult` shape (`positive`/`neutral`/`negative`
label + a 3-way probability distribution that must sum to ~1.0), so the app
and tests never need to know which backend answered.

## Quickstart

```bash
pip install -r requirements.txt

# Train the sklearn backend (VADER needs no training step)
python scripts/train_sklearn.py

# Launch the UI
streamlit run app_streamlit.py
```

Open the URL Streamlit prints, type a sentence, pick a backend, hit Analyze.

## Project layout

```
sentiment/                  # the actual library — no UI imports in here
  schema.py                 # SentimentResult, validated on construction
  preprocessing.py          # text cleaning (used by sklearn backend only)
  analyzer.py                # factory: analyze(text, backend="vader"|"sklearn")
  backends/
    vader_backend.py        # rule-based, offline, no training
    sklearn_backend.py      # TF-IDF + LogisticRegression, needs training first

scripts/
  generate_dataset.py       # builds data/sample_reviews.csv (deterministic, offline)
  train_sklearn.py          # trains + saves models/sklearn_tfidf_logreg.joblib
  evaluate.py                # benchmarks both backends, prints accuracy/F1

data/
  sample_reviews.csv        # 420 template-generated, labeled examples (training data)
  holdout_test.csv           # 20% split held out from training, same distribution
  sanity_check.csv           # 35 hand-written, out-of-distribution sentences

app_streamlit.py            # the UI — talks to sentiment/ only through analyzer.py
tests/                      # pytest suite for schema, preprocessing, both backends
legacy/                     # original Tkinter/VADER prototype, kept for reference
```

## Why two backends

VADER is the offline floor: no training, handles negation reasonably
("not bad" reads positive), but it's a fixed lexicon — it doesn't learn from
your data and it doesn't understand domain-specific words.

The sklearn backend is trainable: point `data/sample_reviews.csv` at your
actual data and re-run `train_sklearn.py` to get a model that reflects your
domain's vocabulary. The tradeoff is it's only as good as the training data —
see the benchmark below for exactly how that plays out.

## Benchmark (run it yourself: `python scripts/evaluate.py`)

Two evaluation sets, on purpose:

1. **holdout (in-distribution)** — 84 examples from the same templates the
   model trained on. This mostly proves the pipeline works, not that the
   model generalizes.
2. **sanity_check (out-of-distribution)** — 35 hand-written sentences,
   including negation ("not bad at all") and hedged/mixed opinions, that
   neither backend has seen.

Latest run on this repo:

| Dataset | Backend | Accuracy | Macro F1 |
|---|---|---|---|
| holdout (in-distribution) | vader | 0.976 | 0.976 |
| holdout (in-distribution) | sklearn | 1.000 | 1.000 |
| sanity_check (out-of-distribution) | vader | 0.686 | 0.672 |
| sanity_check (out-of-distribution) | sklearn | 0.543 | 0.540 |

**Read this honestly, not optimistically.** The sklearn model hits 100% on
data drawn from its own templates because it's largely memorizing adjective
vocabulary ("amazing", "terrible", ...) — that number is not evidence of
real-world accuracy. On genuinely unseen phrasing, VADER actually
outperforms it. That's the expected failure mode of a small model trained on
synthetic, template-generated text with limited lexical diversity: it
overfits fast. The fix isn't a bigger model, it's more (and more diverse)
labeled data — swap `data/sample_reviews.csv` for real labeled examples from
your actual domain and retrain.

## Testing

```bash
python -m pytest -q
```

19 tests covering the `SentimentResult` validation contract, text
preprocessing, both backends, and the analyzer factory. The sklearn tests
skip gracefully if `train_sklearn.py` hasn't been run yet.

## Extending this

- **More/better training data** is the single highest-leverage change — see
  the benchmark section above.
- **A third backend** (e.g. a local Hugging Face transformer such as
  `distilbert-base-uncased-finetuned-sst-2-english`, run fully offline after
  a one-time model download — still no paid API) can be added as
  `sentiment/backends/transformer_backend.py` and registered in
  `sentiment/analyzer.py`'s `_BACKENDS` dict; nothing else needs to change,
  by design.
- **Voice/image input**: not implemented here. If added, ingest code should
  normalize to text and hand off to `sentiment.analyzer.analyze()` — the
  core analysis logic should never need to know where the text came from.

## Legacy prototype

`legacy/` holds the original standalone scripts this project started as: a
Tkinter GUI (`app.py`) wrapping VADER directly, plus assorted experiments
(`OLDCODE.py`, `trial.py`, `sentimentchatbot.py`,
`Voice_based_Sentiment_Analysis.py`, etc.). They're kept for reference but
are superseded by `sentiment/` + `app_streamlit.py` above.
