from .feature import Feature


class SizeFeature(Feature):

    def name(self):
        return 'size'

    def keys(self):
        yield 'width'
        yield 'height'
        yield 'ratio'

    def extract(self, sample):
        yield sample.width
        yield sample.height
        yield sample.width / sample.height
