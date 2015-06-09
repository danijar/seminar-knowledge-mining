import numpy as np
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from extraction import feature_names
from sklearn.feature_selection import chi2
from helper.dataset import read_dataset, normalize
from helper.text import print_headline


def compute_chi(data, target):
    data = normalize(data)
    # chi2() requires positive values
    features = np.rollaxis(data, 1)
    for i, feature in enumerate(features):
        features[i] = feature - feature.min()
    chi_values, p_values = chi2(data, target)
    p_values = [1 - x for x in p_values]
    return chi_values, p_values

def print_chi(names, data, target):
    chi_values, p_values = compute_chi(data, target)
    chi_values_sqrt = np.sqrt(chi_values)
    max_chi_sqrt = max(chi_values_sqrt)
    print('Feature                         chi2    p-value chi       ')
    print('------------------------- ---------- ---------- ----------')
    for x in zip(names, chi_values, p_values, chi_values_sqrt):
        bar = '#' * (10 * x[3] / max_chi_sqrt) if not np.isnan(x[3]) else ''
        print('{: <25} {: >10.4f} {: >10.4f}'.format(*x), bar)

def write_chi(filename, names, data, target):
    chi_values, p_values = compute_chi(data, target)
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
    parser.add_argument('-o', '--output', default='<directory>/p-values.csv',
        help='Filename of the CSV file where p-values will be written to')
    args = parser.parse_args()

    args.output = args.output.replace('<directory>', args.directory)

    names = feature_names()
    print('')
    filenames, data, target, classes = read_dataset(args.directory)
    print_chi(names, data, target)
    write_chi(args.output, names, data, target)
    print('')
    print('Wrote CSV table to', args.output)
