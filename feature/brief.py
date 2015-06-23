from .feature import Feature
import numpy as np
from skimage.feature import corner_peaks, corner_harris
from skimage.feature import BRIEF


class BriefFeature(Feature):
    length = 32

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.size = self.image.shape[:2]

    @classmethod
    def names(cls):
        return cls.multiple_names('brief', cls.length)

    def extract(self):
        points = self.get_points()
        radius = np.min(self.size) // 4
        extractor = BRIEF(type(self).length)
        extractor.extract(self.gray, points)
        points = points[extractor.mask]
        if len(extractor.descriptors):
            descriptor = extractor.descriptors[0].tolist()
            return descriptor
        else:
            print('Could not extract BRIEF descriptor')
            return [0] * type(self).length

    def get_points(self):
        points = corner_peaks(corner_harris(self.gray), min_distance=5)
        center = [int(x / 2) for x in self.size]
        points = np.append(points, [center], 0)
        return points
