from .string_feature import StringFeature
from helper.format import strip_digits


class ArchiveTitleFeature(StringFeature):

    predicate = 'http://commons.dbpedia.org/property/archiveTitle'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def extract(self):
        return self.string

    def normalize():
        return [
            strip_digits
        ]
