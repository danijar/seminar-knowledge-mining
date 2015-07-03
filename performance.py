from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from classifier import evaluate_classifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC, LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.lda import LDA
from sklearn.dummy import DummyClassifier
from helper.dataset import Dataset


def get_classifiers():
    return {
        'Nearest Neighbors': KNeighborsClassifier(),
        'Linear SVM': LinearSVC(),
        'RBF SVM': SVC(),
        'RBF SVM Weighted': SVC(class_weight='auto'),
        'LDA': LDA(),
        'Random Forest 10': RandomForestClassifier(10),
        'Random Forest 100': RandomForestClassifier(100),
        'Dummy Classifier Random': DummyClassifier(strategy='uniform'),
        'Dummy Classifier Weighted': DummyClassifier(strategy='stratified')
    }


if __name__ == '__main__':
    parser = ArgumentParser(description='Train and validate classifiers '
        'multiple time and get statistics about their performance.',
        formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('features',
        help='Path to the directory containing folders for each class that '
        'contain the images and metadata files')
    parser.add_argument('-s', '--split', type=float, default=0.25,
        help='Fraction of data used for validation')
    parser.add_argument('-i', '--iterations', type=int, default=20,
        help='Number of times each algorithm is trained and tested')
    args = parser.parse_args()

    dataset = Dataset()
    dataset.load(args.features)

    results = {}
    for name, classifier in get_classifiers().items():
        result = evaluate_classifier(dataset, classifier, args.iterations,
            args.split)
        results[name] = result

    results = sorted(results.items(), key=lambda x: x[1][1], reverse=True)
    for name, (worst, average, best) in results:
        print('{name: <35} {worst: 4.2f} {average: 4.2f} {best: 4.2f}'.format(
            **locals()))
