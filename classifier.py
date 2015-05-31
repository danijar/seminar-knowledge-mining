import os, shutil
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
from sklearn.metrics import confusion_matrix, classification_report
from argparse import ArgumentParser
from helper.download import ensure_directory
from helper.dataset import read_dataset
from extraction import feature_names
import matplotlib.pyplot as plt


def print_headline(text):
    underline = '-' * len(text)
    print('\n' + text + '\n' + underline)

def split_dataset(data, target):
    train_data, test_data, train_target, test_target = train_test_split(data, target)
    print_headline('Results')
    print('Training set size', train_target.shape[0])
    print('Test set size', test_target.shape[0])
    print('Feature vector length', train_data.shape[1])
    return train_data, test_data, train_target, test_target

def compare_target(predictions, references):
    correct = 0
    for prediction, reference in zip(predictions, references):
        if prediction == reference:
            correct += 1
    precision = correct / len(predictions)
    print('Prediction precision', precision)

def copy_classified(output, paths, classes):
    map(classes, ensure_directory)
    for index, path in enumerate(paths):
        basename = os.path.basename(path)
        destination = os.path.join(output, basename)
        shutil.copyfile(path, destination)

def get_confusion(test_target, predicted):
    """
    Returns a confusion matrix
    """
    confusion = confusion_matrix(test_target, predicted)
    # Normalize range
    confusion = confusion.astype('float') / confusion.sum(axis=1)[:, np.newaxis]
    print(confusion)
    return confusion

def print_scores(test_target, predicted, classes):
    scores = classification_report(test_target, predicted, target_names=classes)
    print(scores)

def plot_confusion(confusion, classes):
    plt.figure()
    plt.imshow(confusion, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title('Confusion matrix')
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.show()


if __name__ == '__main__':
    parser = ArgumentParser(description='Learning algorithm used to classify \
        images.')
    parser.add_argument('data',
        help='Path to the directory containing the images to learn from and \
        validate against; sub directory for each class expected')
    parser.add_argument('-s', '--split', default=0.25,
        help='Fraction of data used for validation')
    parser.add_argument('-o', '--output', default='data/predicted',
        help='Folder to copy predicted images into; sub directories for all \
        classes are created')
    args = parser.parse_args()

    # Read dataset
    filenames, data, target, classes = read_dataset(args.data)
    # Convert to numpy arrays and split
    data = np.array(data)
    target = np.array(target)
    train_data, test_data, train_target, test_target = split_dataset(data, target)
    # Create an train classifier
    classifier = OneVsRestClassifier(LinearSVC())
    classifier.fit(train_data, train_target)
    # Use model to make predictions
    predicted = classifier.predict(test_data)
    # Evaluate results
    compare_target(predicted, test_target)
    print_scores(test_target, predicted, classes)
    confusion = get_confusion(test_target, predicted)
    #plot_confusion(confusion, classes)
    #copy_classified(args.output, filenames, classes)
