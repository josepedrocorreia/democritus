from __future__ import division

import numpy as np

from democritus.exceptions import InvalidValueInSpecification, IncompatibilityInSpecification


class SimilarityFunctionReader(object):
    @staticmethod
    def create(spec, states):
        spec_type = spec.get('type') or 'identity'
        if spec_type == 'identity':
            return SimilarityFunctionFactory.create_identity(states.size())
        if spec_type == 'nosofsky':
            decay = spec.get('decay') or 1
            if not hasattr(states, 'distances'):
                raise IncompatibilityInSpecification(spec, 'states', 'utility')
            return SimilarityFunctionFactory.create_nosofsky(states.distances, decay)
        else:
            raise InvalidValueInSpecification(spec, 'type', spec_type)


class SimilarityFunctionFactory(object):
    @staticmethod
    def create_identity(size):
        return np.identity(size)

    @staticmethod
    def create_nosofsky(distances, decay):
        return np.exp(-(distances ** 2) / (decay ** 2))
