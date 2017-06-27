import copy

from democritus.exceptions import InvalidValueInSpecification
from democritus.messages import MessagesFactory
from democritus.specification import Specification
from democritus.states import StatesFactory
from democritus.utility import UtilityFactory


class GameFactory(object):
    @staticmethod
    def create(spec):
        spec_type = spec.get('type') or 'sim-max'
        if spec_type == 'sim-max':
            states_spec = spec.get_or_fail('states')
            messages_spec = spec.get_or_fail('messages')
            utility_spec = spec.get('utility') or Specification.from_dict({})
            states = StatesFactory.create(states_spec)
            messages = MessagesFactory.create(messages_spec)
            utility = UtilityFactory.create(utility_spec, states)
            return SimMaxGame(states, messages, utility)
        else:
            raise InvalidValueInSpecification(spec, 'type', spec_type)


class Game(object):
    def __init__(self, states, messages, actions, utility):
        self.states = states
        self.messages = messages
        self.actions = actions
        self.utility = utility


class SimMaxGame(Game):
    def __init__(self, states, messages, utility):
        actions = copy.deepcopy(states)
        Game.__init__(self, states, messages, actions, utility)
