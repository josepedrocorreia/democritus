from __future__ import division

import numpy as np
import pytest

from democritus.types import StateSet, StateMetricSpace, ActionSet, ElementSet, BivariateFunction, SenderStrategy, \
    ReceiverStrategy


class TestElementSet(object):
    def test_constructor(self):
        elements = [1, 2, 3, 4, 5]
        element_set = ElementSet(elements)
        assert hasattr(element_set, 'elements')
        assert type(element_set.elements) is list
        assert element_set.elements == elements

    def test_size(self):
        element_set = ElementSet([7, 2, 99, -4])
        assert element_set.size() == 4

    def test_index(self):
        element_set = ElementSet([7, 2, 99, -4])
        assert element_set.index(7) == 0
        assert element_set.index(2) == 1
        assert element_set.index(99) == 2
        assert element_set.index(-4) == 3


class TestStateSet(object):
    def test_constructor(self):
        elements = [1, 2, 3, 4]
        priors = [1 / 4, 1 / 4, 1 / 4, 1 / 4]
        state_set = StateSet(elements, priors)
        assert hasattr(state_set, 'elements')
        assert type(state_set.elements) is list
        assert state_set.elements == elements
        assert hasattr(state_set, 'priors')
        assert type(state_set.priors) is np.ndarray
        assert state_set.priors.tolist() == priors

    def test_constructor_incorrect_dimensions_raises_exception(self):
        elements = [1, 2, 3, 4]
        priors = [1]
        with pytest.raises(ValueError):
            StateSet(elements, priors)

    def test_get_prior(self):
        elements = [7, 2, 99, 4]
        priors = [1 / 7, 1 / 2, 1 / 99, 1 / 4]
        state_set = StateSet(elements, priors)
        assert state_set.get_prior(7) == 1 / 7
        assert state_set.get_prior(2) == 1 / 2
        assert state_set.get_prior(99) == 1 / 99
        assert state_set.get_prior(4) == 1 / 4


class TestStateMetricSpace(object):
    def test_constructor(self):
        elements = [1, 2, 3, 4]
        priors = [1 / 4, 1 / 4, 1 / 4, 1 / 4]
        distances = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
        metric_space = StateMetricSpace(elements, priors, distances)
        assert hasattr(metric_space, 'elements')
        assert metric_space.elements == elements
        assert hasattr(metric_space, 'priors')
        assert metric_space.priors.tolist() == priors
        assert hasattr(metric_space, 'distances')
        assert metric_space.distances.tolist() == distances

    def test_constructor_incorrect_metric_x_dimensions_raises_exception(self):
        elements = [1, 2, 3, 4]
        priors = [1 / 4, 1 / 4, 1 / 4, 1 / 4]
        distances = [[1, 2, 3, 4]]
        with pytest.raises(ValueError):
            StateMetricSpace(elements, priors, distances)

    def test_constructor_incorrect_metric_y_dimensions_raises_exception(self):
        elements = [1, 2, 3, 4]
        priors = [1 / 4, 1 / 4, 1 / 4, 1 / 4]
        distances = [[1, 2, 3, 4, 0], [5, 6, 7, 8, 0], [9, 10, 11, 12, 0], [13, 14, 15, 16, 0]]
        with pytest.raises(ValueError):
            StateMetricSpace(elements, priors, distances)

    def test_distance(self):
        elements = ['a', 'b', 'c']
        priors = [1 / 3, 1 / 3, 1 / 3]
        distances = [[0, 1, 2], [1, 0, 1], [2, 1, 0]]
        metric_space = StateMetricSpace(elements, priors, distances)
        assert metric_space.distance('a', 'a') == 0
        assert metric_space.distance('a', 'b') == 1
        assert metric_space.distance('c', 'b') == 1
        assert metric_space.distance('a', 'c') == 2


class TestMessageSet(object):
    def test_from_element_set(self):
        elements = [7, 2, 99, -4]
        action_set = ActionSet.from_element_set(ElementSet(elements))
        assert type(action_set) is ActionSet
        assert hasattr(action_set, 'elements')
        assert type(action_set.elements) is list
        assert action_set.elements == elements


class TestActionSet(object):
    def test_from_element_set(self):
        elements = [7, 2, 99, -4]
        action_set = ActionSet.from_element_set(ElementSet(elements))
        assert type(action_set) is ActionSet
        assert hasattr(action_set, 'elements')
        assert type(action_set.elements) is list
        assert action_set.elements == elements


class TestBivariateFunction(object):
    def test_constructor(self):
        values = [[0.0, 1.0], [0.3, 0.7]]
        func = BivariateFunction(values)
        assert hasattr(func, 'values')
        assert type(func.values) is np.ndarray
        assert func.values[0].tolist() == values[0]
        assert func.values[1].tolist() == values[1]

    def test_constructor_incorrect_dimensions_raises_exception(self):
        values = [0.0, 1.0, 0.3, 0.7]
        with pytest.raises(ValueError):
            BivariateFunction(values)

    def test_make_row_stochastic(self):
        values = [[0.0, 2.0], [0.3, 0.9], [0.05, 0.2]]
        func = BivariateFunction(values)
        func.make_row_stochastic()
        assert func.values[0].tolist() == [0.0, 1.0]
        assert func.values[1].tolist() == [0.25, 0.75]
        assert func.values[2].tolist() == [0.2, 0.8]


class TestSenderStrategy(object):
    def test_constructor(self, states, messages):
        probabilities = [[0.0, 2.0], [0.3, 0.9], [0.05, 0.2]]
        sender_strategy = SenderStrategy(states, messages, probabilities)
        assert hasattr(sender_strategy, 'states')
        assert hasattr(sender_strategy, 'messages')
        assert hasattr(sender_strategy, 'probabilities')
        assert sender_strategy.values[0].tolist() == [0.0, 1.0]
        assert sender_strategy.values[1].tolist() == [0.25, 0.75]
        assert sender_strategy.values[2].tolist() == [0.2, 0.8]

    def test_constructor_incorrect_x_dimensions_raises_exception(self, states, messages):
        probabilities = [[0.0, 2.0]]
        with pytest.raises(ValueError):
            SenderStrategy(states, messages, probabilities)

    def test_constructor_incorrect_y_dimensions_raises_exception(self, states, messages):
        probabilities = [[0.0], [0.3], [0.05]]
        with pytest.raises(ValueError):
            SenderStrategy(states, messages, probabilities)


class TestReceiverStrategy(object):
    def test_constructor(self, messages, actions):
        probabilities = [[0.1, 0.2, 0.3, 1.4], [0.0, 0.0, 0.0, 0.5]]
        receiver_strategy = ReceiverStrategy(messages, actions, probabilities)
        assert hasattr(receiver_strategy, 'messages')
        assert hasattr(receiver_strategy, 'actions')
        assert hasattr(receiver_strategy, 'probabilities')
        assert receiver_strategy.values[0].tolist() == [0.05, 0.1, 0.15, 0.7]
        assert receiver_strategy.values[1].tolist() == [0.0, 0.0, 0.0, 1.0]

    def test_constructor_incorrect_x_dimensions_raises_exception(self, messages, actions):
        probabilities = [[0.1, 0.2, 0.3, 1.4]]
        with pytest.raises(ValueError):
            ReceiverStrategy(messages, actions, probabilities)

    def test_constructor_incorrect_y_dimensions_raises_exception(self, messages, actions):
        probabilities = [[0.1, 0.2, 0.3], [0.0, 0.0, 0.0]]
        with pytest.raises(ValueError):
            ReceiverStrategy(messages, actions, probabilities)
