def main():
  answer = input("What is the Answer to the Great Question of Life, the Universe, and Everything? ")

  sanitized_answer = answer.lower().strip()

  match sanitized_answer:
    case "42" | "forty two" | "forty-two":
      print("Yes")
    case _:
      print("No")


main()
