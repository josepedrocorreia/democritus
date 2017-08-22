from __future__ import division

import numpy as np
import pytest

from democritus.converters import DynamicsFactory, ElementsFactory, BivariateFunctionReader, StatesFactory, \
    GameFactory, MetricFactory, PriorsFactory, SimulationSpecReader, ElementSetFactory, MessageSetFactory, \
    ActionSetFactory
from democritus.dynamics import ReplicatorDynamics, BestResponseDynamics, QuantalResponseDynamics
from democritus.exceptions import InvalidValueInSpecification, MissingFieldInSpecification, \
    IncompatibilityInSpecification
from democritus.games import SimMaxGame, Game
from democritus.metrics import ExpectedUtilityMetric
from democritus.specification import Specification
from democritus.types import StateSet, StateMetricSpace, ElementSet, MessageSet, ActionSet


class TestElementsFactory(object):
    def test_missing_type_defaults_to_numbered_labels(self):
        elements_spec = Specification.from_dict({'size': 2})
        elements = ElementsFactory.create(elements_spec)
        assert elements == ['1', '2']

    def test_numbered_labels(self):
        elements_spec = Specification.from_dict({'type': 'numbered labels', 'size': 5})
        elements = ElementsFactory.create(elements_spec)
        assert elements == ['1', '2', '3', '4', '5']

    def test_numbered_labels_with_prefix(self):
        elements_spec = Specification.from_dict({'type': 'numbered labels', 'size': 5, 'prefix': 'test'})
        elements = ElementsFactory.create(elements_spec)
        assert elements == ['test1', 'test2', 'test3', 'test4', 'test5']

    def test_numeric_range(self):
        elements_spec = Specification.from_dict({'type': 'numeric range', 'size': 5})
        elements = ElementsFactory.create(elements_spec)
        assert elements == [1, 2, 3, 4, 5]

    def test_numeric_interval(self):
        elements_spec = Specification.from_dict({'type': 'numeric interval', 'size': 3, 'start': 5, 'end': 9})
        elements = ElementsFactory.create(elements_spec)
        assert elements == [5, 7, 9]

    def test_numbered_labels_missing_size_raises_exception(self):
        elements_spec = Specification.from_dict({'type': 'numbered labels'})
        with pytest.raises(MissingFieldInSpecification):
            ElementsFactory.create(elements_spec)

    def test_numeric_range_missing_size_raises_exception(self):
        elements_spec = Specification.from_dict({'type': 'numeric range'})
        with pytest.raises(MissingFieldInSpecification):
            ElementsFactory.create(elements_spec)

    def test_numeric_interval_missing_size_raises_exception(self):
        elements_spec = Specification.from_dict({'type': 'numeric interval', 'start': 5, 'end': 9})
        with pytest.raises(MissingFieldInSpecification):
            ElementsFactory.create(elements_spec)

    def test_interval_missing_start_defaults_to_0(self):
        elements_spec = Specification.from_dict({'type': 'numeric interval', 'size': 5, 'end': 4})
        elements = ElementsFactory.create(elements_spec)
        assert elements == [0, 1, 2, 3, 4]

    def test_interval_missing_end_defaults_to_1(self):
        elements_spec = Specification.from_dict({'type': 'numeric interval', 'size': 3, 'start': 0.5})
        elements = ElementsFactory.create(elements_spec)
        assert elements == [0.5, 0.75, 1]

    def test_unknown_type_raises_exception(self):
        elements_spec = Specification.from_dict({'type': '????????'})
        with pytest.raises(InvalidValueInSpecification):
            ElementsFactory.create(elements_spec)


