import numpy as np
import skimage.color


class Feature:

    def __init__(self, **kwargs):
        # Allow empty creation for calling names()
        if not kwargs:
            return
        expected = ('image', 'original', 'gray', 'channels', 'pixels', 'filename')
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
