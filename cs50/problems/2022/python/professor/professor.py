import sys
import random

def main():
    level = get_level()
    score = run_game(level)
    print(f"Score: {score}")

def get_int(prompt):
    while True:
        try:
            user_input = input(prompt)
            return int(user_input)
        except (EOFError, KeyboardInterrupt):
            print("\nGame Terminated!")
            sys.exit(0)
        except ValueError:
             raise ValueError

def get_level():
    while True:
        try:
            level = get_int("Level: ")
            if level in [1, 2, 3]:
                return level
        except ValueError:
            pass

def generate_integer(level):
    match level:
        case 1:
            bounds = (0, 9)
        case 2:
            bounds = (10, 99)
        case 3:
            bounds = (100, 999)
        case _:
            raise ValueError("Level must be 1, 2, or 3")

    lower_bound, upper_bound = bounds
    return random.randint(lower_bound, upper_bound)

def handle_problem(x, y):
    correct_answer = x + y
    tries = 0
    while tries < 3:
        try:
            prompt = f"{x} + {y} = "
            user_answer = get_int(prompt)

            if user_answer == correct_answer:
                return True
            else:
                tries += 1
                print("EEE")

        except ValueError:
            tries += 1
            print("EEE")

    print(correct_answer)
    return False

def run_game(level, num_problems=10):
    score = 0
    for _ in range(num_problems):
        x = generate_integer(level)
        y = generate_integer(level)
        if handle_problem(x, y):
            score += 1
    return score

if __name__ == "__main__":
    main()
