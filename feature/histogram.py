import numpy as np
from .feature import Feature


class HistogramFeature(Feature):

    def __init__(self, bins=8):
        self.bins = bins

    def name(self):
        return 'histogram'

    def keys(self):
        for name in ['hue', 'saturation', 'value']:
            yield from ['{}_{!s}'.format(name, x) for x in range(self.bins)]

    def extract(self, sample):
        for i in range(3):
            channel = sample.hsv[:, :, i]
            histogram, edges = np.histogram(channel, bins=self.bins,
                range=(0, 1), density=True)
            normalized = histogram * np.diff(edges)
            yield from normalized
