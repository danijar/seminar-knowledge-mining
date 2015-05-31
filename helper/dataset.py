import os
from helper.image import load
from extraction import feature_vector


def print_headline(text):
    underline = '-' * len(text)
    print('\n' + text + '\n' + underline)

def read_images(directory):
    print_headline('Class ' + os.path.basename(directory))
    for filename in next(os.walk(directory))[2]:
        print('Image', filename)
        image = load(os.path.join(directory, filename))
        yield filename, image

def read_features(directory):
    filenames = []
    data = []
    for filename, image in read_images(directory):
        try:
            features = feature_vector(image)
            filenames.append(os.path.join(directory, filename))
            data.append(features)
        except:
            print('Error extracting feature vector')
    # No valid images to extract feature from
    if not data:
        return None
    return filenames, data

def read_dataset(root):
    filenames = []
    data = []
    target = []
    classes = []
    for directory in next(os.walk(root))[1]:
        result = read_features(os.path.join(root, directory))
        if not result:
            continue
        names, features = result

        filenames += names
        data += features
        target += [len(classes)] * len(features)
        classes.append(directory)
    return filenames, data, target, classes
