def main():
    percentage = get_fraction()
    fuel_level = gauge(percentage)
    print(fuel_level)


def get_fraction():
    while True:
        try:
            fraction = input("Fraction: ")
            return convert(fraction)
        except Exception as e:
            print(e)


def convert(fraction):
    try:
        numerator, denominator = fraction.split("/")
        numerator = int(numerator)
        denominator = int(denominator)
    except ValueError:
        raise ValueError("Fraction format should be \"X/Y\"")

    if numerator > denominator:
        raise ValueError("Denominator must be larger than numerator")

    try:
        percentage = (numerator / denominator) * 100
    except ZeroDivisionError:
        raise ZeroDivisionError("Denominator cannot be zero.")

    return round(percentage)


def gauge(percentage):
    rounded_percentage = round(percentage)
    if rounded_percentage < 2:
        return "E"
    elif  rounded_percentage > 98:
        return "F"
    else:
        return f"{rounded_percentage}%"


if __name__ == "__main__":
    main()
