import skimage.feature
import numpy as np
from .feature import Feature
from helper.utility import plot_image


class GradientFeature(Feature):

    def __init__(self, bins=8):
        self.bins = bins

    def name(self):
        return 'gradient'

    def keys(self):
        return map(str, range(self.bins))

    def extract(self, sample):
        flat = skimage.feature.hog(sample.gray, orientations=self.bins)
        cells = flat.reshape(len(flat) / self.bins, self.bins)
        histogram = [0] * self.bins
        for cell in cells:
            assert len(cell) == self.bins
            index = np.argmax(cell)
            histogram[index] += 1
        # Normalize histogram
        histogram = [x / len(cells) for x in histogram]
        return histogram

    def show(self, sample):
        _, visualization = skimage.feature.hog(sample.gray,
            orientations=self.bins, visualise=True)
        plot_image(visualization)
