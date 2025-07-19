import validators

def main():
    print(validate_email(input("What's your email address? ")))


def validate_email(s):
    try:
        email_valid = validators.email(s)
        if email_valid:
            return "Valid"
        else:
            return "Invalid"
    except ValidationError:
        return "Invalid"


if __name__ == "__main__":
    main()
