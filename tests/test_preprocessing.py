from sentiment.preprocessing import clean_text


def test_lowercases():
    assert clean_text("HELLO World") == "hello world"


def test_strips_urls():
    assert clean_text("check https://example.com now") == "check now"


def test_strips_punctuation_but_keeps_apostrophes():
    assert clean_text("This isn't bad, it's great!") == "this isn't bad it's great"


def test_collapses_whitespace():
    assert clean_text("too   many\n\nspaces") == "too many spaces"
