from __future__ import division

import numpy as np
import pytest
from fixtures import *

from democritus.collections import MessageSet, StateSet, MetricSpace
from democritus.converters import DynamicsFactory, ElementsFactory, SimilarityFunctionReader, StatesFactory, \
    GameFactory, MessagesFactory, MetricFactory, PriorsFactory, SimulationSpecReader, SimulationMetricConverter
from democritus.dynamics import ReplicatorDynamics, BestResponseDynamics, QuantalResponseDynamics
from democritus.exceptions import InvalidValueInSpecification, MissingFieldInSpecification, \
    IncompatibilityInSpecification
from democritus.games import SimMaxGame
from democritus.metrics import ExpectedUtilityMetric, ReceiverNormalizedEntropyMetric, \
    SenderNormalizedEntropyMetric
from democritus.specification import Specification


# ElementsFactory
def test_elements_factory_missing_type_defaults_to_numbered():
    elements_spec = Specification.from_dict({'size': 2})
    elements = ElementsFactory.create(elements_spec)
    assert elements.tolist() == [1, 2]


def test_elements_factory_numbered():
    elements_spec = Specification.from_dict({'type': 'numbered', 'size': 5})
    elements = ElementsFactory.create(elements_spec)
    assert elements.tolist() == [1, 2, 3, 4, 5]


def test_elements_factory_interval():
    elements_spec = Specification.from_dict({'type': 'interval', 'size': 5, 'start': 5, 'end': 9})
    elements = ElementsFactory.create(elements_spec)
    assert elements.tolist() == [5, 6, 7, 8, 9]


def test_elements_factory_numbered_missing_size_raises_exception():
    elements_spec = Specification.from_dict({'type': 'numbered'})
    with pytest.raises(MissingFieldInSpecification):
        ElementsFactory.create(elements_spec)


def test_elements_factory_interval_missing_size_raises_exception():
    elements_spec = Specification.from_dict({'type': 'interval', 'start': 5, 'end': 9})
    with pytest.raises(MissingFieldInSpecification):
        ElementsFactory.create(elements_spec)


def test_elements_factory_interval_missing_start_defaults_to_0():
    elements_spec = Specification.from_dict({'type': 'interval', 'size': 5, 'end': 4})
    elements = ElementsFactory.create(elements_spec)
    assert elements.tolist() == [0, 1, 2, 3, 4]


def test_elements_factory_interval_missing_end_defaults_to_1():
    elements_spec = Specification.from_dict({'type': 'interval', 'size': 3, 'start': 0.5})
    elements = ElementsFactory.create(elements_spec)
    assert elements.tolist() == [0.5, 0.75, 1]


def test_elements_factory_unknown_type_raises_exception():
    elements_spec = Specification.from_dict({'type': '????????'})
    with pytest.raises(InvalidValueInSpecification):
        ElementsFactory.create(elements_spec)


# PriorsFactory
def test_priors_factory_uniform():
    priors_spec = Specification.from_dict({'type': 'uniform'})

    priors_1 = PriorsFactory.create(priors_spec, [1])
    assert priors_1.tolist() == [1]

    priors_3 = PriorsFactory.create(priors_spec, [1, 2, 3])
    assert priors_3.tolist() == [1 / 3, 1 / 3, 1 / 3]


def test_priors_factory_normal():
    priors_spec = Specification.from_dict({'type': 'normal', 'mean': 3, 'standard deviation': 1})

    priors_3 = PriorsFactory.create(priors_spec, [1, 2, 3, 4, 5])
    assert np.round(priors_3, decimals=3).tolist() == [0.054, 0.242, 0.399, 0.242, 0.054]


def test_priors_factory_missing_type_defaults_to_uniform():
    priors_spec = Specification.empty()
    priors_3 = PriorsFactory.create(priors_spec, [1, 2, 3])
    assert priors_3.tolist() == [1 / 3, 1 / 3, 1 / 3]


def test_priors_factory_unknown_type_raises_exception():
    priors_spec = Specification.from_dict({'type': '?????????'})
    with pytest.raises(InvalidValueInSpecification):
        PriorsFactory.create(priors_spec, [1])


def test_priors_factory_missing_mean_defaults_to_estimate():
    priors_spec = Specification.from_dict({'type': 'normal', 'standard deviation': 1})
    priors = PriorsFactory.create(priors_spec, [1, 2, 3, 4, 5])
    assert np.round(priors, decimals=3).tolist() == [0.054, 0.242, 0.399, 0.242, 0.054]


