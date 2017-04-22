from democritus.message_spaces import *

MESSAGE_SET_SPEC_ONE_ELEMENT = {'type': 'numbered', 'size': 1}
MESSAGE_SET_SPEC_FIVE_ELEMENTS = {'type': 'numbered', 'size': 5}
MESSAGE_SPACE_SPEC_FIVE_ELEMENTS = {'type': 'set', 'messages': MESSAGE_SET_SPEC_FIVE_ELEMENTS}


def test_set_space_creation_five_elements():
    set_space = SetSpace([1, 2, 3, 4, 5])
    # assert set_space has messages field
    assert type(set_space.messages) is list
    assert set_space.messages == [1, 2, 3, 4, 5]


def test_set_space_size():
    set_space = SetSpace([1, 2, 3, 4, 5])
    assert set_space.size() == 5


def test_message_set_creation_one_element():
    message_set = MessageSetFactory.create(MESSAGE_SET_SPEC_ONE_ELEMENT)
    assert type(message_set) is list
    assert len(message_set) == 1
    assert message_set == [1]


def test_message_set_creation_five_elements():
    message_set = MessageSetFactory.create(MESSAGE_SET_SPEC_FIVE_ELEMENTS)
    assert type(message_set) is list
    assert len(message_set) == 5
    assert message_set == [1, 2, 3, 4, 5]


def test_message_space_creation_five_elements():
    message_space = MessageSpaceFactory.create(MESSAGE_SPACE_SPEC_FIVE_ELEMENTS)
    assert type(message_space) is SetSpace
    assert message_space.size() == 5
    assert message_space.messages == [1, 2, 3, 4, 5]
