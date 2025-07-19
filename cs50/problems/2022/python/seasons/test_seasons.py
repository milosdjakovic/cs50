import pytest
from seasons import TimeSinceBirthCalculator

def test_TimeSinceBirthCalculator():
    assert TimeSinceBirthCalculator("2024-04-29").difference_in_minutes_words == "Five hundred twenty-five thousand, six hundred minutes"
    assert TimeSinceBirthCalculator("2023-04-29").difference_in_minutes_words == "One million, fifty-two thousand, six hundred forty minutes"
    assert TimeSinceBirthCalculator("2020-04-29").difference_in_minutes_words == "Two million, six hundred twenty-nine thousand, four hundred forty minutes"
    assert TimeSinceBirthCalculator("2013-04-29").difference_in_minutes_words == "Six million, three hundred eleven thousand, five hundred twenty minutes"
    with pytest.raises(ValueError):
        TimeSinceBirthCalculator("2026-15-01")
    with pytest.raises(ValueError):
        TimeSinceBirthCalculator("2026-11-56")
