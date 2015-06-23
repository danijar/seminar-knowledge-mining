from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from helper.plot import plot_image
from helper.dataset import Dataset
from helper.extraction import feature_names, feature_vector


if __name__ == '__main__':
    parser = ArgumentParser(description='Extract features of a dataset.',
        formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('dataset',
        help='Path to the directory containing folders for each class that \
        contain the images and metadata')
    parser.add_argument('-v', '--visual', action='store_true',
        help='Whether to extract visual features')
    parser.add_argument('-t', '--textual', action='store_true',
        help='Whether to extract textual features; requires JSON metadata \
        files for all the images')
    parser.add_argument('-o', '--output', default='<dataset>/features.json',
        help='Where to store the extracted features')
    args = parser.parse_args()

    args.output = args.output.replace('<dataset>', args.dataset)

    assert args.visual or args.textual, 'Need at least one feature source'

    dataset = Dataset()
    dataset.read(args.dataset, args.visual, args.textual)
    dataset.save(args.output)
