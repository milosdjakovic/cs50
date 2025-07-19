import random


def main():
    level = get_value("Level: ")
    goal = random.randrange(1, level + 1)
    print_results(goal)

def print_results(goal):
    while True:
        guess = get_value("Guess: ")

        if guess == goal:
            print("Just right!")
            break
        elif guess > goal:
            print("Too large!")
        elif guess < goal:
            print("Too small!")


def get_value(message):
    level = 0
    while level < 1:
        try:
            level = int(input(message))
        except ValueError:
            print("Input must be a positive number")
            pass
    return level


if __name__ == "__main__":
    main()
