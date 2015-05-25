import skimage.feature
import numpy as np
from .feature import Feature
from helper.image import load, show


class GradientFeature(Feature):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bins = 8

    def names(self):
        yield from self.multiple_names('gradient', self.bins)

    def extract(self):
        flat = skimage.feature.hog(self.image_gray, orientations=self.bins)
        cells = flat.reshape(len(flat) / self.bins, self.bins)
        histogram = [0] * self.bins
        for cell in cells:
            assert len(cell) == self.bins
            index = np.argmax(cell)
            histogram[index] += 1
        # Normalize histogram
        histogram = [x / len(cells) for x in histogram]
        return histogram

    def show(self):
        _, visualization = skimage.feature.hog(self.image_gray,
            orientations=self.bins, visualise=True)
        show(visualization)
