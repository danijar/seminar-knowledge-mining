from .feature import Feature
import random


class RandomFeature(Feature):
    """
    A random feature that is useful to check if the feature evaluation works.
    Should not be used in production.
    """

    @classmethod
    def names(cls):
        return ['random']

    def extract(self):
        value = random.random()
        return [value]
