import skimage.io
import skimage.transform
import skimage.exposure
import numpy as np
import matplotlib.pyplot


def load(filename):
    image = skimage.io.imread(filename)
    nearest = 0
    image = skimage.transform.resize(image, (128, 128), order=nearest)
    ignore_extrema = (np.percentile(image, 2), np.percentile(image, 98))
    image = skimage.exposure.rescale_intensity(image, in_range=ignore_extrema)
    return image

def show(image):
    matplotlib.pyplot.figure()
    skimage.io.imshow(image)
    skimage.io.show()
