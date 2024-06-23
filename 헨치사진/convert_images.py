# convert_images.py
from PIL import Image
import os
import sys

def convert_image_to_gif(file_path):
    img = Image.open(file_path)
    base_filename = os.path.splitext(file_path)[0]
    gif_filename = base_filename + '.gif'
    img.save(gif_filename)
    print(f"Converted {file_path} to {gif_filename}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python convert_images.py <file1> <file2> ...")
    else:
        for file_path in sys.argv[1:]:
            convert_image_to_gif(file_path)
