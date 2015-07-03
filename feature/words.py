import os
import re
import itertools
from sklearn.feature_extraction.text import CountVectorizer
from scipy.sparse import coo_matrix
import snowballstemmer
from .feature import Feature, FeatureExtractionError


class WordsFeature(Feature):

    def __init__(self, samples, stopwords='english', limit=20, logging=False):
        """
        Create a vocabulary which is a mapping from bucket names to lists of
        synonyms that fall into their bucket. Stopwords is a list of words that
        are ignored for the vocabulary and defaults to a built-in english
        stopword list.
        """
        self.stopwords = stopwords
        self.stemmer = snowballstemmer.stemmer('english')
        self.tokens = re.compile(r'[A-Z]?[a-z]{2,}')
        self.logging = logging
        # Process input samples
        documents = self._texts_by_label(samples)
        self.buckets = sorted(documents.keys())
        self.overall = self._get_frequencies(self._flatten(documents.values()))
        # Compute vocabulary
        self._generate_vocabulary(documents, limit)
        # List of all terms
        self.terms = sorted(set(self._flatten(self.vocabulary.values())))
        self.vectorizer = self._create_vectorizer(self.terms)

    def name(self):
        return 'words'

    def keys(self):
        return self.buckets

    def extract(self, sample):
        # Check for metadata
        if not sample.metadata:
            raise FeatureExtractionError(self, 'Metadata not found')
        # Count words
        text = self._preprocess_text(sample.url, sample.title,
            sample.description)
        term_counts = self.vectorizer.transform([text]).toarray()[0].tolist()
        # Aggregate term counts into buckets
        counts = [0 for _ in self.buckets]
        for term_index, count in enumerate(term_counts):
            term = self.terms[term_index]
            for bucket_index, bucket in enumerate(self.buckets):
                if term in self.vocabulary[bucket]:
                    counts[bucket_index] += count
        yield from counts

    def _texts_by_label(self, samples):
        """
        Sort the samples by their label and return a directory from labels to
        lists of preprocessed text.
        """
        labels = set(sample.label for sample in samples)
        texts = {label: [] for label in labels}
        for sample in samples:
            text = self._preprocess_text(sample.url, sample.title,
                sample.description)
            texts[sample.label].append(text)
        return texts

    def _get_frequencies(self, texts):
        vectorizer = self._create_vectorizer()
        counts = vectorizer.fit_transform(texts)
        counts = coo_matrix.sum(counts, axis=0).tolist()[0]
        amount = sum(counts)
        mapping = vectorizer.vocabulary_
        freqs = {term: counts[i] / amount for term, i in mapping.items()}
        return freqs

    def _get_top_words(self, texts, limit):
        freqs = self._get_frequencies(texts)
        freqs = self._compute_tfidf(freqs)
        freqs = sorted(freqs.items(), key=lambda x: x[1], reverse=True)
        if len(freqs) > limit:
            freqs = freqs[:limit]
        words, freqs = [x[0] for x in freqs], [x[1] for x in freqs]
        return words, freqs

    def _compute_tfidf(self, frequencies):
        """
        Returns a copy of the frequencies mapping to TFIDF scores instead of
        the frequencies. TFIDF is a measure for how unique the frequency is
        compared to the overall dataset.
        """
        assert all(0 <= x <= 1 for x in frequencies.values())
        assert all(0 <= x <= 1 for x in self.overall.values())
        assert all(term in self.overall for term in frequencies)
        adjusted = {}
        for term in frequencies:
            score = frequencies[term] / (1 - self.overall[term])
            adjusted[term] = score
        return adjusted

    def _create_vectorizer(self, terms=None):
        args = {}
        args['decode_error'] = 'replace'
        args['strip_accents'] = 'unicode'
        args['stop_words'] = self.stopwords
        if terms:
            args['vocabulary'] = terms
        return CountVectorizer(**args)

    def _preprocess_text(self, url, title, description):
        url = os.path.splitext(os.path.split(url)[1])[0]
        text = ' '.join((url, title, description))
        # Tokenize
        chunks = self.tokens.findall(text)
        # Stemming
        chunks = self.stemmer.stemWords(chunks)
        # Combine for input in CountVectorizer
        text = ' '.join(chunks)
        text = text.lower()
        return text

    def _flatten(self, list_of_lists):
        return list(itertools.chain.from_iterable(list_of_lists))

    def _generate_vocabulary(self, documents, limit):
        self.vocabulary = {key: [] for key in self.buckets}
        for key, texts in documents.items():
            words, freqs = self._get_top_words(texts, limit)
            self.vocabulary[key] = words
            self._log(key + ':', ', '.join('{} {:.3f}'.format(x, y)
                for x, y in zip(words, freqs)) + '\n')

    def _log(self, *args, **kwargs):
        if self.logging:
            print(*args, **kwargs)
