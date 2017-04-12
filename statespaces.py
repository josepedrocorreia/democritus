import numpy as np
from scipy import stats as stats


class StateSpaceFactory(object):
    @staticmethod
    def create(spec):
        if spec['priors'] == 'uniform':
            return UniformEuclideanSpace(number_of_states=spec['size'])
        if spec['priors'] == 'normal':
            return NormalEuclideanSpace(number_of_states=spec['size'])
        # if all else fails
        raise ValueError('Invalid state space specification: ' + str(spec))


class IntervalSet(object):
    def __init__(self, number_of_states, start=0, end=1):
        self.states = np.linspace(start, end, number_of_states, endpoint=True)


class EuclideanSpace(IntervalSet):
    def __init__(self, number_of_states, start=0, end=1):
        IntervalSet.__init__(self, number_of_states, start, end)
        self.distances = np.array([[abs(x - y)
                                    for y in self.states]
                                   for x in self.states])


class UniformEuclideanSpace(EuclideanSpace):
    def __init__(self, number_of_states, start=0, end=1):
        EuclideanSpace.__init__(self, number_of_states, start, end)
        self.priors = stats.uniform.pdf(self.states, scale=len(self.states))


class NormalEuclideanSpace(EuclideanSpace):
    def __init__(self, number_of_states, start=0, end=1, center=0.5, standard_deviation=0.1):
        EuclideanSpace.__init__(self, number_of_states, start, end)
        self.priors = stats.norm.pdf(self.states, loc=center, scale=standard_deviation)
