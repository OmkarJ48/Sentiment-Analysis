"""Builds data/sample_reviews.csv from templates — no network access needed.

Deterministic (fixed seed) so the committed CSV is reproducible. Re-run
this only if you want to regenerate/expand the dataset; the CSV itself is
what training actually reads.
"""
from __future__ import annotations

import csv
import random
from pathlib import Path

random.seed(42)

OUT_PATH = Path(__file__).resolve().parent.parent / "data" / "sample_reviews.csv"

NOUNS = [
    "movie", "product", "restaurant", "phone", "laptop", "hotel room",
    "customer service", "book", "app", "delivery", "course", "headphones",
    "vacation", "car", "software update", "meal", "concert", "game",
    "haircut", "flight",
]

POS_ADJ = [
    "amazing", "fantastic", "wonderful", "excellent", "outstanding",
    "brilliant", "superb", "delightful", "impressive", "great",
]
NEG_ADJ = [
    "terrible", "awful", "horrible", "disappointing", "dreadful",
    "mediocre", "poor", "frustrating", "useless", "unbearable",
]
NEUTRAL_FACT = [
    "arrived on Tuesday", "was scheduled for 3pm", "comes in three sizes",
    "is located downtown", "was released last month", "runs on batteries",
    "has a two year warranty", "was updated yesterday", "is 45 minutes long",
    "ships from the east coast",
]

POS_TEMPLATES = [
    "The {noun} was {pos_adj}, I loved every part of it.",
    "I really enjoyed the {noun}, {pos_adj} experience overall.",
    "{noun_cap} exceeded my expectations, truly {pos_adj}.",
    "Highly recommend the {noun}, it was {pos_adj}.",
    "What a {pos_adj} {noun}, I would do it again in a heartbeat.",
    "The {noun} was not bad at all, actually quite {pos_adj}.",
    "I can't stop thinking about how {pos_adj} the {noun} was.",
    "Best {noun} I've had in years, absolutely {pos_adj}.",
]

NEG_TEMPLATES = [
    "The {noun} was {neg_adj}, I regret it completely.",
    "I really disliked the {noun}, {neg_adj} experience overall.",
    "{noun_cap} fell short of my expectations, truly {neg_adj}.",
    "Would not recommend the {noun}, it was {neg_adj}.",
    "What a {neg_adj} {noun}, I would never do that again.",
    "The {noun} was not good at all, honestly {neg_adj}.",
    "I don't think the {noun} was worth it, quite {neg_adj}.",
    "Worst {noun} I've had in years, absolutely {neg_adj}.",
]

NEUTRAL_TEMPLATES = [
    "The {noun} {fact}.",
    "According to the listing, the {noun} {fact}.",
    "For reference, the {noun} {fact}.",
    "Note that the {noun} {fact}.",
    "The {noun} {fact}, nothing more to add.",
]


def build_rows() -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    for noun in NOUNS:
        for template in POS_TEMPLATES:
            adj = random.choice(POS_ADJ)
            text = template.format(noun=noun, noun_cap=noun.capitalize(), pos_adj=adj)
            rows.append((text, "positive"))
        for template in NEG_TEMPLATES:
            adj = random.choice(NEG_ADJ)
            text = template.format(noun=noun, noun_cap=noun.capitalize(), neg_adj=adj)
            rows.append((text, "negative"))
        for template in NEUTRAL_TEMPLATES:
            fact = random.choice(NEUTRAL_FACT)
            text = template.format(noun=noun, fact=fact)
            rows.append((text, "neutral"))

    random.shuffle(rows)
    return rows


def main() -> None:
    rows = build_rows()
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUT_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["text", "label"])
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows to {OUT_PATH}")


if __name__ == "__main__":
    main()
