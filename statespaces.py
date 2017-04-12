import numpy as np
from scipy import stats as stats


class StateSpaceFactory(object):
    @staticmethod
    def create(spec):
        if spec['type'] == 'set':
            return SimpleSet(spec)
        if spec['type'] == 'metric':
            return MetricSpace(spec)
        else:
            raise ValueError('Invalid state space specification: ' + str(spec))


class SimpleSet(object):
    def __init__(self, spec):
        self.states = StateSetFactory.create(spec['states'])
        self.priors = PriorsFactory.create(spec['priors'], self.states)

    def size(self):
        return len(self.states)


class MetricSpace(SimpleSet):
    def __init__(self, spec):
        SimpleSet.__init__(self, spec)
        self.distances = MetricFactory.create(spec['metric'], self.states)


class StateSetFactory(object):
    @staticmethod
    def create(spec):
        if spec['type'] == 'interval':
            return np.linspace(start=spec['start'], stop=spec['end'], num=spec['size'], endpoint=True)
        else:
            raise ValueError('Invalid state set specification: ' + str(spec))


class PriorsFactory(object):
    @staticmethod
    def create(spec, states):
        if spec['type'] == 'uniform':
            return stats.uniform.pdf(states, scale=len(states))
        elif spec['type'] == 'normal':
            return stats.norm.pdf(states, loc=spec['mean'], scale=spec['standard deviation'])
        else:
            raise ValueError('Invalid priors specification: ' + str(spec))


class MetricFactory(object):
    @staticmethod
    def create(spec, states):
        if spec['type'] == 'euclidean':
            return np.array([[abs(x - y) for y in states] for x in states])
        else:
            raise ValueError('Invalid metric specification: ' + str(spec))