class TestPriorsFactory(object):
    def test_uniform(self):
        priors_spec = Specification.from_dict({'type': 'uniform'})

        priors_1 = PriorsFactory.create(priors_spec, [1])
        assert priors_1.tolist() == [1]

        priors_3 = PriorsFactory.create(priors_spec, [1, 2, 3])
        assert priors_3.tolist() == [1 / 3, 1 / 3, 1 / 3]

    def test_normal(self):
        priors_spec = Specification.from_dict({'type': 'normal', 'mean': 3, 'standard deviation': 1})

        priors_3 = PriorsFactory.create(priors_spec, [1, 2, 3, 4, 5])
        assert np.round(priors_3, decimals=3).tolist() == [0.054, 0.242, 0.399, 0.242, 0.054]

    def test_from_file(self, tmpdir):
        priors_file_content = '''
            0.0
            0.15
            0.5
            0.35\
        '''
        priors_file = tmpdir.join("test_priors.csv")
        priors_file.write(priors_file_content)
        priors_spec = Specification.from_dict({'type': 'from file', 'file': str(priors_file)})
        priors = PriorsFactory.create(priors_spec, [1, 2, 3, 4])
        assert priors.tolist() == [0.0, 0.15, 0.5, 0.35]

    def test_missing_type_defaults_to_uniform(self):
        priors_spec = Specification.empty()
        priors_3 = PriorsFactory.create(priors_spec, [1, 2, 3])
        assert priors_3.tolist() == [1 / 3, 1 / 3, 1 / 3]

    def test_unknown_type_raises_exception(self):
        priors_spec = Specification.from_dict({'type': '?????????'})
        with pytest.raises(InvalidValueInSpecification):
            PriorsFactory.create(priors_spec, [1])

    def test_normal_with_non_numeric_elements_raises_exception(self):
        priors_spec = Specification.from_dict({'type': 'normal', 'mean': 3, 'standard deviation': 1})
        with pytest.raises(ValueError):
            PriorsFactory.create(priors_spec, ['1', '2', '3', '4', '5'])

    def test_missing_mean_defaults_to_estimate(self):
        priors_spec = Specification.from_dict({'type': 'normal', 'standard deviation': 1})
        priors = PriorsFactory.create(priors_spec, [1, 2, 3, 4, 5])
        assert np.round(priors, decimals=3).tolist() == [0.054, 0.242, 0.399, 0.242, 0.054]

    def test_missing_standard_deviation_defaults_to_estimate(self):
        priors_spec = Specification.from_dict({'type': 'normal', 'mean': 3})
        priors = PriorsFactory.create(priors_spec, [1, 2, 3, 4, 5])
        assert np.round(priors, decimals=3).tolist() == [0.113, 0.207, 0.252, 0.207, 0.113]

    def test_missing_file_raises_exception(self):
        priors_spec = Specification.from_dict({'type': 'from file'})
        with pytest.raises(MissingFieldInSpecification):
            PriorsFactory.create(priors_spec, [1, 2, 3, 4])

    def test_unknown_file_raises_exception(self):
        priors_spec = Specification.from_dict({'type': 'from file', 'file': 'some-non-existing-file.bat'})
        with pytest.raises(IOError):
            PriorsFactory.create(priors_spec, [1, 2, 3, 4])


class TestMetricFactory(object):
    def test_create_euclidean(self):
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

    def test_create_from_file(self, tmpdir):
        metric_file_content = '''
            0.0,  0.4,  0.6
            0.15, 0.05, 0.8
            0.3,  0.3,  0.4\
        '''
        metric_file = tmpdir.join("test_priors.csv")
        metric_file.write(metric_file_content)
        metric_spec = Specification.from_dict({'type': 'from file', 'file': str(metric_file)})
        metric = MetricFactory.create(metric_spec, ['a', 'b', 'c'])
        assert metric[0].tolist() == [0, 0.4, 0.6]
        assert metric[1].tolist() == [0.15, 0.05, 0.8]
        assert metric[2].tolist() == [0.3, 0.3, 0.4]

    def test_missing_type_defaults_to_euclidean(self):
        metric_spec = Specification.empty()
        metric_3 = MetricFactory.create(metric_spec, [1, 2, 3])
        assert metric_3[0].tolist() == [0, 1, 2]
        assert metric_3[1].tolist() == [1, 0, 1]
        assert metric_3[2].tolist() == [2, 1, 0]

    def test_unknown_type_raises_exception(self):
        metric_spec = Specification.from_dict({'type': '????????'})
        with pytest.raises(InvalidValueInSpecification):
            MetricFactory.create(metric_spec, [1, 2, 3])


