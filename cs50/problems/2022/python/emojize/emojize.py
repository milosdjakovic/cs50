import emoji

def main():
  i = input("Input: ")
  print(emoji.emojize(i, language='alias'))


if __name__ == "__main__":
  main()