def test_priors_factory_missing_standard_deviation_defaults_to_estimate():
    priors_spec = Specification.from_dict({'type': 'normal', 'mean': 3})
    priors = PriorsFactory.create(priors_spec, [1, 2, 3, 4, 5])
    assert np.round(priors, decimals=3).tolist() == [0.113, 0.207, 0.252, 0.207, 0.113]


def test_dynamics_factory_types():
    dynamics_spec = Specification.from_dict({'type': 'replicator'})
    assert type(DynamicsFactory.create(dynamics_spec)) is ReplicatorDynamics

    dynamics_spec = Specification.from_dict({'type': 'best response'})
    assert type(DynamicsFactory.create(dynamics_spec)) is BestResponseDynamics

    dynamics_spec = Specification.from_dict({'type': 'quantal response', 'rationality': 10})
    assert type(DynamicsFactory.create(dynamics_spec)) is QuantalResponseDynamics


# MetricFactory
def test_metric_factory_euclidean():
    metric_spec = Specification.from_dict({'type': 'euclidean'})

    metric_1 = MetricFactory.create(metric_spec, [1])
    assert metric_1[0].tolist() == [0]

    metric_3 = MetricFactory.create(metric_spec, [1, 2, 3])
    assert metric_3[0].tolist() == [0, 1, 2]
    assert metric_3[1].tolist() == [1, 0, 1]
    assert metric_3[2].tolist() == [2, 1, 0]

    other_metric_3 = MetricFactory.create(metric_spec, [1, 2, 5])
    assert other_metric_3[0].tolist() == [0, 1, 4]
    assert other_metric_3[1].tolist() == [1, 0, 3]
    assert other_metric_3[2].tolist() == [4, 3, 0]


def test_metric_factory_missing_type_defaults_to_euclidean():
    metric_spec = Specification.empty()
    metric_3 = MetricFactory.create(metric_spec, [1, 2, 3])
    assert metric_3[0].tolist() == [0, 1, 2]
    assert metric_3[1].tolist() == [1, 0, 1]
    assert metric_3[2].tolist() == [2, 1, 0]


def test_metric_factory_unknown_type_raises_exception():
    metric_spec = Specification.from_dict({'type': '????????'})
    with pytest.raises(InvalidValueInSpecification):
        MetricFactory.create(metric_spec, [1, 2, 3])


# StatesFactory
def test_states_factory_set():
    states_spec = Specification.from_dict({'type': 'set',
                                           'elements': {'type': 'numbered', 'size': 3},
                                           'priors': {'type': 'uniform'}})
    states = StatesFactory.create(states_spec)
    assert type(states) is StateSet
    assert states.elements.tolist() == [1, 2, 3]
    assert states.priors.tolist() == [1 / 3, 1 / 3, 1 / 3]


def test_states_factory_metric_space():
    states_spec = Specification.from_dict({'type': 'metric space',
                                           'elements': {'type': 'numbered', 'size': 3},
                                           'priors': {'type': 'uniform'},
                                           'metric': {'type': 'euclidean'}})
    states = StatesFactory.create(states_spec)
    assert type(states) is MetricSpace
    assert states.elements.tolist() == [1, 2, 3]
    assert states.priors.tolist() == [1 / 3, 1 / 3, 1 / 3]
    assert states.distances[0].tolist() == [0, 1, 2]
    assert states.distances[1].tolist() == [1, 0, 1]
    assert states.distances[2].tolist() == [2, 1, 0]


def test_states_factory_missing_type_defaults_to_set():
    states_spec = Specification.from_dict({'elements': {'type': 'numbered', 'size': 3},
                                           'priors': {'type': 'uniform'}})
    states = StatesFactory.create(states_spec)
    assert type(states) is StateSet
    assert states.elements.tolist() == [1, 2, 3]
    assert states.priors.tolist() == [1 / 3, 1 / 3, 1 / 3]


def test_states_factory_set_missing_priors_default_to_uniform():
    states_spec = Specification.from_dict({'type': 'set',
                                           'elements': {'type': 'numbered', 'size': 3}})
    states = StatesFactory.create(states_spec)
    assert type(states) is StateSet
    assert states.elements.tolist() == [1, 2, 3]
    assert states.priors.tolist() == [1 / 3, 1 / 3, 1 / 3]


