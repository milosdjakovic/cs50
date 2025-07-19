import sys

def main():
    try:
        file_name = get_file_name(sys.argv)
        line_count = count_lines(file_name)
        print(line_count)
    except:
        sys.exit(1)


def get_file_name(args):
    try:
        if len(args) < 2:
            raise ValueError("Too few command-line arguments")
        if len(args) > 2:
            raise ValueError("Too many command-line arguments")
        if not args[1].endswith(".py"):
            raise ValueError("Not a Python file")
        return args[1]
    except ValueError as e:
        print(e)
        raise

def count_lines(file_name):
    line_count = 0
    try:
        with open(file_name, 'r') as file:
            for line in file:
                no_indentation_line = line.lstrip()
                if no_indentation_line.startswith("#"):
                    continue
                if len(no_indentation_line) == 0:
                    continue
                line_count += 1

        return line_count
    except FileNotFoundError:
        print(f"File does not exist")
        raise

if __name__ == "__main__":
    main()
