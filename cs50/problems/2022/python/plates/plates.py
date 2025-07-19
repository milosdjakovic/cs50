def main():
    plate = input("Plate: ")
    if is_valid(plate):
        print("Valid")
    else:
        print("Invalid")


def is_valid(s):
    if not s.isalnum():
        return False

    if len(s) > 6 or len(s) < 2:
        return False

    if not s[0:2].isalpha():
        return False

    first_digit = True
    for i in range(len(s)):
        if first_digit and s[i] == "0":
            return False
        elif s[i].isdigit():
            first_digit = False
        if i > 0 and s[i-1].isdigit() and s[i].isalpha():
            return False

    return True


main()