class TestStatesFactory(object):
    def test_set(self):
        states_spec = Specification.from_dict({'type': 'set',
                                               'elements': {'type': 'numbered labels', 'size': 3},
                                               'priors': {'type': 'uniform'}})
        states = StatesFactory.create(states_spec)
        assert type(states) is StateSet
        assert states.elements == ['1', '2', '3']
        assert states.priors.tolist() == [1 / 3, 1 / 3, 1 / 3]

    def test_metric_space(self):
        states_spec = Specification.from_dict({'type': 'metric space',
                                               'elements': {'type': 'numeric range', 'size': 3},
                                               'priors': {'type': 'uniform'},
                                               'metric': {'type': 'euclidean'}})
        states = StatesFactory.create(states_spec)
        assert type(states) is StateMetricSpace
        assert states.elements == [1, 2, 3]
        assert states.priors.tolist() == [1 / 3, 1 / 3, 1 / 3]
        assert states.distances[0].tolist() == [0, 1, 2]
        assert states.distances[1].tolist() == [1, 0, 1]
        assert states.distances[2].tolist() == [2, 1, 0]

    def test_missing_type_defaults_to_set(self):
        states_spec = Specification.from_dict({'elements': {'type': 'numbered labels', 'size': 3},
                                               'priors': {'type': 'uniform'}})
        states = StatesFactory.create(states_spec)
        assert type(states) is StateSet
        assert states.elements == ['1', '2', '3']
        assert states.priors.tolist() == [1 / 3, 1 / 3, 1 / 3]

    def test_set_missing_priors_default_to_uniform(self):
        states_spec = Specification.from_dict({'type': 'set',
                                               'elements': {'type': 'numbered labels', 'size': 3}})
        states = StatesFactory.create(states_spec)
        assert type(states) is StateSet
        assert states.elements == ['1', '2', '3']
        assert states.priors.tolist() == [1 / 3, 1 / 3, 1 / 3]

    def test_set_missing_elements_raises_exception(self):
        states_spec = Specification.from_dict({'type': 'set',
                                               'priors': {'type': 'uniform'}})
        with pytest.raises(MissingFieldInSpecification):
            StatesFactory.create(states_spec)

    def test_metric_space_missing_priors_defaults_to_uniform(self):
        states_spec = Specification.from_dict({'type': 'metric space',
                                               'elements': {'type': 'numeric range', 'size': 3},
                                               'metric': {'type': 'euclidean'}})
        states = StatesFactory.create(states_spec)
        assert type(states) is StateMetricSpace
        assert states.elements == [1, 2, 3]
        assert states.priors.tolist() == [1 / 3, 1 / 3, 1 / 3]
        assert states.distances[0].tolist() == [0, 1, 2]
        assert states.distances[1].tolist() == [1, 0, 1]
        assert states.distances[2].tolist() == [2, 1, 0]

    def test_metric_space_missing_metric_defaults_to_euclidean(self):
        states_spec = Specification.from_dict({'type': 'metric space',
                                               'elements': {'type': 'numeric range', 'size': 3},
                                               'priors': {'type': 'uniform'}})
        states = StatesFactory.create(states_spec)
        assert type(states) is StateMetricSpace
        assert states.elements == [1, 2, 3]
        assert states.priors.tolist() == [1 / 3, 1 / 3, 1 / 3]
        assert states.distances[0].tolist() == [0, 1, 2]
        assert states.distances[1].tolist() == [1, 0, 1]
        assert states.distances[2].tolist() == [2, 1, 0]

    def test_metric_space_missing_elements_raises_exception(self):
        states_spec = Specification.from_dict({'type': 'metric space',
                                               'priors': {'type': 'uniform'},
                                               'metric': {'type': 'euclidean'}})
        with pytest.raises(MissingFieldInSpecification):
            StatesFactory.create(states_spec)

    def test_unknown_type_raises_exception(self):
        states_spec = Specification.from_dict({'type': '???????????',
                                               'elements': {'type': 'numbered labels', 'size': 3},
                                               'priors': {'type': 'uniform'}})
        with pytest.raises(InvalidValueInSpecification):
            StatesFactory.create(states_spec)


