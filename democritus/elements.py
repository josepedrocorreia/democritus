import numpy as np


class ElementsFactory(object):
    @staticmethod
    def create(spec):
        spec_type = spec.get('type', 'numbered')
        if spec_type == 'numbered':
            if 'size' not in spec:
                raise ValueError('Missing size in elements specification: ' + str(spec))
            size = spec['size']
            return range(1, size + 1)
        elif spec_type == 'interval':
            if 'size' not in spec:
                raise ValueError('Missing size in elements specification: ' + str(spec))
            size = spec['size']
            start = spec.get('start', 0)
            end = spec.get('end', 1)
            return np.linspace(start=start, stop=end, num=size)
        else:
            raise ValueError('Unknown type in elements specification: ' + str(spec))
