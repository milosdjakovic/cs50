from cs50 import get_string

input = get_string("Text: ")


def get_averages(text):
    letter_count = 0
    word_count = 0
    sentence_count = 0

    if (len(text) > 0):
        word_count += 1

    for char in text:
        if (char.isalpha()):
            letter_count += 1

        if (char.isspace()):
            word_count += 1

        if (char in [".", "?", "!"]):
            sentence_count += 1

    average_letters = (letter_count * 100.0) / word_count
    average_sentences = (sentence_count * 100.0) / word_count

    return (average_letters, average_sentences)


def calculate_cl_index(L, S):
    return 0.0588 * L - 0.296 * S - 15.8


def print_grade(cl_index):
    round_cl_index = round(cl_index)
    if round_cl_index < 1:
        print("Before Grade 1")
    elif round_cl_index > 16:
        print("Grade 16+")
    else:
        print(f"Grade {round_cl_index}")


def main():
    avg_l, avg_s = get_averages(input)
    cl_index = calculate_cl_index(avg_l, avg_s)
    print_grade(cl_index)


if __name__ == "__main__":
    main()
