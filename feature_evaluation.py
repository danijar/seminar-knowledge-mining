import os
import numpy as np
from argparse import ArgumentParser
from helper.image import load
from helper.dataset import read_features
from feature_extraction import feature_names


def class_statistics(directory):
    filenames, features = read_features(directory)
    features = np.array(features)
    return features.mean(axis=0).tolist(), features.var(axis=0).tolist()

def dataset_statistics(root):
    classes = []
    means = []
    variances = []
    for directory in next(os.walk(root))[1]:
        statistics = class_statistics(os.path.join(root, directory))
        # Skip empty folders
        if not statistics:
            continue
        classes.append(directory)
        mean, variance = statistics
        means.append(mean)
        variances.append(variance)
    return classes, means, variances

def output_csv(filename, classes, names, statistics):
    statistics = np.rollaxis(np.array(statistics), 1)
    with open(filename, 'w') as csv:
        csv.write('feature,')
        csv.write(','.join(classes) + '\n')
        for i, name in enumerate(names):
            csv.write(name + ',')
            csv.write(','.join(map(str, statistics[i])) + '\n')


if __name__ == '__main__':
    parser = ArgumentParser(description='Measure statistics of features \
        within the images of the same class to evaluate features.')
    parser.add_argument('directory',
        help='Path to the directory containing folders for each class that \
        contain the images')
    parser.add_argument('-m', '--means', default='<directory>/means.csv',
        help='Filename of the CSV file mean values will be written to')
    parser.add_argument('-v', '--variances',
        default='<directory>/variances.csv',
        help='Filename of the CSV file variance values will be written to')
    args = parser.parse_args()

    args.means = args.means.replace('<directory>', args.directory)
    args.variances = args.variances.replace('<directory>', args.directory)

    names = feature_names()
    classes, means, variances = dataset_statistics(args.directory)
    output_csv(args.means, classes, names, means)
    output_csv(args.variances, classes, names, variances)
