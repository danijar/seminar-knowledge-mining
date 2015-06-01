import numpy as np
import skimage.data
from argparse import ArgumentParser
from helper.image import load, preprocess
from helper.plot import plot_image
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

def get_inputs(filename):
    """
    Return kwargs containing different image versions and DBpedia meta data
    needed to construct feature extractors.
    """
    args = {}
    # Image inputs
    original = load(filename)
    image = preprocess(original)
    args['original'] = original
    args['image'] = image
    args['gray']     = skimage.color.rgb2gray(image)
    args['channels'] = np.rollaxis(image, 2)
    args['pixels']   = image.reshape(-1, image.shape[-1])
    # Define images as write only since they're shared between extractors
    for name in args:
        if args[name] is np.ndarray:
            args[name].setflags(write=False)
    # Textual data
    args['filename'] = filename
    return args

def feature_vector(filename):
    inputs = get_inputs(filename)
    extractors = get_extractors()
    features = apply_extractors(inputs, extractors)
    return list(features)

def feature_names():
    names = []
    for extractor in get_extractors():
        for name in extractor.names():
            names.append(name)
    return names

def apply_extractors(inputs, extractors):
    for extractor in extractors:
        yield from extractor(**inputs).extract()

def validate_feature_range(names, features):
    assert len(names) == len(features)
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

    # inputs = get_inputs(args.filename)
    # plot_image(inputs['original'])
    # plot_image(inputs['image'])
    # BlobFeature(**inputs).show()
    # GradientFeature(**inputs).show()

    names = feature_names()
    features = feature_vector(args.filename)
    validate_feature_range(names, features)
    print_features(names, features)
