from .feature import Feature
import random


class RandomFeature(Feature):
    """
    A random feature that is useful to check if the feature evaluation works.
    Should not be used in production.
    """

    def name(self):
        return 'random'

    def keys(self):
        yield 'random'

    def extract(self, sample):
        yield random.random()
