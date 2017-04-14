from democritus.message_spaces import MessageSetFactory


def test_message_set_creation():
    test_spec = {'type': 'numbered', 'size': 1}
    message_set = MessageSetFactory.create(test_spec)
    assert type(message_set) is list
    assert len(message_set) == 1
    assert message_set[0] == 1
