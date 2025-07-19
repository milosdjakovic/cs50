import re


def main():
    print(convert(input("Hours: ")))


def convert(s):
    matched = re.search(r"(\d{1,2}):?(\d{1,2})? (AM|PM) to (\d{1,2}):?(\d{1,2})? (AM|PM)", s)

    if not matched:
        raise ValueError

    start_hours, start_minutes, start_meridiem, end_hours, end_minutes, end_meridiem = matched.groups()

    if not start_minutes:
        start_minutes = "00"

    if not end_minutes:
        end_minutes = "00"

    if int(start_hours) > 12 or int(start_minutes) > 59 or int(end_hours) > 12 or int(end_minutes) > 59:
        raise ValueError

    if start_meridiem == "PM":
        adjusted_start_hours = int(start_hours) + 12
        start_hours = "12" if start_hours == "12" else f"{adjusted_start_hours:02}"
    else:
        start_hours = "00" if start_hours == "12" else f"{int(start_hours):02}"


    if end_meridiem == "PM":
        adjusted_end_hours = int(end_hours) + 12
        end_hours = "12" if end_hours == "12" else f"{adjusted_end_hours:02}"
    else:
        end_hours = "00" if end_hours == "12" else f"{int(end_hours):02}"

    converted = f"{start_hours}:{start_minutes} to {end_hours}:{end_minutes}"

    return converted


if __name__ == "__main__":
    main()
