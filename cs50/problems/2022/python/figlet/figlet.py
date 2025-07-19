import sys
from pyfiglet import Figlet


def main():
  try:
    font = validate_args(args=sys.argv)
    figlet = Figlet()
    validate_font(font, figlet.getFonts())
  except ValueError as e:
    print(e)
    sys.exit(1)

  text = input("Input: ")
  figlet.setFont(font=font)
  print(figlet.renderText(text))

def validate_args(args):
  usage = "\nUsage: figlet.py [-f | --font] <font_name>"

  if len(args) != 3:
    raise ValueError(f"Incorrect number of arguments.{usage}")

  if args[1] not in ("-f", "--font"):
    raise ValueError(f"Incorrect font flag.{usage}")

  return args[2]


def validate_font(font, fonts):
  if font not in fonts:
    raise ValueError(f"Font \"{font}\" doesn't exist.")

if __name__ == "__main__":
  main()
