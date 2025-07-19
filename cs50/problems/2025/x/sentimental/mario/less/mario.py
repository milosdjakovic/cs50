from cs50 import get_int

while True:
    height = get_int("Height: ")
    if height > 0 and height < 9:
        break


for i in range(height):
    for j in range(height):
        spaces = height - 1 - i
        segments = i + 1
    print(" " * spaces, end="")
    print("#" * segments, end="")
    print()
