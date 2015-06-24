class Feature:

    def __init__(self, **kwargs):
        allowed = ('width', 'height', 'original', 'image', 'gray', 'filename',
            'url', 'extension', 'title', 'description', 'lat', 'long')
        assert all(arg in allowed for arg in kwargs.keys())
        self.__dict__.update(kwargs)

    @classmethod
    def names(cls):
        raise NotImplementedError

    def extract(self):
        raise NotImplementedError

    def show(self):
        raise NotImplementedError

    def validate(self):
        assert len(list(type(self).names())) == len(list(self.extract()))

    @staticmethod
    def multiple_names(name, amount):
        """
        Helper function to generate a range of names with the numbers from 0 to
        amount being appended.
        """
        for i in range(amount):
            yield '{}_{}'.format(name, i)


class FeatureExtractionError(Exception):

    def __init__(self, extractor):
        self.extractor = extractor

    def __str__(self):
        return repr(self.extractor)
