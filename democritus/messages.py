class MessagesFactory(object):
    @staticmethod
    def create(spec):
        if spec['type'] == 'set':
            return MessageSet(MessageElementsFactory.create(spec['elements']))
        else:
            raise ValueError('Invalid messages specification: ' + str(spec))


class MessageElementsFactory(object):
    @staticmethod
    def create(spec):
        if spec['type'] == 'numbered':
            return range(1, spec['size'] + 1)
        else:
            raise ValueError('Invalid message elements specification: ' + str(spec))


class MessageSet(object):
    def __init__(self, elements):
        self.elements = elements

    def size(self):
        return len(self.elements)