def test_states_factory_set_missing_elements_raises_exception():
    states_spec = Specification.from_dict({'type': 'set',
                                           'priors': {'type': 'uniform'}})
    with pytest.raises(MissingFieldInSpecification):
        StatesFactory.create(states_spec)


def test_states_factory_metric_space_missing_priors_defaults_to_uniform():
    states_spec = Specification.from_dict({'type': 'metric space',
                                           'elements': {'type': 'numbered', 'size': 3},
                                           'metric': {'type': 'euclidean'}})
    states = StatesFactory.create(states_spec)
    assert type(states) is MetricSpace
    assert states.elements.tolist() == [1, 2, 3]
    assert states.priors.tolist() == [1 / 3, 1 / 3, 1 / 3]
    assert states.distances[0].tolist() == [0, 1, 2]
    assert states.distances[1].tolist() == [1, 0, 1]
    assert states.distances[2].tolist() == [2, 1, 0]


def test_states_factory_metric_space_missing_metric_defaults_to_euclidean():
    states_spec = Specification.from_dict({'type': 'metric space',
                                           'elements': {'type': 'numbered', 'size': 3},
                                           'priors': {'type': 'uniform'}})
    states = StatesFactory.create(states_spec)
    assert type(states) is MetricSpace
    assert states.elements.tolist() == [1, 2, 3]
    assert states.priors.tolist() == [1 / 3, 1 / 3, 1 / 3]
    assert states.distances[0].tolist() == [0, 1, 2]
    assert states.distances[1].tolist() == [1, 0, 1]
    assert states.distances[2].tolist() == [2, 1, 0]


def test_states_factory_metric_space_missing_elements_raises_exception():
    states_spec = Specification.from_dict({'type': 'metric space',
                                           'priors': {'type': 'uniform'},
                                           'metric': {'type': 'euclidean'}})
    with pytest.raises(MissingFieldInSpecification):
        StatesFactory.create(states_spec)


def test_states_factory_unknown_type_raises_exception():
    states_spec = Specification.from_dict({'type': '???????????',
                                           'elements': {'type': 'numbered', 'size': 3},
                                           'priors': {'type': 'uniform'}})
    with pytest.raises(InvalidValueInSpecification):
        StatesFactory.create(states_spec)


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


# SimilarityFunctionReader
def test_similarity_function_reader_create_identity(states):
    similarity_spec = Specification.from_dict({'type': 'identity'})
    similarity = SimilarityFunctionReader.create(similarity_spec, states)
    assert np.round(similarity[0], decimals=3).tolist() == [1, 0, 0]
    assert np.round(similarity[1], decimals=3).tolist() == [0, 1, 0]
    assert np.round(similarity[2], decimals=3).tolist() == [0, 0, 1]


def test_similarity_function_reader_create_nosofsky(states):
    similarity_spec = Specification.from_dict({'type': 'nosofsky', 'decay': 2})
    similarity = SimilarityFunctionReader.create(similarity_spec, states)
    assert np.round(similarity[0], decimals=3).tolist() == [1, 0.779, 0.368]
    assert np.round(similarity[1], decimals=3).tolist() == [0.779, 1, 0.779]
    assert np.round(similarity[2], decimals=3).tolist() == [0.368, 0.779, 1]


def test_similarity_function_reader_unknown_type_raises_exception(states):
    similarity_spec = Specification.from_dict({'type': '???????????'})
    with pytest.raises(InvalidValueInSpecification):
        SimilarityFunctionReader.create(similarity_spec, states)


def test_similarity_function_reader_missing_type_defaults_to_identity(states):
    similarity_spec = Specification.from_dict({'decay': 2})
    similarity = SimilarityFunctionReader.create(similarity_spec, states)
    assert np.round(similarity[0], decimals=3).tolist() == [1, 0, 0]
    assert np.round(similarity[1], decimals=3).tolist() == [0, 1, 0]
    assert np.round(similarity[2], decimals=3).tolist() == [0, 0, 1]


def test_similarity_function_reader_nosofsky_without_distance_raises_exception():
    states_spec_set = Specification.from_dict({'type': 'set', 'elements': {'type': 'numbered', 'size': 3}})
    states_set = StatesFactory.create(states_spec_set)
    utility_spec = Specification.from_dict({'type': 'nosofsky', 'decay': 2})
    with pytest.raises(IncompatibilityInSpecification):
        SimilarityFunctionReader.create(utility_spec, states_set)


