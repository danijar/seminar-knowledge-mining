from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from helper.plot import plot_image
from helper.extraction import feature_names, feature_vector
from helper.preprocess import get_inputs


def print_features(names, features):
    print(len(names), 'features extracted:')
    for name, feature in zip(names, features):
        print('{name: <25} {feature: >8.4f}'.format(**locals()))


if __name__ == '__main__':
    parser = ArgumentParser(description='Extract feature vector of an image.',
        formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('filename',
        help='Path to the image to extract features from')
    parser.add_argument('-o', '--original', action='store_true',
        help='Whether to show the original image')
    parser.add_argument('-p', '--proprocessed', action='store_true',
        help='Whether to show the proprocessed image')
    parser.add_argument('-b', '--blobs', action='store_true',
        help='Whether to show the extracted blobs')
    parser.add_argument('-g', '--gradients', action='store_true',
        help='Whether to show the extracted gradients')
    args = parser.parse_args()

    inputs = get_inputs(args.filename)
    if args.original:
        plot_image(inputs['original'])
    if args.proprocessed:
        plot_image(inputs['image'])
    if args.blobs:
        BlobFeature(**inputs).show()
    if args.gradients:
        GradientFeature(**inputs).show()

    names = feature_names()
    features = feature_vector(args.filename)
    print_features(names, features)
