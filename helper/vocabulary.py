import os
import re
import json
import snowballstemmer
from scipy.sparse import coo_matrix
from sklearn.feature_extraction.text import CountVectorizer


def load_vocabulary(filename):
    # Load vocabulary from file
    vocabulary = json.load(open(filename))
    buckets = sorted(list(vocabulary.keys()))
    terms = sum(vocabulary.values(), [])
    terms = sorted(list(set(terms)))
    return vocabulary, buckets, terms

def stemming(text):
    stemmer = snowballstemmer.stemmer('english')
    return ' '.join(stemmer.stemWords(text.split()))

def create_vectorizer(terms=None, stopwords='english'):
    args = {}
    args['decode_error'] = 'replace'
    args['strip_accents'] = 'unicode'
    args['stop_words'] = stopwords
    args['preprocessor'] = stemming
    if terms:
        args['vocabulary'] = terms
    return CountVectorizer(**args)

def get_frequencies(texts, stopwords):
    vectorizer = create_vectorizer(stopwords=stopwords)
    term_counts = vectorizer.fit_transform(texts)
    term_counts = coo_matrix.sum(term_counts, axis=0).tolist()[0]
    amount = sum(term_counts)
    assert term_counts
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
    # Tokenize
    chunks = re.findall(r'[A-Z]?[a-z]{2,}', text)
    # Stemming
    stemmer = snowballstemmer.stemmer('english')
    chunks = stemmer.stemWords(chunks)
    # Combine to input string for CountVectorizer
    text = ' '.join(chunks)
    text = text.lower()
    return text
