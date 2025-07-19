def main():
  greeting = input("Greeting: ")
  v = value(greeting)
  print(f"${v}")


def value(greeting):
  sanitized_greeting = greeting.lower().strip()

  if sanitized_greeting.startswith("hello"):
    return 0
  elif sanitized_greeting.startswith("h"):
    return 20
  else:
    return 100


if __name__ == "__main__":
  main()
