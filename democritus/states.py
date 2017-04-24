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
        spec_type = 'uniform' if 'type' not in spec \
            else spec['type']

        if spec_type == 'uniform':
            return stats.uniform.pdf(elements, scale=len(elements))
        elif spec_type == 'normal':
            mean = np.mean(elements) if 'mean' not in spec \
                else spec['mean']
            standard_deviation = np.std(elements, ddof=1) if 'standard deviation' not in spec \
                else spec['standard deviation']
            return stats.norm.pdf(elements, loc=mean, scale=standard_deviation)
        else:
            raise ValueError('Unknown type in priors specification: ' + str(spec))


class MetricFactory(object):
    @staticmethod
    def create(spec, elements):
        spec_type = 'euclidean' if 'type' not in spec \
            else spec['type']

        if spec_type == 'euclidean':
            return np.array([[abs(x - y) for y in elements] for x in elements])
        else:
            raise ValueError('Unknown type in metric specification: ' + str(spec))


class StateSet(object):
    def __init__(self, elements, priors):
        self.elements = np.array(elements)
        self.priors = np.array(priors)

    def size(self):
        return len(self.elements)


class MetricSpace(StateSet):
    def __init__(self, elements, priors, metric):
        StateSet.__init__(self, elements, priors)
        self.distances = np.array(metric)

    def distance(self, x, y):
        x_index = self.elements.tolist().index(x)
        y_index = self.elements.tolist().index(y)
        return self.distances[x_index, y_index]
