import copy


class Game(object):
    def __init__(self, states, messages, actions, utility):
        self.states = states
        self.messages = messages
        self.actions = actions
        self.utility = utility

    def number_of_states(self):
        return self.states.size()

    def number_of_messages(self):
        return self.messages.size()

    def number_of_actions(self):
        return self.actions.size()


class SimMaxGame(Game):
    def __init__(self, states, messages, utility, similarity, imprecise):
        actions = copy.deepcopy(states)
        Game.__init__(self, states, messages, actions, utility)
        self.similarity = similarity
        self.imprecise = imprecise
