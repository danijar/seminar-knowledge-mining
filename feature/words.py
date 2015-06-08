from .feature import Feature


# TODO: Load vocabulary from JSON file here


class WordsFeature(Feature):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def names(cls):
        for key in vocabulary:
            yield 'words_' + key

    def extract(self):
        pass
