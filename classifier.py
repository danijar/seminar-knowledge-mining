import os, shutil
import numpy as np
import matplotlib.pyplot as plt
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score, classification_report
from sklearn.metrics import confusion_matrix
from helper.download import ensure_directory
from helper.dataset import Dataset
from helper.text import print_headline


class Prediction:

    def __init__(self, true=None, predicted=None, classes=None):
        self.true = true
        self.predicted = predicted
        self.classes = classes

    def print_scores(self):
        print_headline('Results')
        scores = classification_report(self.true, self.predicted,
            target_names=self.classes)
        print(scores)

    def plot_confusion_matrix(self):
        confusion = confusion_matrix(self.true, self.predicted)
        # Normalize range
        confusion = confusion.astype('float') / confusion.sum(axis=1)[:, np.newaxis]
        # Create figure
        plt.figure()
        plt.imshow(confusion, interpolation='nearest', cmap=plt.cm.Blues)
        plt.title('Confusion matrix')
        plt.colorbar()
        tick_marks = np.arange(len(self.classes))
        plt.xticks(tick_marks, self.classes, rotation=45)
        plt.yticks(tick_marks, self.classes)
        plt.tight_layout()
        plt.ylabel('True label')
        plt.xlabel('Predicted label')
        plt.show()


def train_and_predict(classifier, dataset, split, log=True):
    # Convert to numpy arrays and split
    training, testing = dataset.split(split, log)
    # Normalize dataset
    means, stds = training.normalize()
    # TODO: Store params
    testing.normalize(means, stds)
    # Train classifier
    classifier.fit(training.data, training.target)
    # Use model to make predictions
    predicted = classifier.predict(testing.data)
    prediction = Prediction(testing.target, predicted, testing.classes)
    return prediction

def evaluate_classifier(dataset, classifier, iterations, split):
    scores = []
    for _ in range(iterations):
        prediction = train_and_predict(classifier, dataset, split, log=False)
        score = f1_score(prediction.true, prediction.predicted,
            average='weighted')
        scores.append(score)
    worst = min(scores)
    average = sum(scores) / len(scores)
    best = max(scores)
    return worst, average, best


if __name__ == '__main__':
    parser = ArgumentParser(description='Learning algorithm used to classify \
        images.',
        formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('data',
        help='Path to the directory containing the images to learn from and \
        validate against; sub directory for each class expected')
    parser.add_argument('-t', '--test-set', type=float, default=0.25,
        help='Fraction of data used for validation')
    parser.add_argument('-s', '--save', action='store_true', default=False,
        help='Cache extracted features and classes inside data directory; can \
        be loaded with --load')
    parser.add_argument('-l', '--load', action='store_true', default=False,
        help='Load cached features and classes to skip the extraction')
    parser.add_argument('-o', '--output', default='data/predicted',
        help='Folder to copy predicted images into; sub directories for all \
        classes are created')
    args = parser.parse_args()

    dataset = Dataset()
    cached = os.path.join(args.data, 'dataset.json')
    if args.load:
        print_headline('Dataset dump')
        dataset.load(cached)
    else:
        dataset.read(args.data)
    if args.save:
        print_headline('Dataset dump')
        dataset.save(cached)

    classifier = RandomForestClassifier(n_estimators=300)
    prediction = train_and_predict(classifier, dataset, args.test_set)
    prediction.print_scores()
    prediction.plot_confusion_matrix()
