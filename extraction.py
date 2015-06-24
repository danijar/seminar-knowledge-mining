from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from helper.plot import plot_image
from helper.dataset import Dataset
from helper.extraction import feature_names, feature_vector
from feature.words import WordsFeature


if __name__ == '__main__':
    parser = ArgumentParser(description='Extract features of a dataset.',
        formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('dataset',
        help='Path to the directory containing folders for each class that \
        contain the images and metadata')
    parser.add_argument('-i', '--image', action='store_true',
        help='Whether to extract visual features from the image')
    parser.add_argument('-t', '--textual', action='store_true',
        help='Whether to extract textual features; requires JSON metadata \
        files for all the images')
    parser.add_argument('-v', '--vocabulary', default='<dataset>/vocabulary.json',
        help='Filename of the JSON vocabulary used for bag of words')
    parser.add_argument('-o', '--output', default='<dataset>/features.json',
        help='Where to store the extracted features')
    args = parser.parse_args()

    args.output = args.output.replace('<dataset>', args.dataset)
    args.vocabulary = args.vocabulary.replace('<dataset>', args.dataset)

    assert args.image or args.textual, 'Need at least one feature source'
    if args.textual:
        assert args.vocabulary, 'Vocabulary is needed for textual features'
        WordsFeature.load_vocabulary(args.vocabulary)

    dataset = Dataset()
    dataset.read(args.dataset, args.image, args.textual)
    dataset.save(args.output)
