from .feature import Feature


class GeoLocationFeature(Feature):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def extract(self):
        if self.lat and self.long:
            return [1]
        else:
            return [0]

    @classmethod
    def names(cls):
        return ['geo_location']
