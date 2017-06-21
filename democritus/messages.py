import numpy as np

from democritus.elements import ElementsFactory
from democritus.exceptions import InvalidValueInSpecification


class MessagesFactory(object):
    @staticmethod
    def create(spec):
        spec_type = spec.get('type') or 'set'
        if spec_type == 'set':
            elements_spec = spec.get_or_fail('elements')
            elements = ElementsFactory.create(elements_spec)
            return MessageSet(elements)
        else:
            raise InvalidValueInSpecification(spec, 'type', spec_type)


class MessageSet(object):
    def __init__(self, elements):
        self.elements = np.array(elements)

    def size(self):
        return len(self.elements)
