import numpy as np
from scipy import stats as stats

DEFAULT_PRIORS_SPEC = {'type': 'uniform'}
DEFAULT_METRIC_SPEC = {'type': 'euclidean'}


class StatesFactory(object):
    @staticmethod
    def create(spec):
        if spec['type'] == 'set':
            elements_spec = spec['elements']
            priors_spec = DEFAULT_PRIORS_SPEC if 'priors' not in spec else spec['priors']
            return StateSetFactory.create(elements_spec, priors_spec)
        if spec['type'] == 'metric space':
            elements_spec = spec['elements']
            priors_spec = DEFAULT_PRIORS_SPEC if 'priors' not in spec else spec['priors']
            metric_spec = DEFAULT_METRIC_SPEC if 'metric' not in spec else spec['metric']
            return MetricSpaceFactory.create(elements_spec, priors_spec, metric_spec)
        else:
            raise ValueError('Invalid states specification: ' + str(spec))


class StateSetFactory(object):
    @staticmethod
    def create(elements_spec, priors_spec):
        elements = StateElementsFactory.create(elements_spec)
        priors = PriorsFactory.create(priors_spec, elements)
        return StateSet(elements, priors)


class MetricSpaceFactory(object):
    @staticmethod
    def create(elements_spec, priors_spec, metric_spec):
        elements = StateElementsFactory.create(elements_spec)
        priors = PriorsFactory.create(priors_spec, elements)
        metric = MetricFactory.create(metric_spec, elements)
        return MetricSpace(elements, priors, metric)


class StateElementsFactory(object):
    @staticmethod
    def create(spec):
        if spec['type'] == 'interval':
            return np.linspace(start=spec['start'], stop=spec['end'], num=spec['size'], endpoint=True)
        else:
            raise ValueError('Invalid state elements specification: ' + str(spec))


class PriorsFactory(object):
    @staticmethod
    def create(spec, elements):
        if spec['type'] == 'uniform':
            return stats.uniform.pdf(elements, scale=len(elements))
        elif spec['type'] == 'normal':
            return stats.norm.pdf(elements, loc=spec['mean'], scale=spec['standard deviation'])
        else:
            raise ValueError('Invalid priors specification: ' + str(spec))


class MetricFactory(object):
    @staticmethod
    def create(spec, elements):
        if spec['type'] == 'euclidean':
            return np.array([[abs(x - y) for y in elements] for x in elements])
        else:
            raise ValueError('Invalid metric specification: ' + str(spec))


class StateSet(object):
    def __init__(self, elements, priors):
        self.elements = elements
        self.priors = priors

    def size(self):
        return len(self.elements)


class MetricSpace(StateSet):
    def __init__(self, elements, priors, metric):
        StateSet.__init__(self, elements, priors)
        self.distances = metric

        # def distance(self, x, y):
        #     x_index = self.elements.indexof(x)
        #     y_index = self.elements.indexof(y)
        #     return self.distances(x_index, y_index)
