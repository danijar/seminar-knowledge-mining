from .feature import Feature


class FormatFeature(Feature):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def extract(self):
        formats = ['jpg', 'jpeg', 'png']
        try:
            value = formats.index(self.extension) + 1
            yield value
        except:
            yield 0

    @classmethod
    def names(cls):
        yield 'format'
