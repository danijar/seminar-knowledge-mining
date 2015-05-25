import os
import numpy as np
from argparse import ArgumentParser
from helper.image import load
from feature_extraction import get_feature_vector, get_feature_names


def get_statistics_of_folder(directory):
    vectors = []
    for filename in next(os.walk(directory))[2]:
        # Only jpg support for now
        if not filename.endswith('.jpg'):
            continue
        print('  Image', filename)
        image = load(os.path.join(directory, filename))
        try:
            features = get_feature_vector(image)
            vectors.append(features)
        except:
            print('Error extracting feature vector')
    # No valid images to extract feature from
    if not vectors:
        return None
    # Numpy has convenient functions to collect statistics
    vectors = np.array(vectors)
    return vectors.mean(axis=0).tolist(), vectors.var(axis=0).tolist()

def get_statistics_of_folders(root):
    classes = []
    means = []
    variances = []
    for directory in next(os.walk(root))[1]:
        print('Directory', directory)
        statistics = get_statistics_of_folder(os.path.join(root, directory))
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

    names = get_feature_names()
    classes, means, variances = get_statistics_of_folders(args.directory)
    output_csv(args.means, classes, names, means)
    output_csv(args.variances, classes, names, variances)
