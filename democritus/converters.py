from __future__ import division

import numpy as np
import yaml
from scipy import stats

from democritus.collections import StateSet, MetricSpace, MessageSet
from democritus.dynamics import ReplicatorDynamics, BestResponseDynamics, QuantalResponseDynamics
from democritus.exceptions import InvalidValueInSpecification, IncompatibilityInSpecification
from democritus.factories import SimilarityFunctionFactory
from democritus.games import SimMaxGame
from democritus.metrics import ExpectedUtilityMetric, SenderNormalizedEntropyMetric, \
    ReceiverNormalizedEntropyMetric
from democritus.simulation import Simulation
from democritus.specification import Specification


class ElementsFactory(object):
    @staticmethod
    def create(spec):
        spec_type = spec.get('type') or 'numbered'
        if spec_type == 'numbered':
            size = spec.get_or_fail('size')
            return np.arange(1, size + 1)
        elif spec_type == 'interval':
            size = spec.get_or_fail('size')
            start = spec.get('start') or 0
            end = spec.get('end') or 1
            return np.linspace(start=start, stop=end, num=size)
        else:
            raise InvalidValueInSpecification(spec, 'type', spec_type)


class PriorsFactory(object):
    @staticmethod
    def create(spec, elements):
        spec_type = spec.get('type') or 'uniform'
        if spec_type == 'uniform':
            return stats.uniform.pdf(elements, scale=len(elements))
        elif spec_type == 'normal':
            mean = spec.get('mean') or np.mean(elements)
            standard_deviation = spec.get('standard deviation') or np.std(elements, ddof=1)
            return stats.norm.pdf(elements, loc=mean, scale=standard_deviation)
        else:
            raise InvalidValueInSpecification(spec, 'type', spec_type)


class MetricFactory(object):
    @staticmethod
    def create(spec, elements):
        spec_type = spec.get('type') or 'euclidean'
        if spec_type == 'euclidean':
            return np.array([[abs(x - y) for y in elements] for x in elements])
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
            return MetricSpace(elements, priors, metric)
        else:
            raise InvalidValueInSpecification(spec, 'type', spec_type)


class MessagesFactory(object):
    @staticmethod
    def create(spec):
        spec_type = spec.get('type') or 'set'
        if spec_type == 'set':
            elements_spec = spec.get_or_fail('elements')
            elements = ElementsFactory.create(elements_spec)
            return MessageSet(elements)
        else:
            raise InvalidValueInSpecification(spec, 'type', spec_type)


class SimilarityFunctionReader(object):
    @staticmethod
    def create(spec, states):
        spec_type = spec.get('type') or 'identity'
        if spec_type == 'identity':
            return SimilarityFunctionFactory.create_identity(states.size())
        if spec_type == 'nosofsky':
            decay = spec.get('decay') or 1
            if not hasattr(states, 'distances'):
                raise IncompatibilityInSpecification(spec, 'states', 'utility')
            return SimilarityFunctionFactory.create_nosofsky(states.distances, decay)
        else:
            raise InvalidValueInSpecification(spec, 'type', spec_type)


class GameFactory(object):
    @staticmethod
    def create(spec):
        spec_type = spec.get('type') or 'sim-max'
        states_spec = spec.get_or_fail('states')
        states = StatesFactory.create(states_spec)
        messages_spec = spec.get_or_fail('messages')
        messages = MessagesFactory.create(messages_spec)
        utility_spec = spec.get('utility') or Specification.empty()
        utility = SimilarityFunctionReader.create(utility_spec, states)
        if spec_type == 'sim-max':
            similarity_spec = spec.get('similarity') or Specification.empty()
            similarity = SimilarityFunctionReader.create(similarity_spec, states)
            imprecise = spec.get('imprecise') or False
            return SimMaxGame(states, messages, utility, similarity, imprecise)
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


class SimulationMetricConverter(object):
    @staticmethod
    def create(name):
        name = name.lower()
        if name == 'expected utility':
            return ExpectedUtilityMetric()
        elif name == 'sender entropy':
            return SenderNormalizedEntropyMetric()
        elif name == 'receiver entropy':
            return ReceiverNormalizedEntropyMetric()
        else:
            raise ValueError('Unknown simulation metric with name: %s', name)


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
        simulations_metrics_names = spec.get('metrics') or []
        game = GameFactory.create(game_spec)
        dynamics = DynamicsFactory.create(dynamics_spec)
        simulations_metrics = [SimulationMetricConverter.create(metric_name) for metric_name in
                               simulations_metrics_names]
        return Simulation(game, dynamics, simulations_metrics)
