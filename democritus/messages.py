import numpy as np


class MessagesFactory(object):
    @staticmethod
    def create(spec):
        spec_type = spec.get('type', 'numbered')
        if spec_type == 'set':
            if 'elements' not in spec:
                raise ValueError('Missing elements in messages specification: ' + str(spec))
            elements = MessageElementsFactory.create(spec['elements'])
            return MessageSet(elements)
        else:
            raise ValueError('Unknown type in messages specification: ' + str(spec))


class MessageElementsFactory(object):
    @staticmethod
    def create(spec):
        spec_type = spec.get('type', 'numbered')
        if spec_type == 'numbered':
            if 'size' not in spec:
                raise ValueError('Missing size in message elements specification: ' + str(spec))
            return range(1, spec['size'] + 1)
        else:
            raise ValueError('Unknown type in message elements specification: ' + str(spec))


class MessageSet(object):
    def __init__(self, elements):
        self.elements = np.array(elements)

    def size(self):
        return len(self.elements)
