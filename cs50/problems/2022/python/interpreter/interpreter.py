def main():
  expression = input("Expression: ").strip()
  x, y, z = expression.split(" ")
  result = calculate(x, y, z)
  print(result)

def calculate(x, y, z):
  match y:
    case "+":
      return float(int(x) + int(z))
    case "-":
      return float(int(x) - int(z))
    case "*":
      return float(int(x) * int(z))
    case "/":
      return float(int(x) / int(z))

main()
