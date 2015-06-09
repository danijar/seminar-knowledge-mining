import os
import json
import sys
import numpy as np
from extraction import feature_vector, feature_names
from helper.image import is_supported
from helper.text import print_headline
from sklearn.preprocessing import StandardScaler


def read_features(directory):
    vector_length = len(feature_names())
    print_headline('Class: ' + os.path.basename(directory))
    count = 0
    for filename in walk_images(directory):
        try:
            features = feature_vector(os.path.join(directory, filename))
            assert len(features) == vector_length
            # Display progress
            print('Process {: <40}'.format(filename), flush=True, end='\r')
            count += 1
            yield filename, features
        except KeyboardInterrupt:
            sys.exit(1)
        except:
            print('Error extracting features from', filename)
    print('Loaded {} images'.format(count).ljust(48) + '\n')

def read_dataset(root):
    filenames = []
    data = []
    target = []
    classes = []
    for directory in walk_directories(root):
        new_class = len(classes)
        for filename, features in read_features(os.path.join(root, directory)):
            filenames.append(filename)
            data.append(features)
            target.append(new_class)
        classes.append(directory)
    return filenames, data, target, classes

def walk_directories(root):
    return next(os.walk(root))[1]

def walk_images(directory):
    """
    Generator of filenames of all supported images files in the directory.
    """
    filenames = next(os.walk(directory))[2]
    for filename in filenames:
        if is_supported(filename):
            yield filename


def normalize(data, directory=None, load=False):

    FILENAME = 'normalization.json'

    def _load(scaler, directory):
        assert directory
        filename = os.path.join(directory, FILENAME)
        try:
            with open(filename, 'r') as file_:
                params = json.load(file_)
                scaler.mean_ = np.array(params['means'])
                scaler.std_ = np.array(params['stds'])
        except:
            print('Could not load normalization parameters from', filename)
            sys.exit(1)

    def _store(scaler, directory):
        filename = os.path.join(directory, FILENAME)
        params = {
            'means': scaler.mean_.tolist(),
            'stds': scaler.std_.tolist()
        }
        with open(filename, 'w') as file_:
            json.dump(params, file_)

    scaler = StandardScaler()
    if load:
        _load(scaler, directory)
    else:
        scaler.fit(data)
        if directory:
            _store(scaler, directory)
    data = scaler.transform(data)
    return data
