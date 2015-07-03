import os
import numpy as np
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from sklearn.feature_selection import chi2
from helper.dataset import Dataset


def compute_chi(dataset):
    dataset.normalize()
    # chi2() requires positive values
    features = np.rollaxis(dataset.data, 1)
    for i, feature in enumerate(features):
        features[i] = feature - feature.min()
    chi2s, ps = chi2(dataset.data, dataset.target)
    ps = [1 - x for x in ps]
    chis = list(map(np.sqrt, chi2s))
    return ps, chis


def print_chi(dataset):
    ps, chis = compute_chi(dataset)
    max_chi = max(chis)
    print('')
    print('Feature                          chi     p       chi       ')
    print('-----------------------------------------------------------')
    for x in zip(dataset.features, chis, ps):
        chi = x[1] if not np.isnan(x[1]) else 0
        bar = '#' * int(10 * chi / max_chi)
        print('{: <25} {: >10.4f} {: >10.4f}'.format(*x), bar)
    print('')


def write_chi(filename, dataset):
    ps, chis = compute_chi(dataset)
    captions = ('Feature', 'chi', 'p')
    data = (dataset.features, chis, ps)
    write_csv(filename, captions, data)


def write_csv(filename, captions, data):
    assert len(captions) == len(data)
    assert all(len(x) == len(data[0]) for x in data)
    with open(filename, 'w') as csv:
        csv.write(','.join(captions) + '\n')
        for row in range(len(data[0])):
            csv.write(','.join(str(column[row]) for column in data) + '\n')


if __name__ == '__main__':
    parser = ArgumentParser(description='Measure statistics of features '
        'within the images of the same class to evaluate features.',
        formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('features',
        help='Path to the JSON file containing extracted features of the '
        'dataset')
    parser.add_argument('-o', '--output', default='<folder>/evaluation.csv',
        help='Filename of the CSV file where p-values will be written to; '
        '<folder> is the directory of the features file')
    args = parser.parse_args()

    folder = os.path.splitext(os.path.split(args.features)[0])[0]
    args.output = args.output.replace('<folder>', folder)

    dataset = Dataset()
    dataset.load(args.features)

    print_chi(dataset)
    print('Write CSV table to', args.output)
    write_chi(args.output, dataset)
    print('Done')
