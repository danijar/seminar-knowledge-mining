from helper.image import load
from argparse import ArgumentParser


if __name__ == '__main__':
    parser = ArgumentParser(description='Extract features from images.')
    parser.add_argument('filename',
        help='Path to the image to extract features from')
    args = parser.parse_args()
    original, resized = load(args.filename)
    original.show()
    resized.show()
