import matplotlib.pyplot as plt
import numpy as np


class ElementSet(object):
    def __init__(self, elements):
        self.elements = np.array(elements)

    def size(self):
        return len(self.elements)

    def index(self, element):
        return list(self.elements).index(element)


class StateSet(ElementSet):
    def __init__(self, elements, priors):
        ElementSet.__init__(self, elements)
        self.priors = np.array(priors)

    def get_prior(self, x):
        x_index = self.index(x)
        return self.priors[x_index]

    def plot(self):
        plt.plot(self.elements, self.priors, marker='.')
        plt.ylim(ymin=0)


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
