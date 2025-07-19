import re


def main():
    print(count(input("Text: ")))


def count(s):
    matches = re.findall(r"\b(um)\b", s, flags=re.IGNORECASE)
    if not matches:
        raise ValueError
    return len(matches)

if __name__ == "__main__":
    main()
