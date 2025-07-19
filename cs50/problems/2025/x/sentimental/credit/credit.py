from cs50 import get_string

cc_num = get_string("Number: ")


first_digit = cc_num[0]


def extract_sequence_start(card_number):
    if (first_digit == "3" or first_digit == "5"):
        return card_number[:2]
    elif (first_digit == "4"):
        return card_number[0]
    else:
        return None


def get_card_name(sequence):
    if (sequence == None):
        return "INVALID"

    cards = {
        "AMEX": {
            "starting_sequences": ["34", "37"],
            "lengths": [15]
        },
        "MASTERCARD": {
            "starting_sequences": ["51", "52", "53", "54", "55"],
            "lengths": [16]
        },
        "VISA": {
            "starting_sequences": ["4"],
            "lengths": [13, 16]
        }

    }

    sequence_start = extract_sequence_start(sequence)
    card = "INVALID"

    for card_name, prefs in cards.items():
        valid_sequence_start = sequence_start in prefs["starting_sequences"]
        valid_sequence_length = len(sequence) in prefs["lengths"]
        if (valid_sequence_start and valid_sequence_length):
            card = card_name

    return card


def validate_checksum(card_number):
    reversed = card_number[::-1]
    sum = ""

    for n in reversed[1::2]:
        sum += str(int(n) * 2)

    for n in reversed[0::2]:
        sum += n

    total = 0

    for n in sum:
        total += int(n)

    return total % 10 == 0


valid = validate_checksum(cc_num)

if (valid):
    card_name = get_card_name(cc_num)
    print(card_name)
else:
    print("INVALID")
