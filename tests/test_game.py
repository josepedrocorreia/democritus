import pytest

from democritus.exceptions import *
from democritus.game import *
from democritus.specification import Specification


def test_game_factory_sim_max_3_5():
    game_spec = Specification.from_dict({'type': 'sim-max',
                                         'states': {'elements': {'type': 'numbered', 'size': 3}},
                                         'messages': {'elements': {'type': 'numbered', 'size': 5}}})
    game = GameFactory.create(game_spec)
    assert type(game) is SimMaxGame
    assert hasattr(game, 'states')
    assert game.states.size() == 3
    assert hasattr(game, 'messages')
    assert game.messages.size() == 5
    assert hasattr(game, 'actions')
    assert game.actions.size() == 3


def test_game_factory_missing_type_defaults_to_sim_max():
    game_spec = Specification.from_dict({'states': {'elements': {'type': 'numbered', 'size': 3}},
                                         'messages': {'elements': {'type': 'numbered', 'size': 5}}})
    game = GameFactory.create(game_spec)
    assert type(game) is SimMaxGame


def test_game_factory_missing_states_raises_exception():
    game_spec = Specification.from_dict({'type': 'sim-max',
                                         'messages': {'elements': {'type': 'numbered', 'size': 5}}})
    with pytest.raises(MissingFieldInSpecification):
        GameFactory.create(game_spec)


def test_game_factory_missing_messages_raises_exception():
    game_spec = Specification.from_dict({'type': 'sim-max',
                                         'states': {'elements': {'type': 'numbered', 'size': 3}}})
    with pytest.raises(MissingFieldInSpecification):
        GameFactory.create(game_spec)


def test_game_factory_unknown_type_raises_exception():
    game_spec = Specification.from_dict({'type': '????????????',
                                         'states': {'elements': {'type': 'numbered', 'size': 3}},
                                         'messages': {'elements': {'type': 'numbered', 'size': 5}}})
    with pytest.raises(InvalidValueInSpecification):
        GameFactory.create(game_spec)
