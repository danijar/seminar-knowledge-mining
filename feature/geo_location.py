from .feature import Feature


class GeoLocationFeature(Feature):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def extract(self):
        return int(self.lat and self.long)

    @classmethod
    def names(cls):
        return ['geo_location']
