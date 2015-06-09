import os
import skimage
import json
import numpy as np
from helper.image import load, preprocess


def get_inputs(filename):
    """
    Return kwargs containing different image versions and DBpedia meta data
    needed to construct feature extractors.
    """
    args = {}
    args['filename'] = filename
    args.update(get_visual(filename))
    args.update(get_metadata(filename))
    return args

def get_visual(filename):
    original = load(filename)
    image = preprocess(original)
    args = {}
    args['original'] = original
    args['image']    = image
    args['gray']     = skimage.color.rgb2gray(image)
    # Define images as write only since they're shared between extractors
    for name in args:
        if args[name] is np.ndarray:
            args[name].setflags(write=False)
    return args

def get_metadata(filename):
    """
    Given an image filename, load it's metadata from the related JSON file.
    """
    filename = replace_extension(filename, 'json')
    try:
        with open(filename) as file_:
            metadata = json.load(file_)
            return metadata
    except:
        print('Medata not found', filename)
        keys = ('title', 'long', 'description', 'url', 'lat', 'extension')
        return {key: '' for key in keys}

def replace_extension(filename, extension):
    basename, _ = os.path.splitext(filename)
    return basename + '.' + extension
