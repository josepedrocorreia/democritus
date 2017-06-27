from __future__ import division

import numpy as np

from democritus.exceptions import InvalidValueInSpecification, IncompatibilityInSpecification


class UtilityFactory(object):
    @staticmethod
    def create(spec, states):
        spec_type = spec.get('type') or 'identity'
        if spec_type == 'identity':
            return IdentityUtility(states)
        if spec_type == 'nosofsky':
            if not hasattr(states, 'distances'):
                raise IncompatibilityInSpecification(spec, 'states', 'utility')
            decay = spec.get('decay') or 1
            return NosofskyUtility(states, decay)
        else:
            raise InvalidValueInSpecification(spec, 'type', spec_type)


class Utility(object):
    def __init__(self, utilities):
        self.utilities = utilities


class IdentityUtility(Utility):
    def __init__(self, states):
        Utility.__init__(self, np.identity(states.size()))


class NosofskyUtility(Utility):
    def __init__(self, states, decay):
        Utility.__init__(self, np.exp(-(states.distances ** 2) / (decay ** 2)))
