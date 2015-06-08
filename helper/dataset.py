import os
from extraction import feature_vector, feature_names
from helper.plot import print_headline


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
