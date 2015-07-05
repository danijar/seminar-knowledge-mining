import os
import json
import traceback
import sys
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
from helper.sample import Sample
from feature.feature import FeatureExtractionError
from helper.image import is_supported, UnsupportedImageError, ImageLoadingError


class Dataset:

    def __init__(self, logging=False):
        self.logging = logging
        self.data = None
        self.target = None
        self.labels = None
        self.samples = None
        self.means = None
        self.stds = None

    def read(self, root, extractors):
        self.data, self.target, self.labels = [], [], []
        self._read_samples(root)
        self.extractors = extractors
        self.features = list(self._feature_names())
        for index, sample in enumerate(self.samples):
            # Display progress
            name = sample.filename[len(root):]
            self._log_progress(name, index, len(self.samples))
            # Find label index
            if sample.label not in self.labels:
                self.labels.append(sample.label)
            target = self.labels.index(sample.label)
            # Extract features
            features = self._feature_vector(sample)
            if features:
                self.data.append(features)
                self.target.append(target)
        self._log('Processed', len(self.data), 'samples', ' ' * 61)
        self.data = np.array(self.data)
        self.target = np.array(self.target)
        self._validate()

    def load(self, filename):
        # TODO: Load parameters of feature extractors
        self._log('Load dataset from', filename)
        with open(filename, 'r') as file_:
            content = json.load(file_)
            self.data = np.array(content['data'])
            self.target = np.array(content['target'])
            self.labels = content['labels']
            self.features = content['features']
            self.means = content['means']
            self.stds = content['stds']
        self._validate()
        self._log('Done (' + str(len(self.target)) + ')')

    def save(self, filename):
        # TODO: Store parameters of feature extractors
        self._log('Save dataset of', len(self.target), 'samples to', filename)
        content = {}
        content['data'] = self.data.tolist()
        content['target'] = self.target.tolist()
        content['labels'] = self.labels
        content['features'] = self.features
        content['means'] = self.means
        content['stds'] = self.stds
        with open(filename, 'w') as file_:
            json.dump(content, file_)
        self._log('Done')

    def split(self, split=0.25, log=True):
        """
        Return two new Dataset instances containing the training data and
        testing data. Filenames are not stored in the new instances.
        """
        splitted = train_test_split(self.data, self.target, test_size=split)
        train_data, test_data, train_target, test_target = splitted
        self._log('Training set size', train_target.shape[0])
        self._log('Test set size', test_target.shape[0])
        self._log('Feature vector length', train_data.shape[1])
        training = self._create_subset(train_data, train_target)
        testing = self._create_subset(test_data, test_target)
        return training, testing

    def normalize(self):
        """
        Normalize dataset either from its own statistical properties or from
        external one. In the second case, both means and stds must be provided.
        """
        scaler = StandardScaler()
        assert bool(self.means is None) == bool(self.stds is None)
        if self.means and self.stds:
            scaler.mean_ = np.array(self.means)
            scaler.std_ = np.array(self.stds)
        else:
            scaler.fit(self.data)
            self.means = scaler.mean_.tolist()
            self.stds = scaler.std_.tolist()
        self.data = scaler.transform(self.data, copy=False)

    def _read_samples(self, root):
        assert os.path.isdir(root)
        row = '| {: <20} | {: >10} |'
        self._log(row.format('label', 'samples'))
        self._log(row.format('-' * 20, '-' * 10))
        self.samples = []
        for label in self._walk_directories(root):
            directory = os.path.join(root, label)
            filenames = list(self._walk_images(directory))
            self._log(row.format(label, str(len(filenames))))
            for filename in filenames:
                full_filename = os.path.join(directory, filename)
                sample = Sample(full_filename, label)
                self.samples.append(sample)
        self._log('')
        return self.samples

    def _walk_directories(self, root):
        """
        Generator over the direct sub-directories of the root directory.
        """
        return next(os.walk(root))[1]

    def _walk_images(self, directory):
        """
        Generator over the filenames of all supported images files in
        the directory.
        """
        filenames = next(os.walk(directory))[2]
        for filename in filenames:
            if is_supported(filename):
                yield filename

    def _feature_names(self):
        for extractor in self.extractors:
            name = extractor.name()
            for key in extractor.keys():
                yield name + '_' + key

    def _feature_vector(self, sample):
        # Extract features
        combined = []
        for extractor in self.extractors:
            features = self._apply_extractor(sample, extractor)
            if not features:
                return None
            combined += features
        return combined

    def _apply_extractor(self, sample, extractor):
        try:
            features = extractor.extract(sample)
            features = list(map(float, features))
            self._validate_extraction(features, extractor)
            return features
        except KeyboardInterrupt:
            sys.exit(1)
        except UnsupportedImageError:
            self._log('\nUnsupported image format')
        except ImageLoadingError:
            self._log('\nError opening image')
        except FeatureExtractionError as extractor:
            self._log('\nError extracting features in', extractor)
            traceback.print_exc()

    def _create_subset(self, data, target):
        dataset = Dataset()
        dataset.data = data
        dataset.target = target
        dataset.labels = self.labels
        dataset.features = self.features
        return dataset

    def _validate(self):
        assert len(self.data) == len(self.target)
        assert isinstance(self.features[0], str)

    def _validate_extraction(self, features, extractor):
        len_features = len(list(features))
        len_keys = len(list(extractor.keys()))
        if len_features != len_keys:
            raise FeatureExtractionError(extractor, 'Features from {} '
                'extractor of length {} do not match amount of keys {}'.format(
                extractor.name(), len_features, len_keys))

    def _log(self, *args, **kwargs):
        if self.logging:
            print(*args, **kwargs)

    def _log_progress(self, name, current, overall):
        name = name[:58] + (name[58:] and '...')
        percent = current * 100 // overall
        self._log('Process [{: >3}%] {: <61}'.format(percent, name),
            flush=True, end='\r')
