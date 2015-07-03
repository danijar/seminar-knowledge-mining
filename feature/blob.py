import skimage.feature
from matplotlib import pyplot
from .feature import Feature


class BlobFeature(Feature):

    def __init__(self, min_size=3, max_size=30):
        self.min_size = min_size
        self.max_size = max_size

    def name(self):
        return 'blob'

    def keys(self):
        yield 'amount'
        yield 'size_mean'
        yield 'size_variance'

    def extract(self, sample):
        blobs = skimage.feature.blob_doh(sample.gray,
            min_sigma=self.min_size, max_sigma=self.max_size)
        if not len(blobs):
            return [0, 0, 0]
        sizes = blobs[:, 2]
        yield len(blobs)
        yield sizes.mean()
        yield sizes.var()

    def show(self, sample):
        fig, ax = pyplot.subplots(1, 1)
        ax.set_title('Blobs by Determinant of Hessian')
        ax.imshow(sample.image, interpolation='nearest')
        blobs = skimage.feature.blob_doh(sample.gray,
            min_sigma=self.min_size, max_sigma=self.max_size)
        for (y, x, r) in blobs:
            circle = pyplot.Circle((x, y), r, linewidth=2, fill=False)
            ax.add_patch(circle)
        pyplot.show()
