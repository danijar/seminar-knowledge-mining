import re
import os
from sklearn.feature_extraction.text import CountVectorizer
from .feature import Feature


SYNONYMS = {
    'chart':         ['chart', 'diagram'],
    'document':      ['document', 'scan'],
    'drawn':         ['drawn', 'sketch'],
    'embellishment': ['embellishment'],
    'flag':          ['flag', 'state'],
    'icon':          ['icon', 'pictogram'],
    'landscape':     ['landscape', 'view', 'mountains'],
    'logo':          ['logo', 'coat', 'arms'],
    'map':           ['map', 'country'],
    'object':        ['object'],
    'painting':      ['painting', 'art'],
    'portrait':      ['portrait', 'face'],
    'sample':        ['sample'],
    'scenery':       ['scenery', 'situation', 'people'],
    'scheme':        ['scheme', 'figure', 'flow', 'schematic'],
    'sign':          ['sign'],
}


class WordsFeature(Feature):

    terms = []
    term_buckets = []
    bucket_names = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def initialize_vocabulary(cls, synonyms):
        # Convert to list of tuples for persistent ordering
        mapping = sorted(synonyms.items(), key=lambda x: x[0])
        for index, (bucket, terms) in enumerate(mapping):
            # Create plain list of all terms
            cls.terms += terms
            # Remember mapping to buckets and thier names
            cls.term_buckets += [len(cls.bucket_names)] * len(terms)
            cls.bucket_names.append(bucket)

    @classmethod
    def initialize_vectorizer(cls):
        cls.vectorizer = CountVectorizer(decode_error='replace',
            strip_accents='unicode', stop_words='english', vocabulary=cls.terms)

    @classmethod
    def preprocess_text(cls, url, title, description):
        url = os.path.splitext(os.path.split(url)[1])[0]
        text = ' '.join((url, title, description))
        chunks = re.findall(r'[A-Z]?[a-z]{2,}', text)
        text = ' '.join(chunks)
        text = text.lower()
        return text

    @classmethod
    def names(cls):
        for bucket in cls.bucket_names:
            yield 'words_' + bucket

    def extract(self):
        cls = type(self)
        text = cls.preprocess_text(self.url, self.title, self.description)
        term_counts = cls.vectorizer.transform([text]).toarray()[0].tolist()
        # Aggregate term counts into buckets
        bucket_counts = [0 for _ in cls.bucket_names]
        for term, count in enumerate(term_counts):
            bucket = cls.term_buckets[term]
            bucket_counts[bucket] += count
        yield from bucket_counts


WordsFeature.initialize_vocabulary(SYNONYMS)
WordsFeature.initialize_vectorizer()
