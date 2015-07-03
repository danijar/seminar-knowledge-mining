from .feature import Feature, FeatureExtractionError
from helper.image import get_supported


class FormatFeature(Feature):

    def __init__(self, supported=get_supported()):
        self.supported = supported

    def name(self):
        return 'format'

    def keys(self):
        return self.supported

    def extract(self, sample):
        if sample.extension not in self.supported:
            raise FeatureExtractionError(self, 'Not supported format' +
                sample.extension)
        for extension in self.supported:
            yield 1 if extension == sample.extension else 0
