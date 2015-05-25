import numpy as np


class Feature:

    def __init__(self, image):
        # Provide useful formats of the image data to sub classes
        self.image = image
        self.channels = np.rollaxis(self.image, 2)
        self.pixels = self.image.reshape(-1, self.image.shape[-1])
        # Pixel data is shared between extractors
        self.image.setflags(write=False)
        self.channels.setflags(write=False)
        self.pixels.setflags(write=False)

    def names(self):
        raise NotImplementedError

    def extract(self):
        raise NotImplementedError
