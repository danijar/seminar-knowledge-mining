from .feature import Feature


VOCABULARY = {
    'chart':      ['chart', 'diagram'],
    'cover':      ['plakat', 'einband', 'albumcover', 'titelbild'],
    'document':   ['titelseite', 'urkunde', 'dokument', 'document'],
    'drawn':      ['drawn', 'sketch', 'zeichnung', 'drawing'],
    'flag':       ['flag', 'flagge'],
    'icon':       ['symbol', 'icon'],
    'logo':       ['logo', 'marke', 'brand'],
    'map':        ['map', 'karte', 'atlas'],
    'object':     ['single', 'einzeln', 'piece', 'exemplar', 'gegenstand', 'object'],
    'painting':   ['painting', 'gemälde', 'canvas', 'composition'],
    'portrait':   ['portrait', 'person', 'face'],
    'scenery':    ['scenery', 'scape', 'szene', 'scene'],
    'scheme':     ['scheme', 'figure', 'abbildung', 'sketch', 'blueprint'],
    'screenshot': ['screenshot'],
}


class WordsFeature(Feature):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def names(cls):
        for key in VOCABULARY:
            yield 'words_' + key

    def extract(self):
        text = ' '.join(self.url, self.title, self.description)
        chunks = self.tokenize(text)
        chunks = self.stemming(chunks)
        # TODO: Use sklearn.feature_extraction.text.CountVectorizer here

    def tokenize(self, text):
        raise NotImplementedError

    def stemming(self, chunks):
        raise NotImplementedError
