def main():
  change_owed = 50

  while change_owed > 0:
    print(f"Amount Due: {change_owed}")
    coin = input("Insert Coin: ")
    if coin != "25" and coin != "10" and coin != "5":
      continue
    change_owed -= int(coin)
  print(f"Change Owed: {change_owed * -1}")

if __name__ == "__main__":
  main()
