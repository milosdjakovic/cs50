def main():
  s = input("Input: ")
  f = remove_vowels(s)
  print(f"Output: {f}")

def remove_vowels(s):
  vowels = ("a", "e", "i", "o", "u")
  chars = []
  for c in s:
    if c.lower() in vowels:
      continue
    chars.append(c)
  return "".join(chars)


if __name__ == "__main__":
  main()
