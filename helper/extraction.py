from helper.preprocess import get_inputs
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
