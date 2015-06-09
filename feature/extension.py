from .feature import Feature
from helper.image import get_supported


class ExtensionFeature(Feature):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def extract(self):
        supported = get_supported()
        assert self.extension in supported
        for extension in supported:
            yield 1 if self.extension == extension else 0

    @classmethod
    def names(cls):
        return ['extension_' + x for x in get_supported()]
