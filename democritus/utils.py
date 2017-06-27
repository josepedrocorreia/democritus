from __future__ import division

import numpy as np


def make_stochastic(vector):
    if np.sum(vector) == 0:
        vector = np.ones(np.shape(vector))
    return vector / np.sum(vector)


def make_row_stochastic(matrix):
    return np.array([make_stochastic(row) for row in matrix])
