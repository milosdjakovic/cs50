import pytest
from jar import Jar


def test_init():
    jar = Jar(7)

    assert jar.size == 0
    assert jar.capacity == 7

    with pytest.raises(ValueError):
        jar = Jar(0)


def test_deposit():
    jar = Jar(7)

    jar.deposit(4)
    assert jar.size == 4

    jar.deposit(2)
    assert jar.size == 6

    jar.deposit(1)
    assert jar.size == 7

    with pytest.raises(ValueError):
        jar.deposit(2)


def test_withdraw():
    jar = Jar(7)
    jar.deposit(7)

    jar.withdraw(4)
    assert jar.size == 3

    jar.withdraw(2)
    assert jar.size == 1

    jar.withdraw(1)
    assert jar.size == 0

    with pytest.raises(ValueError):
        jar.withdraw(2)


def test_str():
    jar = Jar(7)

    assert str(jar) == ""

    jar.deposit(5)
    assert str(jar) == "🍪🍪🍪🍪🍪"

    jar.withdraw(3)
    assert str(jar) == "🍪🍪"




