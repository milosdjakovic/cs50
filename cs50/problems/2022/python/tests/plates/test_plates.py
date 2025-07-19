from plates import is_valid

def test_plates():
    assert is_valid("ML42") == True
    assert is_valid("FOUR44") == True
    assert is_valid("RARELY") == True
    assert is_valid("CS05") == False
    assert is_valid("42") == False
    assert is_valid("ML42D2") == False
    assert is_valid("AA.AAA") == False
    assert is_valid("A") == False
    assert is_valid("LONGWORD") == False
