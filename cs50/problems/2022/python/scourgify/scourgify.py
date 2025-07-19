import sys
import csv

def main():
    try:
        input_file, output_file = get_csv_file_names(sys.argv)
    except ValueError as e:
        print(e)

    refactor_csv(input_file, output_file)


def get_csv_file_names(args):
    if len(args) < 3:
        raise ValueError("Too few command-line arguments")
    elif len(args) > 3:
        raise ValueError("Too many command-line arguments")
    elif not args[1].endswith(".csv"):
        raise ValueError("Input not csv file")
    elif not args[2].endswith(".csv"):
        raise ValueError("Output not csv file")
    else:
        input_file = args[1]
        output_file = args[2]
        return input_file, output_file


def refactor_csv(input_file, output_file):
    try:
        with open(input_file) as input_csv, open(output_file, "w") as output_csv:
            reader = csv.DictReader(input_csv)
            writer = csv.DictWriter(output_csv, fieldnames=["first", "last", "house"])
            writer.writeheader()
            for row in reader:
                last, first = row["name"].split(", ")
                writer.writerow({"first": first, "last": last, "house": row["house"]})
    except FileNotFoundError:
        print(f"Could not read {input_file}")
        sys.exit(1)



if __name__ == "__main__":
    main()
