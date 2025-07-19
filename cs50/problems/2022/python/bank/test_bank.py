from bank import value

def test_value():
    assert value("HELLO") == "$0"
    assert value("hello") == "$0"
    assert value("Hi") == "$20"
    assert value("h") == "$20"
    assert value("how are you") == "$20"
    assert value("Whatzzup") == "$100"
    assert value("Lirili larila") == "$100"
