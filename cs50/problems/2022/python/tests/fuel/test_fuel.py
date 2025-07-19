import pytest
from fuel import convert, gauge

def test_convert():
    assert convert("3/4") == 75
    assert convert("1/3") == 33
    assert convert("2/3") == 67
    assert convert("1/1") == 100
    with pytest.raises(ZeroDivisionError):
        convert("0/0")
    with pytest.raises(ValueError):
        convert("aaa-bbb")
    with pytest.raises(ValueError):
        convert("aaa/bbb")
    with pytest.raises(ValueError):
        convert("3/2")
    with pytest.raises(ValueError):
        convert("3.5/2")
    with pytest.raises(ValueError):
        convert("60-20")

def test_gauge():
    assert gauge(100) == "F"
    assert gauge(99) == "F"
    assert gauge(1) == "E"
    assert gauge(0) == "E"
    assert gauge(98) == "98%"
    assert gauge(2) == "2%"
    assert gauge(55) == "55%"
