import numpy as np
import skimage.feature
from matplotlib import pyplot
from .feature import Feature


class BlobFeature(Feature):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.min_size = 3
        self.max_size = 30

    @classmethod
    def names(cls):
        return [
            'blob_amount',
            'blob_size_mean',
            'blob_size_variance'
        ]

    def extract(self):
        blobs = skimage.feature.blob_doh(self.gray,
            min_sigma=self.min_size, max_sigma=self.max_size)
        if not len(blobs):
            return [0, 0, 0]
        sizes = blobs[:,2]
        yield len(blobs)
        yield sizes.mean()
        yield sizes.var()

    def show(self):
        fig, ax = pyplot.subplots(1, 1)
        ax.set_title('Blobs by Determinant of Hessian')
        ax.imshow(self.image, interpolation='nearest')
        blobs = skimage.feature.blob_doh(self.gray,
            min_sigma=self.min_size, max_sigma=self.max_size)
        for (y, x, r) in blobs:
            circle = pyplot.Circle((x, y), r, linewidth=2, fill=False)
            ax.add_patch(circle)
        pyplot.show()
