import numpy as np

from democritus.collections import MessageSet, StateSet, MetricSpace


# MessageSet
def test_message_set_attributes():
    elements = [1, 2, 3, 4, 5]
    message_set = MessageSet(elements)
    assert hasattr(message_set, 'elements')
    assert type(message_set.elements) is np.ndarray
    assert message_set.elements.tolist() == elements


def test_message_set_size():
    message_set = MessageSet([1, 2, 3, 4, 5])
    assert message_set.size() == 5


# StateSet
def test_state_set_attributes():
    elements = [1, 2, 3, 4]
    priors = [1 / 4, 1 / 4, 1 / 4, 1 / 4]
    state_set = StateSet(elements, priors)
    assert hasattr(state_set, 'elements')
    assert type(state_set.elements) is np.ndarray
    assert state_set.elements.tolist() == elements
    assert hasattr(state_set, 'priors')
    assert type(state_set.priors) is np.ndarray
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
