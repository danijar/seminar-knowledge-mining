import numpy as np
from .feature import Feature


class ColorFeature(Feature):

    def name(self):
        return 'color'

    def keys(self):
        yield 'distinct_amount'
        rgb = 'red', 'green', 'blue'
        yield from ['mean_' + x for x in rgb]
        yield from ['variance_' + x for x in rgb]

    def extract(self, sample):
        pixels = sample.image.reshape(-1, sample.image.shape[-1])
        channels = np.rollaxis(sample.original, 2)
        yield self.amount(pixels)
        yield from self.means(channels)
        yield from self.variances(channels)

    def amount(self, pixels):
        return len(np.unique(pixels))

    def means(self, channels):
        return [x.mean() for x in channels]

    def variances(self, channels):
        return [x.var() for x in channels]
