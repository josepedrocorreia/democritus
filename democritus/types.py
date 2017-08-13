import numpy as np

from democritus import utils


class ElementSet(object):
    def __init__(self, elements):
        self.elements = elements

    def size(self):
        return len(self.elements)

    def index(self, element):
        return self.elements.index(element)


class StateSet(ElementSet):
    def __init__(self, elements, priors):
        ElementSet.__init__(self, elements)
        self.priors = np.array(priors)
        if len(self.elements) != len(self.priors):
            raise ValueError(
                'Number of elements and priors should be the same. '
                'Supplied %s elements and %s priors.' % (len(self.elements), len(self.priors)))

    def get_prior(self, x):
        x_index = self.index(x)
        return self.priors[x_index]

    def plot(self, axis):
        axis.plot(self.elements, self.priors, marker='.')
        axis.set_ylim(bottom=0)


class StateMetricSpace(StateSet):
    def __init__(self, elements, priors, metric):
        StateSet.__init__(self, elements, priors)
        self.distances = np.array(metric)
        if self.distances.shape[0] != len(self.elements) or self.distances.shape[1] != len(self.elements):
            raise ValueError(
                'Incorrect dimensions of metric. '
                'Metric should be square matrix of order %s.' % len(self.elements))

    def distance(self, x, y):
        x_index = self.index(x)
        y_index = self.index(y)
        return self.distances[x_index, y_index]


class MessageSet(ElementSet):
    @staticmethod
    def from_element_set(element_set):
        return MessageSet(element_set.elements)


class ActionSet(ElementSet):
    @staticmethod
    def from_element_set(element_set):
        return ActionSet(element_set.elements)


class BivariateFunction(object):
    def __init__(self, values):
        self.values = np.array(values)
        if len(self.values.shape) != 2:
            raise ValueError('Values for bivariate function should be two-dimensional.')

    def __getitem__(self, index):
        return self.values[index]

    def __setitem__(self, index, value):
        self.values[index] = value

    def __len__(self):
        return len(self.values)

    def make_row_stochastic(self):
        self.values = utils.make_row_stochastic(self.values)

    def plot(self, axis):
        axis.imshow(self.values, origin='upper', interpolation='none')


class BehavioralStrategy(BivariateFunction):
    def __init__(self, choice_points, choices, probabilities):
        BivariateFunction.__init__(self, probabilities)
        self.probabilities = self.values
        self.make_row_stochastic()
        self.choice_points = choice_points
        self.choices = choices
        if self.values.shape[0] != self.choice_points.size() or self.values.shape[1] != self.choices.size():
            raise ValueError('Incorrect dimensions for probabilities, should accord with choice points and choices. '
                             'There are %s choice points, %s choices, '
                             'but probabilities have dimensions %s.' %
                             (self.choice_points.size(), self.choices.size(), self.values.shape))


class SenderStrategy(BehavioralStrategy):
    def __init__(self, states, messages, probabilities):
        BehavioralStrategy.__init__(self, states, messages, probabilities)
        self.states = self.choice_points
        self.messages = self.choices

    def plot(self, axis):
        for m in range(self.messages.size()):
            axis.plot(self.states.elements, self.values[:, m],
                      label='$' + str(self.messages.elements[m]) + '$',
                      marker='.')
        axis.set_ylim(-0.1, 1.1)
        axis.legend(loc='lower left')


class ReceiverStrategy(BehavioralStrategy):
    def __init__(self, messages, actions, probabilities):
        BehavioralStrategy.__init__(self, messages, actions, probabilities)
        self.messages = self.choice_points
        self.actions = self.choices

    def plot(self, axis):
        for m in range(self.messages.size()):
            axis.plot(self.actions.elements, self.values[m, :],
                      label='$' + str(self.messages.elements[m]) + '$',
                      marker='.')
        axis.set_ylim(ymin=0)
        axis.legend(loc='lower left')
