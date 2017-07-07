import pytest

from democritus.dynamics import ReplicatorDynamics
from democritus.exceptions import MissingFieldInSpecification
from democritus.game import SimMaxGame
from democritus.simulation import *


# Simulation

@pytest.fixture(name='game')
def fixture_game():
    sim_max_2x2_spec = Specification.from_dict({'type': 'sim-max',
                                                'states': {'elements': {'type': 'numbered', 'size': 2}},
                                                'messages': {'elements': {'type': 'numbered', 'size': 2}}})
    sim_max_2x2 = GameFactory.create(sim_max_2x2_spec)
    return sim_max_2x2


@pytest.fixture(name='dynamics')
def fixture_dynamics():
    replicator = DynamicsFactory.create(Specification.from_dict({'type': 'best response'}))
    return replicator


def test_constructor_defaults(game, dynamics):
    simulation = Simulation(game, dynamics)
    assert simulation.current_step == 0
    assert len(simulation.sender_strategies) == 1
    assert len(simulation.receiver_strategies) == 1
    assert type(simulation.get_current_sender_strategy()) is np.ndarray
    assert type(simulation.get_current_receiver_strategy()) is np.ndarray


def test_constructor_strategy_parameters(game, dynamics):
    sender_strategy = [[0, 1], [0.5, 0.5]]
    receiver_strategy = [[0.1, 0.9], [0.1, 0.9]]
    new_simulation = Simulation(game, dynamics, sender_strategy, receiver_strategy)
    assert len(new_simulation.sender_strategies) == 1
    assert len(new_simulation.receiver_strategies) == 1
    assert type(new_simulation.get_current_sender_strategy()) is np.ndarray
    assert type(new_simulation.get_current_receiver_strategy()) is np.ndarray
    assert new_simulation.get_current_sender_strategy().tolist() == sender_strategy
    assert new_simulation.get_current_receiver_strategy().tolist() == receiver_strategy


@pytest.fixture(name='converged_simulation')
def fixture_converged_simulation(game, dynamics):
    sender_strategy = [[1, 0], [0, 1]]
    receiver_strategy = [[1, 0], [0, 1]]
    return Simulation(game, dynamics, sender_strategy, receiver_strategy)


@pytest.fixture(name='almost_converged_simulation')
def fixture_almost_converged_simulation(game, dynamics):
    sender_strategy = [[0.9, 0.1], [0.05, 0.95]]
    receiver_strategy = [[0.95, 0.05], [0.1, 0.9]]
    return Simulation(game, dynamics, sender_strategy, receiver_strategy)


def test_step_generates_strategies_and_steps_forward(almost_converged_simulation):
    simulation = almost_converged_simulation
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
    simulation.step()
    assert simulation.current_step == 2
    assert len(simulation.sender_strategies) == 3
    assert len(simulation.receiver_strategies) == 3


def test_converged(almost_converged_simulation):
    simulation = almost_converged_simulation
    assert simulation.converged() is False
    simulation.step()
    # should have reached the stable point but has big enough change since previous
    assert simulation.converged() is False
    simulation.step()
    # should have stayed in the stable point and no change since previous
    assert simulation.converged() is True


def test_run_until_converged(almost_converged_simulation):
    simulation = almost_converged_simulation
    assert simulation.converged() is False
    simulation.run_until_converged()
    # should have run twice until staying in the stable point
    assert simulation.converged() is True
    assert simulation.current_step == 2


def test_run_until_converged_with_max_steps(game, dynamics):
    # flip-flopping strategies under best response
    sender_strategy = [[1, 0], [0, 1]]
    receiver_strategy = [[0, 1], [1, 0]]
    simulation = Simulation(game, dynamics, sender_strategy, receiver_strategy)
    simulation.run_until_converged(max_steps=50)
    assert simulation.converged() is False
    assert simulation.current_step == 50


# want to double-check to make sure there are no infinite loops
def test_run_until_converged_with_none_max_steps_throws_exception(almost_converged_simulation):
    simulation = almost_converged_simulation
    assert simulation.converged() is False
    with pytest.raises(Exception):
        simulation.run_until_converged(max_steps=None)


# SimulationSpecReader

def test_read_sim_max_3_5_replicator():
    simulation_spec = Specification.from_dict({'game': {'type': 'sim-max',
                                                        'states': {'elements': {'type': 'numbered', 'size': 3}},
                                                        'messages': {'elements': {'type': 'numbered', 'size': 5}}},
                                               'dynamics': {'type': 'replicator'}})
    simulation = SimulationSpecReader.read(simulation_spec)
    assert type(simulation.game) is SimMaxGame
    assert type(simulation.dynamics) is ReplicatorDynamics


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

#
