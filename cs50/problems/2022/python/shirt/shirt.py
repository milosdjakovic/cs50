import os
import sys
from PIL import Image, ImageOps

def main():
    try:
        input_file_name, output_file_name = get_image_file_names(sys.argv)
    except ValueError as e:
        print(e)
        sys.exit(1)

    place_shirt_overlay(input_file_name, output_file_name)


def get_image_file_names(args):
    if len(args) < 3:
        raise ValueError("Too few command-line arguments")
    elif len(args) > 3:
        raise ValueError("Too many command-line arguments")
    elif not args[1].endswith((".png", ".jpg")):
        raise ValueError("Invalid input")
    elif not args[2].endswith((".png", ".jpg")):
        raise ValueError("Invalid input")
    else:
        input_file_name = args[1]
        output_file_name = args[2]
        input_file_ext = os.path.splitext(input_file_name)[-1]
        output_file_ext = os.path.splitext(output_file_name)[-1]

        if input_file_ext != output_file_ext:
            raise ValueError("Input and output have different extensions")

        return input_file_name, output_file_name

def place_shirt_overlay(input_file_name, output_file_name):
    try:
        with Image.open("shirt.png") as shirt_image, Image.open(input_file_name) as input_image:
            input_image = ImageOps.fit(input_image, size = (shirt_image.size))
            input_image.paste(shirt_image, shirt_image)
            input_image.save(output_file_name)
    except FileNotFoundError:
        print("Input does not exist")
        sys.exit(1)


if __name__ == "__main__":
    main()
