from .feature import Feature


class GeoFeature(Feature):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def extract(self):
        if self.lat and self.long:
            yield 1
        else:
            yield 0

    @classmethod
    def names(cls):
        yield 'geo_exists'
