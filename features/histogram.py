import numpy as np
import skimage
from .feature import Feature


class HistogramFeature(Feature):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hsv = skimage.color.rgb2hsv(self.image)
        self.bins = 5

    def names(self):
        for name in ['hue', 'saturation', 'value']:
            yield from self.multiple_names('histogram_' + name, self.bins)

    def extract(self):
        for i in range(3):
            channel = self.hsv[:,:,i]
            histogram, edges = np.histogram(channel, bins=self.bins,
                range=(0, 1), density=True)
            normalized = histogram * np.diff(edges)
            yield from normalized
