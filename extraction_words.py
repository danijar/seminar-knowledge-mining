import numpy as np
import pandas as pd
from pprint import pprint
from helper.format import is_nan
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from features.label import LabelFeature
from features.archive_title import ArchiveTitleFeature


def get_words_features():
    return [
        LabelFeature,
        ArchiveTitleFeature
    ]

def print_vocabulary(features, vocabulary):
    """
    Sum up the counts of each vocabulary word
    """
    print('Bags:')
    dist = np.sum(features, axis=0)
    for tag, count in zip(vocabulary, dist):
        print(count, tag)

def print_report(vectorizer, features):
    vocabulary = vectorizer.get_feature_names()
    print(''.join(['=' for i in range(0,30)]))
    print('n_samples: %d, n_features: %d' % features.shape)
    print_vocabulary(features, vocabulary)#

def preprocess(texts, feature):
    results = []
    for text in texts:
        processed_text = '' if is_nan(text) else text
        for func in feature.normalize():
            processed_text = func(processed_text)
        results.append(processed_text)
    return results

if __name__ == '__main__':

    metadata_file = 'metadata/commons.csv'
    print('Loading metadata from {}'.format(metadata_file))
    train = pd.read_csv(metadata_file, header=0, delimiter=';')
    num_files = len(train['filename'])

    for feature in get_words_features():
        print('Evaluating', feature.predicate)
        print('Preprocessing text')
        texts = train[feature.predicate]
        cleaned_texts = preprocess(texts, feature)

        print('Extracting features from the dataset')
        vectorizer = CountVectorizer()
        feature_vector = vectorizer.fit_transform(cleaned_texts)
        feature_vector = feature_vector.toarray()

        print_report(vectorizer, feature_vector)

        # todo training
        #print "Training the random forest..."
        #forest = RandomForestClassifier(n_estimators = 100)
        #forest = forest.fit( train_data_features, train["category"] )
        # todo split
        # todo test
