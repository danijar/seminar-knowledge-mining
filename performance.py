from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from classifier import evaluate_classifier
from helper.dataset import Dataset
from sklearn.datasets import make_moons, make_circles, make_classification
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC, LinearSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.lda import LDA
from sklearn.dummy import DummyClassifier


def get_classifiers():
    return {
        'Nearest Neighbors': KNeighborsClassifier(),
        'Linear SVM': LinearSVC(),
        'RBF SVM': SVC(),
        'RBF SVM Weighted': SVC(class_weight='auto'),
        'Decision Tree': DecisionTreeClassifier(),
        'Naive Bayes': GaussianNB(),
        'LDA': LDA(),
        'Random Forest 10': RandomForestClassifier(10),
        'Random Forest 100': RandomForestClassifier(100),
        'Dummy Classifier Random': DummyClassifier(strategy='uniform'),
        'Dummy Classifier Weighted': DummyClassifier(strategy='stratified')
    }


if __name__ == '__main__':
    parser = ArgumentParser(description='Train and validate classifiers \
        multiple time and get statistics about their performance.',
        formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('dataset',
        help='Filename of dataset dump in JSON format')
    parser.add_argument('-s', '--split', type=float, default=0.25,
        help='Fraction of data used for validation')
    parser.add_argument('-i', '--iterations', type=int, default=20,
        help='Number of times each algorithm is trained and tested')
    args = parser.parse_args()

    dataset = Dataset()
    dataset.load(args.dataset)

    results = {}
    for name, classifier in get_classifiers().items():
        result = evaluate_classifier(dataset, classifier, args.iterations, args.split)
        results[name] = result

    results = sorted(results.items(), key=lambda x: x[1][1], reverse=True)
    for name, (worst, average, best) in results:
        print('{name: <35} {worst: 4.2f} {average: 4.2f} {best: 4.2f}'.format(**locals()))
