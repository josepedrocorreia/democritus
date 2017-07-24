import matplotlib.pyplot as plt
import numpy as np


class MessageSet(object):
    def __init__(self, elements):
        self.elements = np.array(elements)

    def size(self):
        return len(self.elements)


class StateSet(object):
    def __init__(self, elements, priors):
        self.elements = np.array(elements)
        self.priors = np.array(priors)

    def size(self):
        return len(self.elements)

    def plot(self):
        plt.plot(self.elements, self.priors, marker='.')
        plt.ylim(ymin=0)


class StateMetricSpace(StateSet):
    def __init__(self, elements, priors, metric):
        StateSet.__init__(self, elements, priors)
        self.distances = np.array(metric)

    def distance(self, x, y):
        x_index = self.elements.tolist().index(x)
        y_index = self.elements.tolist().index(y)
        return self.distances[x_index, y_index]
