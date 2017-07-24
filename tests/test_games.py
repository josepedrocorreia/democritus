from fixtures import *


# Game
def test_game_number_of_states(game):
    assert game.number_of_states() == 2


def test_game_number_of_messages(game):
    assert game.number_of_messages() == 2


def test_game_number_of_actions(game):
    assert game.number_of_actions() == 2


# SimMaxGame
def test_sim_max_game_actions_equal_states(sim_max_game):
    game = sim_max_game
    assert game.states.elements.tolist() == game.actions.elements.tolist()
