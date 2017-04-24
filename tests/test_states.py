from __future__ import division

import numpy as np

from democritus.states import StateSet, MetricSpace, MetricFactory, PriorsFactory

state_set_three_uniform = StateSet([1, 2, 3], [1 / 3, 1 / 3, 1 / 3])
metric_space_three_uniform = MetricSpace([1, 2, 3], [1 / 3, 1 / 3, 1 / 3], [[1, 1, 1], [1, 1, 1], [1, 1, 1]])


# def test_state_set_creation():
#     assert hasattr(state_set_three_uniform, 'elements')
#     assert type(state_set_three_uniform.elements) is list
#     assert state_set_three_uniform.elements == [1, 2, 3]
#     assert hasattr(state_set_three_uniform, 'priors')
#     assert type(state_set_three_uniform.priors) is list
#     assert state_set_three_uniform.priors == [1 / 3, 1 / 3, 1 / 3]


def test_state_set_size():
    state_set = StateSet([1, 2, 3], [])
    assert state_set.size() == 3


# def test_metric_space_creation():
#     assert hasattr(metric_space_three_uniform, 'elements')
#     assert type(metric_space_three_uniform.elements) is list
#     assert metric_space_three_uniform.elements == [1, 2, 3]
#     assert hasattr(metric_space_three_uniform, 'priors')
#     assert type(metric_space_three_uniform.priors) is list
#     assert metric_space_three_uniform.priors == [1 / 3, 1 / 3, 1 / 3]
#     assert hasattr(metric_space_three_uniform, 'distances')
#     assert type(metric_space_three_uniform.distances) is list
#     assert list(metric_space_three_uniform.distances) == [1 / 3, 1 / 3, 1 / 3]


def test_metric_space_size():
    assert state_set_three_uniform.size() == 3


def test_metric_creation_euclidean():
    metric_spec = {'type': 'euclidean'}

    metric_1 = MetricFactory.create(metric_spec, [1])
    assert type(metric_1) is np.ndarray
    assert list(metric_1[0]) == [0]

    metric_3 = MetricFactory.create(metric_spec, [1, 2, 3])
    assert type(metric_3) is np.ndarray
    assert list(metric_3[0]) == [0, 1, 2]
    assert list(metric_3[1]) == [1, 0, 1]
    assert list(metric_3[2]) == [2, 1, 0]

    other_metric_3 = MetricFactory.create(metric_spec, [1, 2, 5])
    assert type(other_metric_3) is np.ndarray  # of arrays
    assert list(other_metric_3[0]) == [0, 1, 4]
    assert list(other_metric_3[1]) == [1, 0, 3]
    assert list(other_metric_3[2]) == [4, 3, 0]


def test_priors_creation_uniform():
    priors_spec = {'type': 'uniform'}

    priors_1 = PriorsFactory.create(priors_spec, [1])
    assert type(priors_1) is np.ndarray
    assert priors_1[0] == 1

    priors_3 = PriorsFactory.create(priors_spec, [1, 2, 3])
    assert type(priors_3) is np.ndarray
    assert list(priors_3) == [1 / 3, 1 / 3, 1 / 3]
