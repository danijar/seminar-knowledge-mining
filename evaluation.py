import numpy as np
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from extraction import feature_names
from sklearn.feature_selection import chi2
from helper.dataset import Dataset
from helper.text import print_headline


def compute_chi(dataset):
    dataset.normalize()
    # chi2() requires positive values
    features = np.rollaxis(dataset.data, 1)
    for i, feature in enumerate(features):
        features[i] = feature - feature.min()
    chi_values, p_values = chi2(dataset.data, dataset.target)
    p_values = [1 - x for x in p_values]
    return chi_values, p_values

def print_chi(names, dataset):
    chi_values, p_values = compute_chi(dataset)
    chi_values_sqrt = np.sqrt(chi_values)
    max_chi_sqrt = max(chi_values_sqrt)
    print('')
    print('Feature                         chi2    p-value chi       ')
    print('----------------------------------------------------------')
    for x in zip(names, chi_values, p_values, chi_values_sqrt):
        bar = '#' * (10 * x[3] / max_chi_sqrt) if not np.isnan(x[3]) else ''
        print('{: <25} {: >10.4f} {: >10.4f}'.format(*x), bar)

def write_chi(filename, names, dataset):
    chi_values, p_values = compute_chi(dataset)
    captions = ('Feature', 'chi2', 'p-value')
    data = (names, chi_values, p_values)
    write_csv(filename, captions, data)

def write_csv(filename, captions, data):
    assert len(captions) == len(data)
    with open(filename, 'w') as csv:
        csv.write(','.join(captions) + '\n')
        for row in range(len(data[0])):
            csv.write(','.join(str(column[row]) for column in data) + '\n')


if __name__ == '__main__':
    parser = ArgumentParser(description='Measure statistics of features \
        within the images of the same class to evaluate features.',
        formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('directory',
        help='Path to the directory containing folders for each class that \
        contain the images')
    parser.add_argument('-o', '--output', default='<directory>/evaluation.csv',
        help='Filename of the CSV file where p-values will be written to')
    args = parser.parse_args()

    args.output = args.output.replace('<directory>', args.directory)

    names = feature_names()
    dataset = Dataset()
    dataset.read(args.directory)
    print_chi(names, dataset)
    write_chi(args.output, names, dataset)
    print('')
    print('Wrote CSV table to', args.output)
