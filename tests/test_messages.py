from democritus.messages import *

MESSAGE_ELEMENTS_SPEC_ONE_ELEMENT = {'type': 'numbered', 'size': 1}
MESSAGE_ELEMENTS_SPEC_FIVE_ELEMENTS = {'type': 'numbered', 'size': 5}
MESSAGES_SPEC_FIVE_ELEMENTS = {'type': 'set', 'elements': MESSAGE_ELEMENTS_SPEC_FIVE_ELEMENTS}


def test_message_set_creation_five_elements():
    message_set = MessageSet([1, 2, 3, 4, 5])
    # assert message_set has elements field
    assert type(message_set.elements) is list
    assert message_set.elements == [1, 2, 3, 4, 5]


def test_message_set_size():
    message_set = MessageSet([1, 2, 3, 4, 5])
    assert message_set.size() == 5


def test_message_elements_creation_one_element():
    message_elements = MessageElementsFactory.create(MESSAGE_ELEMENTS_SPEC_ONE_ELEMENT)
    assert type(message_elements) is list
    assert len(message_elements) == 1
    assert message_elements == [1]


def test_message_elements_creation_five_elements():
    message_elements = MessageElementsFactory.create(MESSAGE_ELEMENTS_SPEC_FIVE_ELEMENTS)
    assert type(message_elements) is list
    assert len(message_elements) == 5
    assert message_elements == [1, 2, 3, 4, 5]


def test_messages_creation_five_elements():
    messages = MessagesFactory.create(MESSAGES_SPEC_FIVE_ELEMENTS)
    assert type(messages) is MessageSet
    assert messages.size() == 5
    assert messages.elements == [1, 2, 3, 4, 5]
