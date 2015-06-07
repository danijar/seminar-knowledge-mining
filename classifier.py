import os, shutil
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from helper.download import ensure_directory
from helper.dataset import read_dataset
from extraction import feature_names
from helper.plot import plot_confusion_matrix
from helper.plot import print_headline


def split_dataset(data, target):
    train_data, test_data, train_target, test_target = train_test_split(data, target)
    print_headline('Results')
    print('Training set size', train_target.shape[0])
    print('Test set size', test_target.shape[0])
    print('Feature vector length', train_data.shape[1])
    return train_data, test_data, train_target, test_target

def print_scores(labels, predicted, classes):
    scores = classification_report(labels, predicted, target_names=classes)
    print(scores)

def copy_predicted(output, paths, classes):
    map(classes, ensure_directory)
    for index, path in enumerate(paths):
        basename = os.path.basename(path)
        destination = os.path.join(output, basename)
        shutil.copyfile(path, destination)

def train_and_predict(root):
    # Read dataset
    filenames, data, target, classes = read_dataset(root)
    # Convert to numpy arrays and split
    data = np.array(data)
    target = np.array(target)
    train_data, test_data, train_target, test_target = split_dataset(data, target)
    # Create an train classifier
    trees=100
    classifier = RandomForestClassifier(n_estimators=trees)
    classifier.fit(train_data, train_target)
    # Use model to make predictions
    predicted = classifier.predict(test_data)
    return test_target, predicted, classes


if __name__ == '__main__':
    parser = ArgumentParser(description='Learning algorithm used to classify \
        images.',
        formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('data',
        help='Path to the directory containing the images to learn from and \
        validate against; sub directory for each class expected')
    parser.add_argument('-s', '--split', default=0.25,
        help='Fraction of data used for validation')
    parser.add_argument('-o', '--output', default='data/predicted',
        help='Folder to copy predicted images into; sub directories for all \
        classes are created')
    args = parser.parse_args()

    labels, predicted, classes = train_and_predict(args.data)
    print_scores(labels, predicted, classes)
    #plot_confusion_matrix(labels, predicted, classes)
    #copy_predicted(args.output, filenames, classes)
