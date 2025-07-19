import inflect

def main():
  names = []
  while True:
    try:
      name = input("Name: ")
      names.append(name)
    except (EOFError, KeyboardInterrupt):
      print_names(names)
      break


def print_names(names):
  p = inflect.engine()
  farewell_base = "Adieu, adieu, to "

  joined_names = p.join(names)

  farewell = farewell_base + joined_names

  print(farewell)


if __name__ == "__main__":
  main()
