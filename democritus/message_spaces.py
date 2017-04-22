class MessageSpaceFactory(object):
    @staticmethod
    def create(spec):
        if spec['type'] == 'set':
            return SetSpace(MessageSetFactory.create(spec['messages']))
        else:
            raise ValueError('Invalid message space specification: ' + str(spec))


class MessageSetFactory(object):
    @staticmethod
    def create(spec):
        if spec['type'] == 'numbered':
            return range(1, spec['size'] + 1)
        else:
            raise ValueError('Invalid message set specification: ' + str(spec))


class SetSpace(object):
    def __init__(self, elements):
        self.messages = elements

    def size(self):
        return len(self.messages)