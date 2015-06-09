import numpy as np
from .feature import Feature


class ColorFeature(Feature):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pixels = self.image.reshape(-1, self.image.shape[-1])
        self.channels = np.rollaxis(self.original, 2)

    @classmethod
    def names(cls):
        yield 'color_distinct_amount'
        rgb = 'red', 'green', 'blue'
        yield from ['color_mean_' + x for x in rgb]
        yield from ['color_variance_' + x for x in rgb]

    def extract(self):
        yield self.amount()
        yield from self.means()
        yield from self.variances()

    def amount(self):
        return len(np.unique(self.pixels))

    def means(self):
        return [x.mean() for x in self.channels]

    def variances(self):
        return [x.var() for x in self.channels]
