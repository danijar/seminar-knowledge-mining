import numpy as np
from .feature import Feature


class ColorFeature(Feature):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def names():
        return [
            'color_distinct_amount',
            'color_mean_read',
            'color_mean_green',
            'color_mean_blue',
            'color_variance_read',
            'color_variance_green',
            'color_variance_blue'
        ];

    def extract(self):
        return [self.amount()] + self.mean() + self.variance()

    def amount(self):
        return len(np.unique(self.pixels))

    def mean(self):
        return [x.mean() for x in self.channels]

    def variance(self):
        return [x.var() for x in self.channels]
