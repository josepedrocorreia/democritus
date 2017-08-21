from __future__ import division

import numbers

import numpy as np
import yaml
from scipy import stats

from democritus.dynamics import ReplicatorDynamics, BestResponseDynamics, QuantalResponseDynamics
from democritus.exceptions import InvalidValueInSpecification, IncompatibilityInSpecification
from democritus.factories import BivariateFunctionFactory
from democritus.games import SimMaxGame, Game
from democritus.simulation import Simulation
from democritus.specification import Specification
from democritus.types import StateSet, StateMetricSpace, MessageSet, ElementSet, ActionSet


class ElementsFactory(object):
    @staticmethod
    def create(spec):
        spec_type = spec.get('type') or 'numbered labels'
        if spec_type == 'numbered labels':
            size = spec.get_or_fail('size')
            prefix = spec.get('prefix') or ''
            values = [prefix + str(number) for number in np.arange(1, size + 1)]
            return values
        if spec_type == 'numeric range':
            size = spec.get_or_fail('size')
            values = list(np.arange(1, size + 1))
            return values
        if spec_type == 'numeric interval':
            size = spec.get_or_fail('size')
            start = spec.get('start') or 0
            end = spec.get('end') or 1
            values = list(np.linspace(start=start, stop=end, num=size))
            return values
        else:
            raise InvalidValueInSpecification(spec, 'type', spec_type)


class PriorsFactory(object):
    @staticmethod
    def create(spec, elements):
        spec_type = spec.get('type') or 'uniform'
        if spec_type == 'uniform':
            return stats.uniform.pdf(list(range(len(elements))), scale=len(elements))
        if spec_type == 'normal':
            if not isinstance(elements[0], numbers.Number):
                raise ValueError('Priors type \'normal\' requires numeric elements')
            mean = spec.get('mean') or np.mean(elements)
            standard_deviation = spec.get('standard deviation') or np.std(elements, ddof=1)
            return stats.norm.pdf(elements, loc=mean, scale=standard_deviation)
        if spec_type == 'from file':
            file_name = spec.get_or_fail('file')
            return np.loadtxt(file_name, delimiter=',')
        else:
            raise InvalidValueInSpecification(spec, 'type', spec_type)


class MetricFactory(object):
    @staticmethod
    def create(spec, elements):
        spec_type = spec.get('type') or 'euclidean'
        if spec_type == 'euclidean':
            return np.array([[abs(x - y) for y in elements] for x in elements])
        if spec_type == 'from file':
            file_name = spec.get_or_fail('file')
            return np.loadtxt(file_name, delimiter=',')
        else:
            raise InvalidValueInSpecification(spec, 'type', spec_type)


class StatesFactory(object):
    @staticmethod
    def create(spec):
        spec_type = spec.get('type') or 'set'
        if spec_type == 'set':
            elements_spec = spec.get_or_fail('elements')
            priors_spec = spec.get('priors') or Specification.empty()
            elements = ElementsFactory.create(elements_spec)
            priors = PriorsFactory.create(priors_spec, elements)
            return StateSet(elements, priors)
        if spec_type == 'metric space':
            elements_spec = spec.get_or_fail('elements')
            priors_spec = spec.get('priors') or Specification.empty()
            metric_spec = spec.get('metric') or Specification.empty()
            elements = ElementsFactory.create(elements_spec)
            priors = PriorsFactory.create(priors_spec, elements)
            metric = MetricFactory.create(metric_spec, elements)
            return StateMetricSpace(elements, priors, metric)
        else:
            raise InvalidValueInSpecification(spec, 'type', spec_type)


class ElementSetFactory(object):
    @staticmethod
    def create(spec):
        spec_type = spec.get('type') or 'set'
        if spec_type == 'set':
            elements_spec = spec.get_or_fail('elements')
            elements = ElementsFactory.create(elements_spec)
            return ElementSet(elements)
        else:
            raise InvalidValueInSpecification(spec, 'type', spec_type)


class MessageSetFactory(object):
    @staticmethod
    def create(spec):
        element_set = ElementSetFactory.create(spec)
        return MessageSet(element_set.elements)


class ActionSetFactory(object):
    @staticmethod
    def create(spec):
        element_set = ElementSetFactory.create(spec)
        return ActionSet(element_set.elements)


class BivariateFunctionReader(object):
    @staticmethod
    def create(spec, states):
        spec_type = spec.get('type') or 'identity'
        if spec_type == 'identity':
            return BivariateFunctionFactory.create_identity(states.size())
        if spec_type == 'nosofsky':
            decay = spec.get('decay') or 1
            if not hasattr(states, 'distances'):
                raise IncompatibilityInSpecification(spec, 'states', 'utility')
            return BivariateFunctionFactory.create_nosofsky(states.distances, decay)
        if spec_type == 'from file':
            file_name = spec.get_or_fail('file')
            return BivariateFunctionFactory.read_from_file(file_name)
        else:
            raise InvalidValueInSpecification(spec, 'type', spec_type)


class GameFactory(object):
    @staticmethod
    def create(spec):
        spec_type = spec.get('type') or 'basic'
        states_spec = spec.get_or_fail('states')
        states = StatesFactory.create(states_spec)
        messages_spec = spec.get_or_fail('messages')
        messages = MessageSetFactory.create(messages_spec)
        utility_spec = spec.get('utility') or Specification.empty()
        utility = BivariateFunctionReader.create(utility_spec, states)
        imprecise = spec.get('imprecise') or False
        if spec_type == 'sim-max':
            similarity_spec = spec.get('similarity') or Specification.empty()
            similarity = BivariateFunctionReader.create(similarity_spec, states)
            return SimMaxGame(states, messages, utility, similarity, imprecise)
        if spec_type == 'basic':
            actions_spec = spec.get_or_fail('actions')
            actions = ActionSetFactory.create(actions_spec)
            return Game(states, messages, actions, utility)
        else:
            raise InvalidValueInSpecification(spec, 'type', spec_type)


class DynamicsFactory(object):
    @staticmethod
    def create(spec):
        dynamics_type = spec.get('type') or 'replicator'
        if dynamics_type == 'replicator':
            return ReplicatorDynamics()
        if dynamics_type == 'best response':
            return BestResponseDynamics()
        if dynamics_type == 'quantal response':
            rationality_spec = spec.get_or_fail('rationality')
            return QuantalResponseDynamics(rationality_spec)
        else:
            raise InvalidValueInSpecification(spec, 'type', dynamics_type)


class SimulationSpecReader(object):
    @staticmethod
    def read_from_file(filename):
        spec_file = open(filename, 'r')
        spec_dict = yaml.safe_load(spec_file)
        spec = Specification.from_dict(spec_dict)
        return SimulationSpecReader.read(spec)

    @staticmethod
    def read(spec):
        game_spec = spec.get_or_fail('game')
        dynamics_spec = spec.get_or_fail('dynamics')
        simulations_metrics = spec.get('metrics') or []
        game = GameFactory.create(game_spec)
        dynamics = DynamicsFactory.create(dynamics_spec)
        return Simulation(game, dynamics, simulations_metrics)
