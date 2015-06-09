import os
import json
import numpy as np
from extraction import feature_vector, feature_names
from helper.plot import print_headline
from sklearn.preprocessing import StandardScaler


def read_features(directory):
    vector_length = len(feature_names())
    print_headline('Class ' + os.path.basename(directory))
    for filename in next(os.walk(directory))[2]:
        # Skip metadata files
        if filename.endswith('.json'):
            continue
        print('Image', filename)
        try:
            features = feature_vector(os.path.join(directory, filename))
            assert len(features) == vector_length
            yield filename, features
        except:
            print('Error extracting feature vector')

def read_dataset(root):
    filenames = []
    data = []
    target = []
    classes = []
    for directory in next(os.walk(root))[1]:
        new_class = len(classes)
        for filename, features in read_features(os.path.join(root, directory)):
            filenames.append(filename)
            data.append(features)
            target.append(new_class)
        classes.append(directory)
    return filenames, data, target, classes

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
