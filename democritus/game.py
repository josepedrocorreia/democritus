import copy

from democritus.exceptions import InvalidValueInSpecification
from democritus.messages import MessagesFactory
from democritus.similarity import SimilarityFunctionReader
from democritus.specification import Specification
from democritus.states import StatesFactory


class GameFactory(object):
    @staticmethod
    def create(spec):
        spec_type = spec.get('type') or 'sim-max'
        states_spec = spec.get_or_fail('states')
        states = StatesFactory.create(states_spec)
        messages_spec = spec.get_or_fail('messages')
        messages = MessagesFactory.create(messages_spec)
        utility_spec = spec.get('utility') or Specification.from_dict({})
        utility = SimilarityFunctionReader.create(utility_spec, states)
        if spec_type == 'sim-max':
            similarity_spec = spec.get('similarity') or Specification.from_dict({})
            similarity = SimilarityFunctionReader.create(similarity_spec, states)
            imprecise = spec.get('imprecise') or False
            return SimMaxGame(states, messages, utility, similarity, imprecise)
        else:
            raise InvalidValueInSpecification(spec, 'type', spec_type)


class Game(object):
    def __init__(self, states, messages, actions, utility):
        self.states = states
        self.messages = messages
        self.actions = actions
        self.utility = utility


class SimMaxGame(Game):
    def __init__(self, states, messages, utility, similarity, imprecise):
        actions = copy.deepcopy(states)
        Game.__init__(self, states, messages, actions, utility)
        self.similarity = similarity
        self.imprecise = imprecise
