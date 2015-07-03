import os
import numpy as np
import matplotlib.pyplot as plt
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score, classification_report
from sklearn.metrics import confusion_matrix
from helper.dataset import Dataset
from helper.utility import print_headline


class Prediction:

    def __init__(self, true=None, predicted=None, labels=None):
        self.true = true
        self.predicted = predicted
        self.labels = labels

    def print_scores(self):
        print_headline('Results')
        scores = classification_report(self.true, self.predicted,
            target_names=self.labels)
        print(scores)

    def plot_confusion_matrix(self):
        confusion = confusion_matrix(self.true, self.predicted)
        # Normalize range
        confusion = (confusion.astype('float') /
            confusion.sum(axis=1)[:, np.newaxis])
        # Create figure
        plt.figure()
        plt.imshow(confusion, interpolation='nearest', cmap=plt.cm.Blues)
        plt.title('Confusion matrix')
        plt.colorbar()
        tick_marks = np.arange(len(self.labels))
        plt.xticks(tick_marks, self.labels, rotation=45)
        plt.yticks(tick_marks, self.labels)
        plt.tight_layout()
        plt.ylabel('True label')
        plt.xlabel('Predicted label')
        plt.show()


def train_and_predict(classifier, dataset, split, log=True):
    # Convert to numpy arrays and split
    training, testing = dataset.split(split, log)
    # Normalize dataset
    training.normalize()
    testing.means, testing.stds = training.means, training.stds
    testing.normalize()
    # Train classifier
    classifier.fit(training.data, training.target)
    # Use model to make predictions
    predicted = classifier.predict(testing.data)
    prediction = Prediction(testing.target, predicted, testing.labels)
    return prediction


def evaluate_classifier(dataset, classifier, iterations, split):
    # TODO: Move into performance.py
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
    parser = ArgumentParser(description='Learning algorithm used to classify '
        'images.',
        formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('features',
        help='Path to the JSON file containing extracted features of the '
        'dataset')
    parser.add_argument('-s', '--split', type=float, default=0.25,
        help='Fraction of data used for validation')
    parser.add_argument('-c', '--copy-predicted',
        default='<folder>/../<folder>-predicted/',
        help='Folder to copy predicted images into; sub directories for all '
        'labels are created; <folder> is the directory of the features file')
    args = parser.parse_args()

    if '<folder>' in args.copy_predicted:
        folder = os.path.splitext(args.features)[0]
        args.copy_predicted = args.copy_predicted.replace('<folder>', folder)

    dataset = Dataset()
    dataset.load(args.features)

    classifier = RandomForestClassifier(n_estimators=300)
    prediction = train_and_predict(classifier, dataset, args.split)
    prediction.print_scores()
    prediction.plot_confusion_matrix()
