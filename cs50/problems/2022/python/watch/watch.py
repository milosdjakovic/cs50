import re
import sys


def main():
    print(parse(input("HTML: ")))


def parse(s):
    matched = re.search(r'<iframe src="https?://(?:www\.)?youtube\.com/embed/(.+?)">', s)
    if matched:
        video_id = matched.group(1)
        video_short_url = f"https://youtu.be/{video_id}"
        return video_short_url
    else:
        return None


if __name__ == "__main__":
    main()
