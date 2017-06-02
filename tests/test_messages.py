import pytest

from democritus.messages import *


# MessageSet

def test_message_set_attributes():
    elements = [1, 2, 3, 4, 5]
    message_set = MessageSet(elements)
    assert hasattr(message_set, 'elements')
    assert message_set.elements.tolist() == elements


def test_message_set_size():
    message_set = MessageSet([1, 2, 3, 4, 5])
    assert message_set.size() == 5


# MessagesFactory

def test_messages_factory_five_elements():
    messages = MessagesFactory.create({'type': 'set', 'elements': {'type': 'numbered', 'size': 5}})
    assert type(messages) is MessageSet
    assert messages.size() == 5
    assert messages.elements.tolist() == [1, 2, 3, 4, 5]


def test_messages_factory_unknown_type_raises_exception():
    with pytest.raises(InvalidValueInSpecification):
        MessagesFactory.create({'type': '????????', 'elements': {'type': 'numbered', 'size': 5}})


def test_messages_factory_missing_type_defaults_to_set():
    messages = MessagesFactory.create({'elements': {'type': 'numbered', 'size': 5}})
    assert type(messages) is MessageSet
    assert messages.size() == 5
    assert messages.elements.tolist() == [1, 2, 3, 4, 5]


def test_messages_factory_missing_elements_raises_exception():
    with pytest.raises(MissingFieldInSpecification):
        MessagesFactory.create({'type': 'set'})
