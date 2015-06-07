from .string_feature import StringFeature

class GeoLocationFeature(StringFeature):

    predicate = 'http://www.w3.org/2003/01/geo/wgs84_pos#lat'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def extract(self):
        if not self.string:
            return 0
        return 1

    def preprocess(self):
        return
