
class StringFeature:

    def __init__(self, string):
        self.string = string.lower()

    def extract(self):
        raise NotImplementedError
