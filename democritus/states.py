import numpy as np
from scipy import stats as stats

from democritus.elements import ElementsFactory


class StatesFactory(object):
    @staticmethod
    def create(spec):
        spec_type = spec.get('type', 'set')
        if spec_type == 'set':
            if 'elements' not in spec:
                raise ValueError('Missing elements in states specification: ' + str(spec))
            elements_spec = spec['elements']
            priors_spec = spec.get('priors', {})
            elements = ElementsFactory.create(elements_spec)
            priors = PriorsFactory.create(priors_spec, elements)
            return StateSet(elements, priors)
        if spec_type == 'metric space':
            if 'elements' not in spec:
                raise ValueError('Missing elements in states specification: ' + str(spec))
            elements_spec = spec['elements']
            priors_spec = spec.get('priors', {})
            metric_spec = spec.get('metric', {})
            elements = ElementsFactory.create(elements_spec)
            priors = PriorsFactory.create(priors_spec, elements)
            metric = MetricFactory.create(metric_spec, elements)
            return MetricSpace(elements, priors, metric)
        else:
            raise ValueError('Invalid states specification: ' + str(spec))


class PriorsFactory(object):
    @staticmethod
    def create(spec, elements):
        spec_type = spec.get('type', 'uniform')
        if spec_type == 'uniform':
            return stats.uniform.pdf(elements, scale=len(elements))
        elif spec_type == 'normal':
            mean = spec.get('mean', np.mean(elements))
            standard_deviation = spec.get('standard deviation', np.std(elements, ddof=1))
            return stats.norm.pdf(elements, loc=mean, scale=standard_deviation)
        else:
            raise ValueError('Unknown type in priors specification: ' + str(spec))


class MetricFactory(object):
    @staticmethod
    def create(spec, elements):
        spec_type = spec.get('type', 'euclidean')
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
