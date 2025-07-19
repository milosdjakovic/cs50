from numb3rs import validate

def test_validate():
    assert validate("1.2.3.4") == True
    assert validate("127.0.0.1") == True
    assert validate("255.255.255.0") == True
    assert validate("512.512.512.512") == False
    assert validate("1.300.3.4") == False
    assert validate("275.3.6.28") == False
    assert validate("1.2.3.1000") == False
    assert validate("cat") == False
