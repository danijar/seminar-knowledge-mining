class Feature:

    def __init__(self, **kwargs):
        expected = ('image', 'original', 'gray', 'filename', 'url',
            'extension', 'title', 'description', 'lat', 'long')
        assert set(kwargs.keys()) == set(expected)
        self.__dict__.update(kwargs)

    @classmethod
    def names(cls):
        raise NotImplementedError

    def extract(self):
        raise NotImplementedError

    def show(self):
        raise NotImplementedError

    @staticmethod
    def multiple_names(name, amount):
        """
        Helper function to generate a range of names with the numbers from 0 to
        amount being appended.
        """
        for i in range(amount):
            yield '{}_{}'.format(name, i)
