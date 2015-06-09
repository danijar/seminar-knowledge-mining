import os, shutil
import numpy as np
import matplotlib.pyplot as plt
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
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


def train_and_predict(dataset, split):
    # Convert to numpy arrays and split
    training, testing = dataset.split(split)
    # Normalize dataset
    params = training.normalize()
    # TODO: Store params
    testing.normalize(params)
    # Create an train classifier
    classifier = RandomForestClassifier(n_estimators=1000)
    classifier.fit(training.data, training.target)
    # Use model to make predictions
    predicted = classifier.predict(testing.data)
    prediction = Prediction(testing.target, predicted, testing.classes)
    return prediction


if __name__ == '__main__':
    parser = ArgumentParser(description='Learning algorithm used to classify \
        images.',
        formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('data', nargs='?',
        help='Path to the directory containing the images to learn from and \
        validate against; sub directory for each class expected')
    parser.add_argument('-t', '--test-set', default=0.25,
        help='Fraction of data used for validation')
    parser.add_argument('-s', '--save',
        help='Filename of JSON file to store extracted features and classes \
        to; can be loaded with --load')
    parser.add_argument('-l', '--load',
        help='Filename of JSON file to load extracted features and classes \
        from; mutually exclusive with positional argument data')
    parser.add_argument('-o', '--output', default='data/predicted',
        help='Folder to copy predicted images into; sub directories for all \
        classes are created')
    args = parser.parse_args()

    dataset = Dataset()
    if args.load:
        print_headline('Dataset dump')
        dataset.load(args.load)
    else:
        dataset.read(args.data)
    if args.save:
        print_headline('Dataset dump')
        dataset.save(args.save)

    prediction = train_and_predict(dataset, args.test_set)
    prediction.print_scores()
    prediction.plot_confusion_matrix()
