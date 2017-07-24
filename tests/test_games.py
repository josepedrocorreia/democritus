class TestGame(object):
    def test_number_of_states(self, game):
        assert game.number_of_states() == 2

    def test_number_of_messages(self, game):
        assert game.number_of_messages() == 2

    def test_number_of_actions(self, game):
        assert game.number_of_actions() == 2


class TestSimMaxGame(object):
    def test_sim_max_game_actions_equal_states(self, sim_max_game):
        game = sim_max_game
        assert game.states.elements.tolist() == game.actions.elements.tolist()