class TestElementSetFactory(object):
    def test_five_elements(self):
        element_set_spec = Specification.from_dict({'type': 'set', 'elements': {'type': 'numbered labels', 'size': 5}})
        element_set = ElementSetFactory.create(element_set_spec)
        assert type(element_set) is ElementSet
        assert element_set.size() == 5
        assert element_set.elements == ['1', '2', '3', '4', '5']

    def test_unknown_type_raises_exception(self):
        element_set_spec = Specification.from_dict(
            {'type': '????????', 'elements': {'type': 'numbered labels', 'size': 5}})
        with pytest.raises(InvalidValueInSpecification):
            ElementSetFactory.create(element_set_spec)

    def test_missing_type_defaults_to_set(self):
        element_set_spec = Specification.from_dict({'elements': {'type': 'numbered labels', 'size': 5}})
        element_set = ElementSetFactory.create(element_set_spec)
        assert type(element_set) is ElementSet
        assert element_set.size() == 5
        assert element_set.elements == ['1', '2', '3', '4', '5']

    def test_missing_elements_raises_exception(self):
        element_set_spec = Specification.from_dict({'type': 'set'})
        with pytest.raises(MissingFieldInSpecification):
            ElementSetFactory.create(element_set_spec)


class TestMessageSetFactory(object):
    def test_five_elements(self):
        element_set_spec = Specification.from_dict({'type': 'set', 'elements': {'type': 'numbered labels', 'size': 5}})
        element_set = MessageSetFactory.create(element_set_spec)
        assert type(element_set) is MessageSet
        assert element_set.size() == 5
        assert element_set.elements == ['1', '2', '3', '4', '5']


class TestActionSetFactory(object):
    def test_five_elements(self):
        element_set_spec = Specification.from_dict({'type': 'set', 'elements': {'type': 'numbered labels', 'size': 5}})
        element_set = ActionSetFactory.create(element_set_spec)
        assert type(element_set) is ActionSet
        assert element_set.size() == 5
        assert element_set.elements == ['1', '2', '3', '4', '5']


class TestBivariateFunctionReader(object):
    def test_create_identity(self, states):
        func_spec = Specification.from_dict({'type': 'identity'})
        func = BivariateFunctionReader.create(func_spec, states)
        assert np.round(func[0], decimals=3).tolist() == [1, 0, 0]
        assert np.round(func[1], decimals=3).tolist() == [0, 1, 0]
        assert np.round(func[2], decimals=3).tolist() == [0, 0, 1]

    def test_create_nosofsky(self, states):
        func_spec = Specification.from_dict({'type': 'nosofsky', 'decay': 2})
        func = BivariateFunctionReader.create(func_spec, states)
        assert np.round(func[0], decimals=3).tolist() == [1, 0.779, 0.368]
        assert np.round(func[1], decimals=3).tolist() == [0.779, 1, 0.779]
        assert np.round(func[2], decimals=3).tolist() == [0.368, 0.779, 1]

    def test_create_from_file(self, tmpdir, states):
        func_file_content = '''
            0.0,  0.4,  0.6
            0.15, 0.05, 0.8
            0.3,  0.3,  0.4\
        '''
        func_file = tmpdir.join("test_priors.csv")
        func_file.write(func_file_content)
        func_spec = Specification.from_dict({'type': 'from file', 'file': str(func_file)})
        func = BivariateFunctionReader.create(func_spec, states)
        assert func[0].tolist() == [0, 0.4, 0.6]
        assert func[1].tolist() == [0.15, 0.05, 0.8]
        assert func[2].tolist() == [0.3, 0.3, 0.4]

    def test_unknown_type_raises_exception(self, states):
        func_spec = Specification.from_dict({'type': '???????????'})
        with pytest.raises(InvalidValueInSpecification):
            BivariateFunctionReader.create(func_spec, states)

    def test_missing_type_defaults_to_identity(self, states):
        func_spec = Specification.from_dict({'decay': 2})
        func = BivariateFunctionReader.create(func_spec, states)
        assert np.round(func[0], decimals=3).tolist() == [1, 0, 0]
        assert np.round(func[1], decimals=3).tolist() == [0, 1, 0]
        assert np.round(func[2], decimals=3).tolist() == [0, 0, 1]

    def test_nosofsky_without_distance_raises_exception(self):
        states_spec_set = Specification.from_dict({'type': 'set', 'elements': {'type': 'numbered labels', 'size': 3}})
        states_set = StatesFactory.create(states_spec_set)
        utility_spec = Specification.from_dict({'type': 'nosofsky', 'decay': 2})
        with pytest.raises(IncompatibilityInSpecification):
            BivariateFunctionReader.create(utility_spec, states_set)

    def test_nosofsky_missing_decay_defaults_to_1(self, states):
        func_spec = Specification.from_dict({'type': 'nosofsky'})
        func = BivariateFunctionReader.create(func_spec, states)
        assert np.round(func[0], decimals=3).tolist() == [1, 0.368, 0.018]
        assert np.round(func[1], decimals=3).tolist() == [0.368, 1, 0.368]
        assert np.round(func[2], decimals=3).tolist() == [0.018, 0.368, 1]

    def test_missing_file_raises_exception(self, states):
        func_spec = Specification.from_dict({'type': 'from file'})
        with pytest.raises(MissingFieldInSpecification):
            BivariateFunctionReader.create(func_spec, states)

    def test_unknown_file_raises_exception(self, states):
        func_spec = Specification.from_dict({'type': 'from file', 'file': 'some-non-existing-file.bat'})
        with pytest.raises(IOError):
            BivariateFunctionReader.create(func_spec, states)


