from helper.preprocess import get_inputs
from feature.color import ColorFeature
from feature.histogram import HistogramFeature
from feature.blob import BlobFeature
from feature.gradient import GradientFeature
from feature.geo import GeoFeature
from feature.extension import ExtensionFeature
from feature.size import SizeFeature
from feature.words import WordsFeature


def get_extractors(visual=True, textual=True):
    extractors = []
    if visual:
        extractors += [
            ColorFeature,
            HistogramFeature,
            BlobFeature,
            GradientFeature
        ]
    if textual:
        extractors += [
            GeoFeature,
            ExtensionFeature,
            SizeFeature,
            WordsFeature
        ]
    return extractors

def feature_vector(filename):
    inputs = get_inputs(filename)
    extractors = get_extractors()
    features = apply_extractors(inputs, extractors)
    return list(features)

def feature_names():
    names = []
    for extractor in get_extractors():
        for name in extractor.names():
            names.append(name)
    return names

def apply_extractors(inputs, extractors):
    for extractor in extractors:
        yield from extractor(**inputs).extract()
