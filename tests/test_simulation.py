import numpy as np
import pytest

from democritus.simulation import Simulation


class TestSimulation(object):
    def test_constructor_defaults(self, game, dynamics):
        simulation = Simulation(game, dynamics)
        assert simulation.current_step == 0
        assert len(simulation.sender_strategies) == 1
        assert len(simulation.receiver_strategies) == 1
        assert type(simulation.get_current_sender_strategy()) is np.ndarray
        assert type(simulation.get_current_receiver_strategy()) is np.ndarray
        assert len(simulation.simulation_measurements) == 0

    def test_constructor_strategy_parameters(self, game, dynamics):
        sender_strategy = [[0, 1], [0.5, 0.5]]
        receiver_strategy = [[0.1, 0.9], [0.1, 0.9]]
        new_simulation = Simulation(game, dynamics, sender_strategy=sender_strategy,
                                    receiver_strategy=receiver_strategy)
        assert len(new_simulation.sender_strategies) == 1
        assert len(new_simulation.receiver_strategies) == 1
        assert type(new_simulation.get_current_sender_strategy()) is np.ndarray
        assert type(new_simulation.get_current_receiver_strategy()) is np.ndarray
        assert new_simulation.get_current_sender_strategy().tolist() == sender_strategy
        assert new_simulation.get_current_receiver_strategy().tolist() == receiver_strategy

    def test_step_generates_strategies_and_steps_forward(self, almost_converged_simulation_with_eu_metric):
        simulation = almost_converged_simulation_with_eu_metric
        initial_sender = simulation.get_current_sender_strategy()
        initial_receiver = simulation.get_current_receiver_strategy()
        simulation.step()
        assert simulation.current_step == 1
        assert len(simulation.sender_strategies) == 2
        assert len(simulation.receiver_strategies) == 2
        assert simulation.get_current_sender_strategy().tolist() != initial_sender.tolist()
        assert simulation.get_current_receiver_strategy().tolist() != initial_receiver.tolist()
        assert simulation.get_sender_strategy(0).tolist() == initial_sender.tolist()
        assert simulation.get_receiver_strategy(0).tolist() == initial_receiver.tolist()
        assert len(simulation.simulation_measurements[0][1]) == 2
        simulation.step()
        assert simulation.current_step == 2
        assert len(simulation.sender_strategies) == 3
        assert len(simulation.receiver_strategies) == 3
        assert len(simulation.simulation_measurements[0][1]) == 3

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
        sender_strategy = [[1, 0], [0, 1]]
        receiver_strategy = [[0, 1], [1, 0]]
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
