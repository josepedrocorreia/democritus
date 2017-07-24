from __future__ import division

import numpy as np


class SimilarityFunctionFactory(object):
    @staticmethod
    def create_identity(size):
        return np.identity(size)

    @staticmethod
    def create_nosofsky(distances, decay):
        return np.exp(-(distances ** 2) / (decay ** 2))