class TestGameFactory(object):
    def test_create_basic_game_3_4_5(self):
        game_spec = Specification.from_dict({'type': 'basic',
                                             'states': {'elements': {'type': 'numbered labels', 'size': 3}},
                                             'messages': {'elements': {'type': 'numbered labels', 'size': 4}},
                                             'actions': {'elements': {'type': 'numbered labels', 'size': 5}}})
        game = GameFactory.create(game_spec)
        assert type(game) is Game
        assert hasattr(game, 'states')
        assert game.states.size() == 3
        assert hasattr(game, 'messages')
        assert game.messages.size() == 4
        assert hasattr(game, 'actions')
        assert game.actions.size() == 5
        assert hasattr(game, 'confusion')
        assert game.confusion is None

    def test_create_sim_max_game_3_5(self):
        game_spec = Specification.from_dict({'type': 'sim-max',
                                             'states': {'elements': {'type': 'numbered labels', 'size': 3}},
                                             'messages': {'elements': {'type': 'numbered labels', 'size': 5}}})
        game = GameFactory.create(game_spec)
        assert type(game) is SimMaxGame
        assert hasattr(game, 'states')
        assert game.states.size() == 3
        assert hasattr(game, 'messages')
        assert game.messages.size() == 5
        assert hasattr(game, 'actions')
        assert game.actions.size() == 3
        assert hasattr(game, 'confusion')
        assert game.confusion is None

    def test_create_sim_max_game_3_5_with_confusion(self):
        game_spec = Specification.from_dict({'type': 'sim-max',
                                             'states': {'type': 'metric space',
                                                        'elements': {'type': 'numeric interval', 'size': 3}},
                                             'messages': {'elements': {'type': 'numbered labels', 'size': 5}},
                                             'confusion': {'type': 'nosofsky'}})
        game = GameFactory.create(game_spec)
        assert type(game) is SimMaxGame
        assert hasattr(game, 'confusion')
        assert game.confusion.values.shape == (3, 3)

    def test_missing_type_defaults_to_basic(self):
        game_spec = Specification.from_dict({'states': {'elements': {'type': 'numbered labels', 'size': 3}},
                                             'messages': {'elements': {'type': 'numbered labels', 'size': 4}},
                                             'actions': {'elements': {'type': 'numbered labels', 'size': 5}}})
        game = GameFactory.create(game_spec)
        assert type(game) is Game

    def test_missing_states_raises_exception(self):
        game_spec = Specification.from_dict({'type': 'sim-max',
                                             'messages': {'elements': {'type': 'numbered labels', 'size': 5}}})
        with pytest.raises(MissingFieldInSpecification):
            GameFactory.create(game_spec)

    def test_missing_messages_raises_exception(self):
        game_spec = Specification.from_dict({'type': 'sim-max',
                                             'states': {'elements': {'type': 'numbered labels', 'size': 3}}})
        with pytest.raises(MissingFieldInSpecification):
            GameFactory.create(game_spec)

    def test_unknown_type_raises_exception(self):
        game_spec = Specification.from_dict({'type': '????????????',
                                             'states': {'elements': {'type': 'numbered labels', 'size': 3}},
                                             'messages': {'elements': {'type': 'numbered labels', 'size': 5}}})
        with pytest.raises(InvalidValueInSpecification):
            GameFactory.create(game_spec)


