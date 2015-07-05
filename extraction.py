import os
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from helper.dataset import Dataset
from feature.color import ColorFeature
from feature.histogram import HistogramFeature
from feature.blob import BlobFeature
from feature.gradient import GradientFeature
from feature.brief import BriefFeature
from feature.geo import GeoFeature
from feature.format import FormatFeature
from feature.size import SizeFeature
from feature.words import WordsFeature
from feature.random import RandomFeature


def read_samples(root):
    samples = Dataset()._read_samples(root)
    return samples


if __name__ == '__main__':
    parser = ArgumentParser(description='Extract and store features of a '
        'dataset.',
        formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('dataset',
        help='Path to the directory containing folders for each class that '
        'contain the images and metadata')
    parser.add_argument('-v', '--visual', action='store_true',
        help='Whether to extract visual features from the image')
    parser.add_argument('-t', '--textual', action='store_true',
        help='Whether to extract textual features; requires JSON metadata '
        'files for all the images')
    parser.add_argument('-s', '--stopwords', default='english',
        help='Filename of a list of words that are ignored for the '
        'vocabulary; defaults to a built-in english stopword list')
    parser.add_argument('-o', '--output', default='<dataset>/dataset.json',
        help='Where to store the extracted features')
    args = parser.parse_args()

    args.output = args.output.replace('<dataset>', args.dataset)
    assert args.visual or args.textual, 'Need at least one feature source'

    extractors = []
    if args.visual:
        extractors.append(SizeFeature())
        extractors.append(ColorFeature())
        extractors.append(HistogramFeature())
        extractors.append(GradientFeature())
        # extractors.append(BlobFeature())
        # extractors.append(BriefFeature())
    if args.textual:
        samples = read_samples(args.dataset)
        if os.path.isfile(args.stopwords):
            args.stopwords = open(args.stopwords)
        extractors.append(GeoFeature())
        extractors.append(FormatFeature())
        extractors.append(WordsFeature(samples, args.stopwords))
        # extractors.append(RandomFeature())

    dataset = Dataset(logging=True)
    dataset.read(args.dataset, extractors)
    dataset.save(args.output)
