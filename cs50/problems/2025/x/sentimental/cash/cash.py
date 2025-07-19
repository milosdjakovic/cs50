from cs50 import get_float

while True:
    change = int(get_float("Change: ") * 100)
    if change > 0:
        break

coins = [25, 10, 5, 1]
coins_count = 0

for coin in coins:
    coins_count += change // coin
    change %= coin
    # while change >= coin:
    #     change -= coin
    #     coins_count += 1

print(coins_count)
