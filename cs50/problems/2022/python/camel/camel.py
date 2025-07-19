def main():
  camel_case = input("camelCase: ")
  snake_case = camel_to_snake(camel_case)
  print(f"snake_case: {snake_case}")

def camel_to_snake(s):
  chars = []

  for c in s:
    if c.isupper():
      chars.append("_")
      chars.append(c.lower())
    else:
      chars.append(c)

  return "".join(chars)


if __name__ == "__main__":
  main()
