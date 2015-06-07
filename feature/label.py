from .string_feature import StringFeature
from helper.format import strip_digits, strip_extension

class LabelFeature(StringFeature):

    predicate = 'http://www.w3.org/2000/01/rdf-schema#label'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def extract(self):
        return self.string

    def normalize():
        return [
            strip_digits,
            strip_extension
        ]
