import os
from .feature import Feature
from helper.image import get_supported


class ExtensionFeature(Feature):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Try to get missing extension from filename
        if not self.extension and self.filename:
            # Split extension and remove leading dot
            self.extension = os.path.splitext(self.filename)[1][1:]

    def extract(self):
        supported = get_supported()
        assert self.extension in supported, self.extension + ' is not supported'
        for extension in supported:
            yield 1 if self.extension == extension else 0

    @classmethod
    def names(cls):
        return ['extension_' + x for x in get_supported()]
