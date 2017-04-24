class MessagesFactory(object):
    @staticmethod
    def create(spec):
        if 'type' not in spec \
                or 'elements' not in spec:
            raise ValueError('Invalid messages specification: ' + str(spec))
        if spec['type'] == 'set':
            elements = MessageElementsFactory.create(spec['elements'])
            return MessageSet(elements)
        else:
            raise ValueError('Unknown type in messages specification: ' + str(spec))


class MessageElementsFactory(object):
    @staticmethod
    def create(spec):
        if 'type' not in spec \
                or 'size' not in spec:
            raise ValueError('Invalid message elements specification: ' + str(spec))
        if spec['type'] == 'numbered':
            return range(1, spec['size'] + 1)
        else:
            raise ValueError('Unknown type in message elements specification: ' + str(spec))


class MessageSet(object):
    def __init__(self, elements):
        self.elements = elements

    def size(self):
        return len(self.elements)
