import numpy as np

from democritus.elements import ElementsFactory
from democritus.exceptions import *


class MessagesFactory(object):
    @staticmethod
    def create(spec):
        spec_type = spec.get('type', 'set')
        if spec_type == 'set':
            if 'elements' not in spec:
                raise MissingFieldInSpecification(spec, 'elements')
            elements = ElementsFactory.create(spec['elements'])
            return MessageSet(elements)
        else:
            raise InvalidValueInSpecification(spec, 'type', spec_type)


class MessageSet(object):
    def __init__(self, elements):
        self.elements = np.array(elements)

    def size(self):
        return len(self.elements)
