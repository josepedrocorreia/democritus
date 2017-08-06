from collections import OrderedDict

import pytest

from democritus.metrics import ExpectedUtilityMetric, SenderNormalizedEntropyMetric, ReceiverNormalizedEntropyMetric
from democritus.simulation import Simulation, SimulationMetricConverter, SimulationMeasurementsCollector
from democritus.types import SenderStrategy, ReceiverStrategy


class TestSimulationMetricConverter(object):
    def test_create_expected_utility(self):
        metric = SimulationMetricConverter.create('expected utility')
        assert type(metric) is ExpectedUtilityMetric

    def test_create_expected_utility_case_insensitive(self):
        metric = SimulationMetricConverter.create('eXpEcTeD UtIlItY')
        assert type(metric) is ExpectedUtilityMetric

    def test_create_sender_entropy(self):
        metric = SimulationMetricConverter.create('sender entropy')
        assert type(metric) is SenderNormalizedEntropyMetric

    def test_create_receiver_entropy(self):
        metric = SimulationMetricConverter.create('receiver entropy')
        assert type(metric) is ReceiverNormalizedEntropyMetric

    def test_create_unknown_metric_throws_exception(self):
        with pytest.raises(ValueError):
            SimulationMetricConverter.create('?????????????')


class TestSimulationMeasurementsCollector(object):
    def test_constructor_defaults(self):
        collector = SimulationMeasurementsCollector([])
        assert type(collector.metrics) is OrderedDict
        assert type(collector.measurements) is OrderedDict
        assert len(collector.metrics) == 0
        assert len(collector.measurements) == 0

    def test_constructor_with_two_metrics(self):
        collector = SimulationMeasurementsCollector([ExpectedUtilityMetric.name, SenderNormalizedEntropyMetric.name])
        assert type(collector.metrics) is OrderedDict
        assert type(collector.measurements) is OrderedDict
        assert len(collector.metrics) == 2
        assert collector.number_of_metrics() == 2
        assert len(collector.measurements) == 2
        assert type(collector.get_metric_class(ExpectedUtilityMetric.name)) is ExpectedUtilityMetric
        assert type(collector.get_metric_class(SenderNormalizedEntropyMetric.name)) is SenderNormalizedEntropyMetric
        assert collector.get_measurements(ExpectedUtilityMetric.name) == []
        assert collector.get_measurements(SenderNormalizedEntropyMetric.name) == []

    def test_calculate_all(self, converged_simulation):
        collector = SimulationMeasurementsCollector([ExpectedUtilityMetric.name, SenderNormalizedEntropyMetric.name])
        assert len(collector.get_measurements(ExpectedUtilityMetric.name)) == 0
        assert len(collector.get_measurements(SenderNormalizedEntropyMetric.name)) == 0
        collector.calculate_all(converged_simulation)
        assert len(collector.get_measurements(ExpectedUtilityMetric.name)) == 1
        assert len(collector.get_measurements(SenderNormalizedEntropyMetric.name)) == 1


class TestSimulation(object):
    def test_constructor_defaults(self, game, dynamics):
        simulation = Simulation(game, dynamics)
        assert simulation.current_step == 0
        assert len(simulation.sender_strategies) == 1
        assert len(simulation.receiver_strategies) == 1
        assert type(simulation.get_current_sender_strategy()) is SenderStrategy
        assert type(simulation.get_current_receiver_strategy()) is ReceiverStrategy
        assert type(simulation.measurements_collector) is SimulationMeasurementsCollector

    def test_constructor_strategy_parameters(self, game, dynamics):
        sender_strategy = SenderStrategy(game.states, game.messages, [[0, 1], [0.5, 0.5]])
        receiver_strategy = ReceiverStrategy(game.messages, game.actions, [[0.1, 0.9], [0.1, 0.9]])
        new_simulation = Simulation(game, dynamics, sender_strategy=sender_strategy,
                                    receiver_strategy=receiver_strategy)
        assert len(new_simulation.sender_strategies) == 1
        assert len(new_simulation.receiver_strategies) == 1
        assert type(new_simulation.get_current_sender_strategy()) is SenderStrategy
        assert type(new_simulation.get_current_receiver_strategy()) is ReceiverStrategy
        assert new_simulation.get_current_sender_strategy() == sender_strategy
        assert new_simulation.get_current_receiver_strategy() == receiver_strategy

    def test_step_generates_strategies_and_steps_forward(self, almost_converged_simulation_with_eu_metric):
        simulation = almost_converged_simulation_with_eu_metric
        initial_sender = simulation.get_current_sender_strategy()
        initial_receiver = simulation.get_current_receiver_strategy()
        simulation.step()
        assert simulation.current_step == 1
        assert len(simulation.sender_strategies) == 2
        assert len(simulation.receiver_strategies) == 2
        assert simulation.get_current_sender_strategy() != initial_sender
        assert simulation.get_current_receiver_strategy() != initial_receiver
        assert simulation.get_sender_strategy(0) == initial_sender
        assert simulation.get_receiver_strategy(0) == initial_receiver
        assert len(simulation.measurements_collector.measurements[ExpectedUtilityMetric.name.lower()]) == 2
        simulation.step()
        assert simulation.current_step == 2
        assert len(simulation.sender_strategies) == 3
        assert len(simulation.receiver_strategies) == 3
        assert len(simulation.measurements_collector.measurements[ExpectedUtilityMetric.name.lower()]) == 3

    def test_converged(self, almost_converged_simulation):
        simulation = almost_converged_simulation
        assert simulation.converged() is False
        simulation.step()
        # should have reached the stable point but has big enough change since previous
        assert simulation.converged() is False
        simulation.step()
        # should have stayed in the stable point and no change since previous
        assert simulation.converged() is True

    def test_run_until_converged(self, almost_converged_simulation):
        simulation = almost_converged_simulation
        assert simulation.converged() is False
        simulation.run_until_converged()
        # should have run twice until staying in the stable point
        assert simulation.converged() is True
        assert simulation.current_step == 2

    def test_run_until_converged_with_max_steps(self, game, dynamics):
        # flip-flopping strategies under best response
        sender_strategy = SenderStrategy(game.states, game.messages, [[1, 0], [0, 1]])
        receiver_strategy = ReceiverStrategy(game.messages, game.actions, [[0, 1], [1, 0]])
        simulation = Simulation(game, dynamics, sender_strategy=sender_strategy, receiver_strategy=receiver_strategy)
        simulation.run_until_converged(max_steps=50)
        assert simulation.converged() is False
        assert simulation.current_step == 50

    # want to double-check to make sure there are no infinite loops
    def test_run_until_converged_with_none_max_steps_throws_exception(self, almost_converged_simulation):
        simulation = almost_converged_simulation
        assert simulation.converged() is False
        with pytest.raises(Exception):
            simulation.run_until_converged(max_steps=None)
