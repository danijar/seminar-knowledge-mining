import numpy as np
from argparse import ArgumentParser
from helper.image import load, show
from features.color import ColorFeature


def apply_extractors(image, extractors):
    names = []
    features = []
    for extractor in extractors:
        names += extractor.names()
        features += extractor(image).extract()
    assert len(names) == len(features)
    return names, features

def print_features(names, features):
    for name, feature in zip(names, features):
        print('{name: <25} {feature: >8.3f}'.format(**locals()))

if __name__ == '__main__':
    parser = ArgumentParser(description='Extract features from images.')
    parser.add_argument('filename',
        help='Path to the image to extract features from')
    args = parser.parse_args()

    extractors = [
        ColorFeature
    ]

    image = load(args.filename)
    # show(image)
    names, features = apply_extractors(image, extractors)
    print_features(names, features)
