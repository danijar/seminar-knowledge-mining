import os
import skimage
import json
import numpy as np
from helper.image import load, preprocess, clamp_size
from feature.feature import FeatureExtractionError
from feature.color import ColorFeature
from feature.histogram import HistogramFeature
from feature.blob import BlobFeature
from feature.gradient import GradientFeature
from feature.brief import BriefFeature
from feature.geo import GeoFeature
from feature.extension import ExtensionFeature
from feature.size import SizeFeature
from feature.words import WordsFeature
from feature.random import RandomFeature


def get_extractors(visual, textual):
    extractors = []
    if visual:
        extractors += [
            SizeFeature,
            ColorFeature,
            HistogramFeature,
            GradientFeature,
            # BlobFeature,
            # BriefFeature,
        ]
    if textual:
        extractors += [
            GeoFeature,
            ExtensionFeature,
            WordsFeature,
            # RandomFeature,
        ]
    return extractors

def feature_vector(filename, visual=True, textual=True):
    inputs = get_inputs(filename, visual, textual)
    extractors = get_extractors(visual, textual)
    features = apply_extractors(inputs, extractors)
    return list(features)

def feature_names(visual, textual):
    names = []
    for extractor in get_extractors(visual, textual):
        for name in extractor.names():
            names.append(name)
    return names

def apply_extractors(inputs, extractors):
    for extractor in extractors:
        features = list(extractor(**inputs).extract())
        # TODO: Requesting the names again every time is slow
        names = list(extractor.names())
        if len(features) != len(names):
            raise FeatureExtractionError(extractor)
        yield from features

def get_inputs(filename, visual, textual):
    """
    Return kwargs containing different image versions and DBpedia meta data
    needed to construct feature extractors.
    """
    args = {}
    args['filename'] = filename
    if visual:
        args.update(get_images(filename))
    if textual:
        args.update(get_metadata(filename))
    return args

def get_images(filename):
    original, size = load(filename)
    image = preprocess(original)
    args = {}
    args['width'] = size[0]
    args['height'] = size[1]
    args['original'] = original
    args['image'] = image
    args['gray'] = skimage.color.rgb2gray(image)
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
        print('Metadata not found', filename)
        keys = ('title', 'long', 'description', 'url', 'lat', 'extension')
        return {key: '' for key in keys}

def replace_extension(filename, extension):
    basename, _ = os.path.splitext(filename)
    return basename + '.' + extension
