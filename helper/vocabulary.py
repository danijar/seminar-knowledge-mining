import os
import re
import json
from scipy.sparse import coo_matrix
from sklearn.feature_extraction.text import CountVectorizer


def load_vocabulary(filename):
    # Load vocabulary from file
    vocabulary = json.load(open(filename))
    buckets = sorted(list(vocabulary.keys()))
    terms = sum(vocabulary.values(), [])
    terms = sorted(list(set(terms)))
    return vocabulary, buckets, terms

def create_vectorizer(terms=None):
    args = {}
    args['decode_error'] = 'replace'
    args['strip_accents'] = 'unicode'
    args['stop_words'] = 'english'
    if terms:
        args['vocabulary'] = terms
    return CountVectorizer(**args)

def get_frequencies(texts):
    vectorizer = create_vectorizer()
    term_counts = vectorizer.fit_transform(texts)
    term_counts = coo_matrix.sum(term_counts, axis=0).tolist()[0]
    amount = sum(term_counts)
    mapping = vectorizer.vocabulary_
    frequencies = {term: term_counts[index] / amount for term, index in mapping.items()}
    return frequencies

def get_top_frequencies(frequencies, limit=20):
    frequencies = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)
    if limit and len(frequencies) > limit:
        frequencies = frequencies[:limit]
    frequencies = {key: value for (key, value) in frequencies}
    return frequencies

def preprocess_text(url, title, description):
    url = os.path.splitext(os.path.split(url)[1])[0]
    text = ' '.join((url, title, description))
    chunks = re.findall(r'[A-Z]?[a-z]{2,}', text)
    text = ' '.join(chunks)
    text = text.lower()
    return text
