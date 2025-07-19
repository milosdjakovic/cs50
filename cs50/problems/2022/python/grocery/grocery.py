groceries = {}


def main():
    while True:
        try:
            item = input("").strip().upper()
            groceries[item] += 1
        except KeyError:
            groceries[item] = 1
        except (EOFError, KeyboardInterrupt):
            print_groceries()
            break


def print_groceries():
    for grocery in sorted(groceries.keys()):
        print(f"{groceries[grocery]} {grocery}")


if __name__ == "__main__":
    main()
