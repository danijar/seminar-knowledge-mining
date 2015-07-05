class Feature:
    """
    Represents a feature extractor that is constructued once and used to
    extract() a list of features from multiple samples.

    The constructor may have parameters, but all should have default values so
    that an empty instance can be created first and the state can be recovered
    later using `set_params()`.
    """

    def name(self):
        """
        Expected to return the name of this extractor. This gets prepended to
        the keys() and may be used for debug printing.
        """
        raise NotImplementedError

    def keys(self):
        """
        Expected to return a list or generator of names for the features. This
        maps to the list of features returned from extract(). Thus their
        lengths must match.
        """
        raise NotImplementedError

    def extract(self, sample):
        """
        Extracts features from the sample class. Expected to return a list or
        generator of floats.
        """
        raise NotImplementedError

    def get_params(self):
        """
        Parameters should represent the whole state of the feature extractor so
        that the state of the extractor can be recovered fully. Should return
        a dictionary.
        """
        return {}

    def set_params(self, params):
        """
        Resets the internal state to the dictionary obtained from get_params().
        """
        pass


class FeatureExtractionError(Exception):

    def __init__(self, extractor, message=''):
        self.extractor = extractor
        self.message = message

    def __str__(self):
        return '{} feature: {}'.format(self.extractor.name(), self.message)
