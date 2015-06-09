import os
import json
import sys
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
from extraction import feature_vector, feature_names
from helper.image import is_supported
from helper.text import print_headline


class Dataset:

    def __init__(self, data=None, target=None, classes=None, filenames=None):
        self.data = data
        self.target = target
        self.classes = classes
        self.filenames = filenames

    def read(self, root):
        data = []
        target = []
        self.classes = []
        self.filenames = []
        for directory in self._walk_directories(root):
            new_class = len(self.classes)
            directory_path = os.path.join(root, directory)
            for filename, features in self._read_features(directory_path):
                self.filenames.append(filename)
                data.append(features)
                target.append(new_class)
            self.classes.append(directory)
        self.data = np.array(data)
        self.target = np.array(target)
        self._assert_length()

    def load(self, filename):
        with open(filename, 'r') as file_:
            content = json.load(file_)
            self.data = np.array(content['data'])
            self.target = np.array(content['target'])
            self.classes = content['classes']
            self.filenames = content['filenames']
        self._assert_length()
        print('Loaded dataset with ', len(self.target), ' samples from', filename)

    def save(self, filename):
        content = {}
        content['data'] = self.data.tolist()
        content['target'] = self.target.tolist()
        content['classes'] = self.classes
        content['filenames'] = self.filenames
        with open(filename, 'w') as file_:
            json.dump(content, file_)
            print('Saved dataset with ', len(self.target), ' samples to', filename)

    def split(self, split=0.25, log=True):
        """
        Return two new Dataset instances containing the training data and
        testing data. Filenames are not stored in the new instances.
        """
        splitted = train_test_split(self.data, self.target, test_size=split)
        train_data, test_data, train_target, test_target = splitted
        if log:
            print_headline('Dataset Split')
            print('Training set size', train_target.shape[0])
            print('Test set size', test_target.shape[0])
            print('Feature vector length', train_data.shape[1])
        training = Dataset(train_data, train_target, self.classes)
        testing = Dataset(test_data, test_target, self.classes)
        return training, testing

    def normalize(self, means=None, stds=None):
        """
        Normalize dataset either from its own statistical properties or from
        external one. In the second case, both means and stds must be provided.
        """
        scaler = StandardScaler()
        assert (means is None) == (stds is None)
        if means and stds:
            scaler.mean_ = np.array(means)
            scaler.std_ = np.array(stds)
        else:
            scaler.fit(self.data)
        self.data = scaler.transform(self.data, copy=False)
        return scaler.mean_.tolist(), scaler.std_.tolist()

    def _read_features(self, directory):
        vector_length = len(feature_names())
        print_headline('Class: ' + os.path.basename(directory))
        count = 0
        for filename in self._walk_images(directory):
            try:
                features = feature_vector(os.path.join(directory, filename))
                assert len(features) == vector_length
                # Display progress
                print('Process {: <50}'.format(filename), flush=True, end='\r')
                count += 1
                yield filename, features
            except KeyboardInterrupt:
                sys.exit(1)
            except:
                print('Error extracting features from', filename)
        print('Loaded {} images'.format(count).ljust(58))

    def _walk_directories(self, root):
        return next(os.walk(root))[1]

    def _walk_images(self, directory):
        """
        Generator of filenames of all supported images files in the directory.
        """
        filenames = next(os.walk(directory))[2]
        for filename in filenames:
            if is_supported(filename):
                yield filename

    def _assert_length(self):
        lengths = list(map(len, [self.filenames, self.data, self.target]))
        assert lengths.count(lengths[0]) == len(lengths)
