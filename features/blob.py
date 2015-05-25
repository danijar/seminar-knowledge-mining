import numpy as np
import skimage.feature
from matplotlib import pyplot
from .feature import Feature


class BlobFeature(Feature):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_amount = 100
        self.min_size = 3
        self.max_size = 30

    def names(self):
        return [
            'blob_amount',
            'blob_size_mean',
            'blob_size_variance',
            'blob_size_median'
        ]

    def extract(self):
        blobs = skimage.feature.blob_doh(self.image_gray,
            min_sigma=self.min_size, max_sigma=self.max_size)
        if not len(blobs):
            return [0, 0, 0, 0]
        amount = min(len(blobs), self.max_amount) / self.max_amount
        sizes = blobs[:,2] / self.max_size
        return [
            amount,
            sizes.mean(),
            sizes.var(),
            np.median(sizes)
        ]

    def show(self):
        fig, ax = pyplot.subplots(1, 1)
        ax.set_title('Blobs by Determinant of Hessian')
        ax.imshow(self.image, interpolation='nearest')
        blobs = skimage.feature.blob_doh(self.image_gray,
            min_sigma=self.min_size, max_sigma=self.max_size)
        for (y, x, r) in blobs:
            circle = pyplot.Circle((x, y), r, linewidth=2, fill=False)
            ax.add_patch(circle)
        pyplot.show()
