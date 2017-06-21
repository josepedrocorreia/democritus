import pytest

from democritus.exceptions import MissingFieldInSpecification
from democritus.messages import *
from democritus.specification import Specification


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
    messages_spec = Specification.from_dict({'type': 'set', 'elements': {'type': 'numbered', 'size': 5}})
    messages = MessagesFactory.create(messages_spec)
    assert type(messages) is MessageSet
    assert messages.size() == 5
    assert messages.elements.tolist() == [1, 2, 3, 4, 5]


def test_messages_factory_unknown_type_raises_exception():
    messages_spec = Specification.from_dict({'type': '????????', 'elements': {'type': 'numbered', 'size': 5}})
    with pytest.raises(InvalidValueInSpecification):
        MessagesFactory.create(messages_spec)


def test_messages_factory_missing_type_defaults_to_set():
    messages_spec = Specification.from_dict({'elements': {'type': 'numbered', 'size': 5}})
    messages = MessagesFactory.create(messages_spec)
    assert type(messages) is MessageSet
    assert messages.size() == 5
    assert messages.elements.tolist() == [1, 2, 3, 4, 5]


def test_messages_factory_missing_elements_raises_exception():
    messages_spec = Specification.from_dict({'type': 'set'})
    with pytest.raises(MissingFieldInSpecification):
        MessagesFactory.create(messages_spec)