class TestDynamicsFactory(object):
    def test_types(self):
        dynamics_spec = Specification.from_dict({'type': 'replicator'})
        assert type(DynamicsFactory.create(dynamics_spec)) is ReplicatorDynamics

        dynamics_spec = Specification.from_dict({'type': 'best response'})
        assert type(DynamicsFactory.create(dynamics_spec)) is BestResponseDynamics

        dynamics_spec = Specification.from_dict({'type': 'quantal response', 'rationality': 10})
        assert type(DynamicsFactory.create(dynamics_spec)) is QuantalResponseDynamics

    def test_missing_type_defaults_to_replicator(self):
        dynamics_spec = Specification.empty()
        dynamics = DynamicsFactory.create(dynamics_spec)
        assert type(dynamics) is ReplicatorDynamics

    def test_unknown_type_raises_exception(self):
        dynamics_spec = Specification.from_dict({'type': '???????'})
        with pytest.raises(InvalidValueInSpecification):
            DynamicsFactory.create(dynamics_spec)

    def test_quantal_response_missing_rationality_raises_exception(self):
        dynamics_spec = Specification.from_dict({'type': 'quantal response'})
        with pytest.raises(MissingFieldInSpecification):
            DynamicsFactory.create(dynamics_spec)


class TestSimulationSpecReader(object):
    def test_read_from_file_sim_max_3_5_with_metrics(self, tmpdir):
        simulation_spec_yml = '''
            'game': 
                'type':
                    'sim-max'
                'states':
                    'elements': 
                        'type': 'numbered labels'
                        'size': 3
                'messages':
                    'elements': 
                        'type': 'numbered labels'
                        'size': 5
            'dynamics':
                'type': 'replicator'
            'metrics':
                - 'expected utility'
        '''
        spec_file = tmpdir.join("test_spec.yml")
        spec_file.write(simulation_spec_yml)
        simulation = SimulationSpecReader.read_from_file(str(spec_file))
        assert type(simulation.game) is SimMaxGame
        assert type(simulation.dynamics) is ReplicatorDynamics
        assert simulation.measurements_collector.number_of_metrics() == 1
        assert type(simulation.measurements_collector.metrics['expected utility']) is ExpectedUtilityMetric
        assert len(simulation.measurements_collector.measurements['expected utility']) == 1

    def test_read_sim_max_3_5_replicator_with_metrics(self):
        simulation_spec = Specification.from_dict({
            'game': {'type': 'sim-max',
                     'states': {'elements': {'type': 'numbered labels', 'size': 3}},
                     'messages': {'elements': {'type': 'numbered labels', 'size': 5}}},
            'dynamics': {'type': 'replicator'},
            'metrics': ['expected utility']})
        simulation = SimulationSpecReader.read(simulation_spec)
        assert type(simulation.game) is SimMaxGame
        assert type(simulation.dynamics) is ReplicatorDynamics
        assert simulation.measurements_collector.number_of_metrics() == 1
        assert type(simulation.measurements_collector.metrics['expected utility']) is ExpectedUtilityMetric
        assert len(simulation.measurements_collector.measurements['expected utility']) == 1

    def test_read_missing_game_throws_exception(self):
        simulation_spec = Specification.from_dict({'dynamics': {'type': 'replicator'}})
        with pytest.raises(MissingFieldInSpecification):
            SimulationSpecReader.read(simulation_spec)

    def test_read_missing_dynamics_throws_exception(self):
        simulation_spec = Specification.from_dict({
            'game': {'type': 'sim-max',
                     'states': {'elements': {'type': 'numbered labels', 'size': 3}},
                     'messages': {'elements': {'type': 'numbered labels', 'size': 5}}}})
        with pytest.raises(MissingFieldInSpecification):
            SimulationSpecReader.read(simulation_spec)

    def test_read_missing_metrics_defaults_to_none(self):
        simulation_spec = Specification.from_dict({
            'game': {'type': 'sim-max',
                     'states': {'elements': {'type': 'numbered labels', 'size': 3}},
                     'messages': {'elements': {'type': 'numbered labels', 'size': 5}}},
            'dynamics': {'type': 'replicator'}})
        simulation = SimulationSpecReader.read(simulation_spec)
        assert type(simulation.game) is SimMaxGame
        assert type(simulation.dynamics) is ReplicatorDynamics
        assert simulation.measurements_collector.number_of_metrics() == 0
