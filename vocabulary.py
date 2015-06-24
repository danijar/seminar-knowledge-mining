import os
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import numpy as np
from scipy.sparse import coo_matrix
from helper.dataset import Dataset
from helper.preprocess import get_metadata
from helper.text import print_headline
from feature.words import WordsFeature
from sklearn.feature_extraction.text import CountVectorizer


def iterate_texts(directory):
    for filename in Dataset()._walk_images(directory):
        metadata = get_metadata(os.path.join(directory, filename))
        text = WordsFeature.preprocess_text(metadata['url'], metadata['title'], metadata['description'])
        yield text

def iterate_overall_texts(root):
    for directory in Dataset()._walk_directories(root):
        yield from iterate_texts(os.path.join(root, directory))

def get_vocabulary(texts):
    vectorizer = CountVectorizer(decode_error='replace', strip_accents='unicode', stop_words='english')
    term_counts = vectorizer.fit_transform(texts)
    term_counts = coo_matrix.sum(term_counts, axis=0).tolist()[0]
    amount = sum(term_counts)
    mapping = vectorizer.vocabulary_
    vocabulary = {term: term_counts[index] / amount for term, index in mapping.items()}
    return vocabulary

def compute_tfidf(vocabulary, overall):
    """
    Returns a copy of the vocabulary mapping to TFIDF scores instead of the
    frequencies. TFIDF is a measure for how unique the frequency is
    compared to the overall dataset.
    """
    assert all(0 <= frequency <= 1 for frequency in vocabulary.values())
    assert all(0 <= frequency <= 1 for frequency in overall.values())
    assert all(term in overall for term in vocabulary)
    result = {}
    for term in vocabulary:
        score = vocabulary[term] / (1 - overall[term])
        result[term] = score
    return result

def print_vocabulary(vocabulary, limit=None):
    vocabulary = sorted(vocabulary.items(), key=lambda x: x[1], reverse=True)
    if limit and len(vocabulary) > limit:
        vocabulary = vocabulary[:limit]
    for term, frequency in vocabulary:
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
    args = parser.parse_args()

    if '<dataset>' in args.output:
        args.output = args.output.replace('<dataset>', args.dataset)

    text = iterate_overall_texts(args.dataset)
    overall = get_vocabulary(text)

    for directory in Dataset()._walk_directories(args.dataset):
        print_headline(directory)
        texts = iterate_texts(os.path.join(args.dataset, directory))
        vocabulary = get_vocabulary(texts)
        vocabulary = compute_tfidf(vocabulary, overall)
        print_vocabulary(vocabulary, args.limit)
