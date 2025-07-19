import sys
from datetime import date
import re
import inflect

class TimeSinceBirthCalculator:
    def __init__(self, birth_date=None):
        if birth_date:
            self.birth_date = birth_date
        else:
            self.birth_date = input("Date of Birth: ")

    @property
    def birth_date(self):
        return self._birth_date

    @birth_date.setter
    def birth_date(self, value):
        date_valid = self.validate_date_string(value)
        if not date_valid:
            sys.exit(1)
        self._birth_date = self.get_birth_date_object(value)

    def validate_date_string(self, date_string):
        matched = re.search(r"^\d{4}-\d{2}-\d{2}$", date_string)
        return bool(matched)

    def get_birth_date_object(self, date_string):
        try:
            return date.fromisoformat(date_string)
        except ValueError:
            print("Incorrect date")
            raise ValueError

    @property
    def current_date_object(self):
        return date.today()

    @property
    def difference_in_minutes(self):
        difference = self.current_date_object - self._birth_date
        difference_minutes = difference.days * 24 * 60
        return difference_minutes

    @property
    def difference_in_minutes_words(self):
        p = inflect.engine()
        number_in_words = p.number_to_words(self.difference_in_minutes, andword="").capitalize()
        return number_in_words + " minutes"

    def __str__(self):
        return self.difference_in_minutes_words


def main():
    print(TimeSinceBirthCalculator())


if __name__ == "__main__":
    main()
