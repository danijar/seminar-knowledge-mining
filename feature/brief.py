from .feature import Feature, FeatureExtractionError
import numpy as np
from skimage.feature import corner_peaks, corner_harris
from skimage.feature import BRIEF


class BriefFeature(Feature):

    def __init__(self, length=32):
        self.length = length

    def name(self):
        return 'brief'

    def keys(self):
        return map(str, range(self.length))

    def extract(self, sample):
        points = self._get_points(sample)
        radius = np.min(sample.size) // 4
        extractor = BRIEF(self.length, patch_size=radius)
        extractor.extract(sample.gray, points)
        points = points[extractor.mask]
        if not len(extractor.descriptors):
            raise FeatureExtractionError(self,
                'Could not extract BRIEF descriptor')
        descriptor = extractor.descriptors[0].tolist()
        return descriptor

    def _get_points(self, sample):
        points = corner_peaks(corner_harris(sample.gray), min_distance=5)
        center = [int(x / 2) for x in self.size]
        points = np.append(points, [center], 0)
        return points
