from .feature import Feature


class SizeFeature(Feature):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def extract(self):
        width = self.original.shape[0]
        height = self.original.shape[1]
        yield width
        yield height
        yield width / height

    @classmethod
    def names(cls):
        yield 'external_width'
        yield 'external_height'
        yield 'external_ratio'
