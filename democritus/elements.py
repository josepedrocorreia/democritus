import numpy as np

from democritus.exceptions import *


class ElementsFactory(object):
    @staticmethod
    def create(spec):
        spec_type = spec.get('type', 'numbered')
        if spec_type == 'numbered':
            if 'size' not in spec:
                raise MissingFieldInSpecification(spec, 'size')
            size = spec['size']
            return np.arange(1, size + 1)
        elif spec_type == 'interval':
            if 'size' not in spec:
                raise MissingFieldInSpecification(spec, 'size')
            size = spec['size']
            start = spec.get('start', 0)
            end = spec.get('end', 1)
            return np.linspace(start=start, stop=end, num=size)
        else:
            raise InvalidValueInSpecification(spec, 'type', spec_type)
