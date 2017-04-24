from __future__ import division

from democritus.states import *


# StateSet

def test_state_set_attributes():
    elements = [1, 2, 3, 4]
    priors = [1 / 4, 1 / 4, 1 / 4, 1 / 4]
    state_set = StateSet(elements, priors)
    assert hasattr(state_set, 'elements')
    assert state_set.elements.tolist() == elements
    assert hasattr(state_set, 'priors')
    assert state_set.priors.tolist() == priors


def test_state_set_size():
    elements = [1, 2, 3, 4]
    priors = [1 / 4, 1 / 4, 1 / 4, 1 / 4]
    state_set = StateSet(elements, priors)
    assert state_set.size() == 4


# MetricSpace

def test_metric_space_attributes():
    elements = [1, 2, 3, 4]
    priors = [1 / 4, 1 / 4, 1 / 4, 1 / 4]
    distances = [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]]
    metric_space = MetricSpace(elements, priors, distances)
    assert hasattr(metric_space, 'elements')
    assert metric_space.elements.tolist() == elements
    assert hasattr(metric_space, 'priors')
    assert metric_space.priors.tolist() == priors
    assert hasattr(metric_space, 'distances')
    assert metric_space.distances.tolist() == distances


def test_metric_space_size():
    elements = ['a', 'b', 'c']
    priors = [1 / 3, 1 / 3, 1 / 3]
    distances = [[0, 1, 2], [1, 0, 1], [2, 1, 0]]
    metric_space = MetricSpace(elements, priors, distances)
    assert metric_space.size() == 3


def test_metric_space_distance():
    elements = ['a', 'b', 'c']
    priors = [1 / 3, 1 / 3, 1 / 3]
    distances = [[0, 1, 2], [1, 0, 1], [2, 1, 0]]
    metric_space = MetricSpace(elements, priors, distances)
    assert metric_space.distance('a', 'a') == 0
    assert metric_space.distance('a', 'b') == 1
    assert metric_space.distance('c', 'b') == 1
    assert metric_space.distance('a', 'c') == 2


# MetricFactory

def test_metric_factory_euclidean():
    metric_spec = {'type': 'euclidean'}

    metric_1 = MetricFactory.create(metric_spec, [1])
    assert metric_1[0].tolist() == [0]

    metric_3 = MetricFactory.create(metric_spec, [1, 2, 3])
    assert metric_3[0].tolist() == [0, 1, 2]
    assert metric_3[1].tolist() == [1, 0, 1]
    assert metric_3[2].tolist() == [2, 1, 0]

    other_metric_3 = MetricFactory.create(metric_spec, [1, 2, 5])
    assert other_metric_3[0].tolist() == [0, 1, 4]
    assert other_metric_3[1].tolist() == [1, 0, 3]
    assert other_metric_3[2].tolist() == [4, 3, 0]


# PriorsFactory

def test_priors_creation_uniform():
    priors_spec = {'type': 'uniform'}

    priors_1 = PriorsFactory.create(priors_spec, [1])
    assert priors_1.tolist() == [1]

    priors_3 = PriorsFactory.create(priors_spec, [1, 2, 3])
    assert priors_3.tolist() == [1 / 3, 1 / 3, 1 / 3]
