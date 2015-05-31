import numpy as np
from argparse import ArgumentParser
from extraction import feature_names
from sklearn.feature_selection import chi2
from helper.dataset import read_dataset
from helper.plot import print_headline


def print_chi(names, data, target):
    chi_values, _ = chi2(data, target)
    print('Feature                       chi2')
    print('-------                       ----')
    for x in zip(names, chi_values):
        print('{: <25} {: >8.4f}'.format(*x))

def write_chi(filename, names, data, target):
    chi_values, _ = chi2(data, target)
    captions = ('Feature', 'chi2')
    data = (names, chi_values)
    write_csv(filename, captions, data)

def write_csv(filename, captions, data):
    assert len(captions) == len(data)
    with open(filename, 'w') as csv:
        csv.write(','.join(captions) + '\n')
        for row in range(len(data[0])):
            csv.write(','.join(str(column[row]) for column in data) + '\n')


if __name__ == '__main__':
    parser = ArgumentParser(description='Measure statistics of features \
        within the images of the same class to evaluate features.')
    parser.add_argument('directory',
        help='Path to the directory containing folders for each class that \
        contain the images')
    parser.add_argument('-o', '--output', default='<directory>/chi2.csv',
        help='Filename of the CSV file where scores will be written to')
    args = parser.parse_args()

    args.output = args.output.replace('<directory>', args.directory)

    names = feature_names()
    filenames, data, target, classes = read_dataset(args.directory)
    print_chi(names, data, target)
    write_chi(args.output, names, data, target)
    print('')
    print('Wrote CSV table to', args.output)
