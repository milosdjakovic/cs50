import sys
import csv
from tabulate import tabulate


def main():
    try:
        file_name = get_csv_file_name(sys.argv)
        print_table_from_csv(file_name)
    except ValueError as e:
        print(e)
        sys.exit(1)
    except FileNotFoundError:
        print(f"File does not exist")
        sys.exit(1)


def get_csv_file_name(args):
    if len(args) < 2:
        raise ValueError("Too few command-line arguments")
    elif len(args) > 2:
        raise ValueError("Too many command-line arguments")
    elif not args[1].endswith(".csv"):
        raise ValueError("Not a CSV file")
    else:
        return args[1]


def print_table_from_csv(file_name):
    with open(file_name) as csvfile:
        reader = csv.reader(csvfile)
        print(tabulate(list(reader), headers="firstrow", tablefmt="grid"))


if __name__ == "__main__":
    main()
