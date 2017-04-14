import numpy as np
from scipy import stats as stats


class StateSpaceFactory(object):
    @staticmethod
    def create(spec):
        if spec['type'] == 'set':
            return SetSpace(spec)
        if spec['type'] == 'metric':
            return MetricSpace(spec)
        else:
            raise ValueError('Invalid state space specification: ' + str(spec))


class SetSpace(object):
    def __init__(self, spec):
        self.states = StateSetFactory.create(spec['states'])
        priors_spec = {'type': 'uniform'} if 'priors' not in spec else spec['priors']
        self.priors = PriorsFactory.create(priors_spec, self.states)

    def size(self):
        return len(self.states)


class MetricSpace(SetSpace):
    def __init__(self, spec):
        SetSpace.__init__(self, spec)
        metric_spec = {'type': 'euclidean'} if 'metric' not in spec else spec['metric']
        self.distances = MetricFactory.create(metric_spec, self.states)


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
