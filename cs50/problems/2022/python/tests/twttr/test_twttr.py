from twttr import shorten

def test_shorten():
    assert shorten("hello") == "hll"
    assert shorten("AEwwIO") == "ww"
    assert shorten("555") == "555"
    assert shorten("...") == "..."
