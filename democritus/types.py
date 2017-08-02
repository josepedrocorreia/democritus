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

    def __getitem__(self, index):
        return self.values[index]

    def __setitem__(self, index, value):
        self.values[index] = value

    def __len__(self):
        return len(self.values)

    def __eq__(self, other):
        return np.all(self.values == other.values)

    def make_row_stochastic(self):
        self.values = utils.make_row_stochastic(self.values)

    def plot(self, axis):
        axis.imshow(self.values, origin='upper', interpolation='none')


class SenderStrategy(BivariateFunction):
    def __init__(self, states, messages, values):
        # TODO: validate dimensions
        BivariateFunction.__init__(self, values)
        self.states = states
        self.messages = messages

    def plot(self, axis):
        # TODO: Use names of states and messages
        for m in range(self.messages.size()):
            axis.plot(self.states.elements, self.values[:, m], label='$m_' + str(m + 1) + '$', marker='.')
        axis.set_ylim(-0.1, 1.1)
        axis.legend(loc='lower left')


class ReceiverStrategy(BivariateFunction):
    def __init__(self, messages, actions, values):
        # TODO: validate dimensions
        BivariateFunction.__init__(self, values)
        self.messages = messages
        self.actions = actions

    def plot(self, axis):
        # TODO: Use names of messages and actions
        for m in range(self.messages.size()):
            axis.plot(self.actions.elements, self.values[m, :], label='$m_' + str(m + 1) + '$', marker='.')
        axis.set_ylim(ymin=0)
        axis.legend(loc='lower left')
