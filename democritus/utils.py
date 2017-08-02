from __future__ import division

import numpy as np


def make_stochastic(vector):
    if np.sum(vector) == 0:
        vector = np.ones(np.shape(vector))
    return vector / np.sum(vector)


def make_row_stochastic(matrix):
    new_matrix = np.array(matrix)
    for i in range(len(matrix)):
        new_matrix[i] = make_stochastic(matrix[i])
    return new_matrix
