from .feature import Feature


class GeoFeature(Feature):

    def name(self):
        return 'geo'

    def keys(self):
        yield 'exists'

    def extract(self, sample):
        yield int(bool(sample.lat and sample.long))
