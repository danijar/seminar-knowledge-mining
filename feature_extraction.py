import numpy as np
from argparse import ArgumentParser
from helper.image import load, show
from features.color import ColorFeature
from features.histogram import HistogramFeature
from features.blob import BlobFeature
from features.gradient import GradientFeature


def apply_extractors(image, extractors):
    names = []
    features = []
    for extractor in extractors:
        instance = extractor(image)
        names += list(instance.names())
        features += list(instance.extract())
    assert len(names) == len(features)
    return names, features

def validate_feature_range(names, features):
    for name, feature in zip(names, features):
        assert 0 <= feature <= 1, name + ' is not between 0 and 1'

def print_features(names, features):
    print(len(names), 'features extracted:')
    for name, feature in zip(names, features):
        print('{name: <25} {feature: >8.4f}'.format(**locals()))

if __name__ == '__main__':
    parser = ArgumentParser(description='Extract features from images.')
    parser.add_argument('filename',
        help='Path to the image to extract features from')
    args = parser.parse_args()

    extractors = [
        ColorFeature,
        HistogramFeature,
        BlobFeature,
        GradientFeature
    ]

    image = load(args.filename)
    # show(image)
    # GradientFeature(image).show()

    names, features = apply_extractors(image, extractors)
    validate_feature_range(names, features)
    print_features(names, features)
