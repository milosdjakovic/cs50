import csv
import sys


def get_file_names():
    if (len(sys.argv) != 3):
        print("Usage: python dna.py database.csv sequence.txt")
        return
    database_csv = sys.argv[1]
    sequence_txt = sys.argv[2]

    return (database_csv, sequence_txt)


def read_csv(file_path):
    try:
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            data = list(reader)
            return data
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None


def read_txt(file_path):
    try:
        with open(file_path, 'r') as file:
            data = file.read()
            return data
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None


def extract_strs(database):
    keys = list(database[0].keys())
    return keys[1:]


def count_strs(sequence, strs):
    count_results = {}

    for str in strs:
        count_results[str] = longest_match(sequence, str)

    return count_results


def check_database(database, strs, sample):
    str_count = len(strs)
    matched_person = "No match"

    for person in database:
        matches = 0

        for str in strs:
            person_strs = int(person[str])
            sample_strs = sample[str]

            if (person_strs == sample_strs):
                matches += 1

        if (matches == str_count):
            matched_person = person["name"]

    return matched_person


def main():
    # TODO: Check for command-line usage
    database_csv, sequence_txt = get_file_names()
    # print(f"database_csv: {database_csv}")
    # print(f"sequence_txt: {sequence_txt}")

    # TODO: Read database file into a variable
    database = read_csv(database_csv)
    # print(f"database: {database}")

    # TODO: Read DNA sequence file into a variable
    sequence = read_txt(sequence_txt)
    # print(f"sequence: {sequence}")

    # TODO: Find longest match of each STR in DNA sequence
    strs = extract_strs(database)
    # print(f"strs: {strs}")

    sample = count_strs(sequence, strs)
    # print(f"sample: {sample}")

    # TODO: Check database for matching profiles
    match = check_database(database, strs, sample)
    # print(f"match: {match}")
    print(match)

    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
