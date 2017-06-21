import numpy as np

from democritus.exceptions import InvalidValueInSpecification


class ElementsFactory(object):
    @staticmethod
    def create(spec):
        spec_type = spec.get('type') or 'numbered'
        if spec_type == 'numbered':
            size = spec.get_or_fail('size')
            return np.arange(1, size + 1)
        elif spec_type == 'interval':
            size = spec.get_or_fail('size')
            start = spec.get('start') or 0
            end = spec.get('end') or 1
            return np.linspace(start=start, stop=end, num=size)
        else:
            raise InvalidValueInSpecification(spec, 'type', spec_type)
