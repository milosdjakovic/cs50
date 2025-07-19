import sys
import requests


def main():
    if len(sys.argv) != 2:
        sys.exit("Missing command-line argument")

    try:
       amount = float(sys.argv[1])
    except:
       sys.exit("Command-line argument is not a number")

    try:
        payload = {'apiKey': 'f4f860d30ebd1f0aaa200c8fdad09852c64462a2babadb3678fbc9b48c4ec433'}
        r = requests.get('https://rest.coincap.io/v3/assets/bitcoin', params=payload)
        price = float(r.json()["data"]["priceUsd"])
        total = price * amount
        print(f"${total:,.4f}")
    except requests.RequestException as e:
       sys.exit(f"Request error {e}")


if __name__ == "__main__":
  main()
