import numpy as np
import skimage.data
from argparse import ArgumentParser
from helper.image import load, show
from features.color import ColorFeature
from features.histogram import HistogramFeature
from features.blob import BlobFeature
from features.gradient import GradientFeature


def get_extractors():
    return [
        ColorFeature,
        HistogramFeature,
        BlobFeature,
        GradientFeature
    ]

def feature_vector(image):
    return list(apply_extractors(image, get_extractors()))

def feature_names():
    dummy_image = skimage.data.astronaut()
    names = []
    for extractor in get_extractors():
        names += extractor(dummy_image).names()
    return names

def apply_extractors(image, extractors):
    for extractor in extractors:
        features = extractor(image).extract()
        # TODO: Why do we need to dissolve the generator here?
        features = list(features)
        yield from features

def validate_feature_range(names, features):
    for name, feature in zip(names, features):
        assert 0 <= feature <= 1, name + ' is not between 0 and 1'

def print_features(names, features):
    print(len(names), 'features extracted:')
    for name, feature in zip(names, features):
        print('{name: <25} {feature: >8.4f}'.format(**locals()))


if __name__ == '__main__':
    parser = ArgumentParser(description='Extract feature vector of an image.')
    parser.add_argument('filename',
        help='Path to the image to extract features from')
    args = parser.parse_args()

    image = load(args.filename)
    # show(image)
    # BlobFeature(image).show()
    # GradientFeature(image).show()

    names = feature_names()
    features = feature_vector(image)
    validate_feature_range(names, features)
    print_features(names, features)
