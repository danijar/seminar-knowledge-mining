import os
import json
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import numpy as np
from helper.dataset import Dataset
from helper.extraction import get_metadata
from helper.vocabulary import preprocess_text, get_frequencies, get_top_frequencies
from helper.text import print_headline
from feature.words import WordsFeature


def read_lines(filename):
    with open(filename) as file_:
        return file_.read().splitlines()

def iterate_texts(directory):
    for filename in Dataset()._walk_images(directory):
        metadata = get_metadata(os.path.join(directory, filename))
        text = preprocess_text(metadata['url'], metadata['title'], metadata['description'])
        yield text

def iterate_overall_texts(root):
    for directory in Dataset()._walk_directories(root):
        yield from iterate_texts(os.path.join(root, directory))

def compute_tfidf(frequencies, overall):
    """
    Returns a copy of the frequencies mapping to TFIDF scores instead of the
    frequencies. TFIDF is a measure for how unique the frequency is
    compared to the overall dataset.
    """
    assert all(0 <= frequency <= 1 for frequency in frequencies.values())
    assert all(0 <= frequency <= 1 for frequency in overall.values())
    assert all(term in overall for term in frequencies)
    result = {}
    for term in frequencies:
        score = frequencies[term] / (1 - overall[term])
        result[term] = score
    return result

def print_frequencies(frequencies, limit=None):
    frequencies = get_top_frequencies(frequencies, limit).items()
    frequencies = sorted(frequencies, key=lambda x: x[1], reverse=True)
    for term, frequency in frequencies:
        print('{: <20} {: >6.2f}%'.format(term, frequency * 100))


if __name__ == '__main__':
    parser = ArgumentParser(description='Generate vocabulary that to each \
        class maps its most frequent words.',
        formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('dataset',
        help='Path to the directory containing folders for each class that \
        contain the images and metadata')
    parser.add_argument('-l', '--limit', type=int, default=20,
        help='Maximal amount of words to display for each class')
    parser.add_argument('-o', '--output', default='<dataset>/vocabulary.json',
        help='Filename of the JSON vocabulary that will be written')
    parser.add_argument('-s', '--stopwords', default='english',
        help='Path to a file containing a list of stopwords; defaults to \
        an english stopwords list')
    args = parser.parse_args()

    args.output = args.output.replace('<dataset>', args.dataset)

    if os.path.isfile(args.stopwords):
        args.stopwords = read_lines(args.stopwords)

    text = iterate_overall_texts(args.dataset)
    overall = get_frequencies(text, args.stopwords)

    vocabulary = {}
    for directory in Dataset()._walk_directories(args.dataset):
        print_headline(directory)
        texts = iterate_texts(os.path.join(args.dataset, directory))
        frequencies = get_frequencies(texts, args.stopwords)
        frequencies = compute_tfidf(frequencies, overall)
        synonyms = list(get_top_frequencies(frequencies, args.limit).keys())
        vocabulary[directory] = synonyms
        print_frequencies(frequencies, args.limit)

    print('')
    print('Write vocabulary to', args.output)
    json.dump(vocabulary, open(args.output, 'w'))
    print('Done')