def test_similarity_function_reader_nosofsky_missing_decay_defaults_to_1(states):
    similarity_spec = Specification.from_dict({'type': 'nosofsky'})
    similarity = SimilarityFunctionReader.create(similarity_spec, states)
    assert np.round(similarity[0], decimals=3).tolist() == [1, 0.368, 0.018]
    assert np.round(similarity[1], decimals=3).tolist() == [0.368, 1, 0.368]
    assert np.round(similarity[2], decimals=3).tolist() == [0.018, 0.368, 1]


# GameFactory
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


# DynamicsFactory
def test_dynamics_factory_missing_type_defaults_to_replicator():
    dynamics_spec = Specification.empty()
    dynamics = DynamicsFactory.create(dynamics_spec)
    assert type(dynamics) is ReplicatorDynamics


def test_dynamics_factory_unknown_type_raises_exception():
    dynamics_spec = Specification.from_dict({'type': '???????'})
    with pytest.raises(InvalidValueInSpecification):
        DynamicsFactory.create(dynamics_spec)


def test_dynamics_factory_quantal_response_missing_rationality_raises_exception():
    dynamics_spec = Specification.from_dict({'type': 'quantal response'})
    with pytest.raises(MissingFieldInSpecification):
        DynamicsFactory.create(dynamics_spec)


# SimulationMetricConverter
def test_simulation_metrics_create_expected_utility():
    metric = SimulationMetricConverter.create('expected utility')
    assert type(metric) is ExpectedUtilityMetric


def test_simulation_metrics_create_expected_utility_case_insensitive():
    metric = SimulationMetricConverter.create('eXpEcTeD UtIlItY')
    assert type(metric) is ExpectedUtilityMetric


def test_simulation_metrics_create_sender_entropy():
    metric = SimulationMetricConverter.create('sender entropy')
    assert type(metric) is SenderNormalizedEntropyMetric


def test_simulation_metrics_create_receiver_entropy():
    metric = SimulationMetricConverter.create('receiver entropy')
    assert type(metric) is ReceiverNormalizedEntropyMetric


def test_simulation_metrics_create_unknown_metric_throws_exception():
    with pytest.raises(ValueError):
        SimulationMetricConverter.create('?????????????')


# SimulationSpecReader
def test_read_sim_max_3_5_replicator_with_metrics():
    simulation_spec = Specification.from_dict({'game': {'type': 'sim-max',
                                                        'states': {'elements': {'type': 'numbered', 'size': 3}},
                                                        'messages': {'elements': {'type': 'numbered', 'size': 5}}},
                                               'dynamics': {'type': 'replicator'},
                                               'metrics': ['expected utility']})
    simulation = SimulationSpecReader.read(simulation_spec)
    assert type(simulation.game) is SimMaxGame
    assert type(simulation.dynamics) is ReplicatorDynamics
    assert len(simulation.simulation_measurements) == 1
    assert type(simulation.simulation_measurements[0][0]) is ExpectedUtilityMetric
    assert len(simulation.simulation_measurements[0][1]) == 1


def test_read_missing_game_throws_exception():
    simulation_spec = Specification.from_dict({'dynamics': {'type': 'replicator'}})
    with pytest.raises(MissingFieldInSpecification):
        SimulationSpecReader.read(simulation_spec)


def test_read_missing_dynamics_throws_exception():
    simulation_spec = Specification.from_dict({'game': {'type': 'sim-max',
                                                        'states': {'elements': {'type': 'numbered', 'size': 3}},
                                                        'messages': {'elements': {'type': 'numbered', 'size': 5}}}})
    with pytest.raises(MissingFieldInSpecification):
        SimulationSpecReader.read(simulation_spec)


def test_read_missing_metrics_throws_exception():
    simulation_spec = Specification.from_dict({'game': {'type': 'sim-max',
                                                        'states': {'elements': {'type': 'numbered', 'size': 3}},
                                                        'messages': {'elements': {'type': 'numbered', 'size': 5}}},
                                               'dynamics': {'type': 'replicator'},
                                               'metrics': ['expected utility']})
    simulation = SimulationSpecReader.read(simulation_spec)
    assert type(simulation.game) is SimMaxGame
    assert type(simulation.dynamics) is ReplicatorDynamics
    assert len(simulation.simulation_measurements) == 1
    assert type(simulation.simulation_measurements[0][0]) is ExpectedUtilityMetric
    assert len(simulation.simulation_measurements[0][1]) == 1
