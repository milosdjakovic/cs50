month_names = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]


def main():
    while True:

        try:
            little_endian_date = input("Date: ")
            if "/" in little_endian_date:
                date_data = parse_short_date(little_endian_date)
            elif "," in little_endian_date:
                date_data = parse_long_date(little_endian_date)
            else:
                raise ValueError

            formatted_date = format_big_endian(date_data)
            print(formatted_date)

            break
        except ValueError as e:
            print(f"Date format not valid:\n{e}")
        except (EOFError, KeyboardInterrupt):
            print()
            break


def parse_short_date(date_string):
    try:
        date_values = date_string.split("/")

        if len(date_values) != 3:
            raise ValueError

        day = int(date_values[1])
        month = int(date_values[0])
        year = int(date_values[2])

        validate_date(year, month, day)

        return (year, month, day)
    except ValueError:
        raise ValueError("Day, month, and year values should be numbers")


def parse_long_date(date_string):
    try:
        date_values = date_string.split(" ")
        date_values[1] = date_values[1][:-1]

        if len(date_values) != 3:
            raise ValueError

        day = int(date_values[1])
        month_name = date_values[0].capitalize()
        month = month_names.index(month_name) + 1
        year = int(date_values[2])

        validate_date(year, month, day)

        return (year, month, day)
    except ValueError:
        raise ValueError("Day, month, and year values should be numbers")


def validate_date(year, month, day):
    if not year > 0:
        raise ValueError("Year not valid, year must be anno Domini")

    if month < 1 or month > 12:
        raise ValueError("Month not valid, value must be between 0 and 12")

    if day < 1 or day > 31:
        raise ValueError("Day not valid, value must be between 0 and 31")


def format_big_endian(values):
    return f"{values[0]:04}-{values[1]:02}-{values[2]:02}"


if __name__ == "__main__":
    main()
