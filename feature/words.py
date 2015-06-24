import re
import os
from .feature import Feature
from helper.vocabulary import create_vectorizer, preprocess_text, load_vocabulary


class WordsFeature(Feature):

    _vocabulary = []
    _buckets = []
    _terms = []
    _vectorizer = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def load_vocabulary(cls, filename):
        cls._vocabulary, cls._buckets, cls._terms = load_vocabulary(filename)
        cls._vectorizer = create_vectorizer(cls._terms)

    @classmethod
    def ensure_vocabulary(cls):
        assert cls._vectorizer, 'Class must be initialized with load_vocabulary()'

    @classmethod
    def names(cls):
        cls.ensure_vocabulary()
        for bucket in cls._buckets:
            yield 'words_' + bucket

    def extract(self):
        cls = type(self)
        cls.ensure_vocabulary()
        text = preprocess_text(self.url, self.title, self.description)
        term_counts = cls._vectorizer.transform([text]).toarray()[0].tolist()
        # Aggregate term counts into buckets
        counts = [0 for _ in cls._buckets]
        for term_index, count in enumerate(term_counts):
            term = cls._terms[term_index]
            for bucket_index, bucket in enumerate(cls._buckets):
                if term in cls._vocabulary[bucket]:
                    counts[bucket_index] += count
        yield from counts
