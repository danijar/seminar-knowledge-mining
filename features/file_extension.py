from .string_feature import StringFeature

class FileExtensionFeature(StringFeature):

    #predicate = 'http://commons.dbpedia.org/ontology/fileExtension'
    predicate = 'http://purl.org/dc/terms/format'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def extract(self):
        # TODO get supported formats from helper class
        values = {'image/jpeg': 0, 'image/png': 1, 'image/bmp': 2, 'image/png': 3, 'image/gif': 4, 'image/svg': 5, 'image/ico': 6}
        return values.get(self.string)

    def preprocess(self):
        #synonyms = {'jpeg': 'jpg'}
        #self.string = synonyms.get(self.string)
        return

