import pytest

from democritus.dynamics import DynamicsFactory
from democritus.game import GameFactory
from democritus.simulation import Simulation
from democritus.simulation_metrics import ExpectedUtilityMetric
from democritus.specification import Specification


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


@pytest.fixture(name='converged_simulation')
def fixture_converged_simulation(game, dynamics):
    sender_strategy = [[1, 0], [0, 1]]
    receiver_strategy = [[1, 0], [0, 1]]
    return Simulation(game, dynamics, sender_strategy=sender_strategy, receiver_strategy=receiver_strategy)


@pytest.fixture(name='almost_converged_simulation')
def fixture_almost_converged_simulation(game, dynamics):
    sender_strategy = [[0.9, 0.1], [0.05, 0.95]]
    receiver_strategy = [[0.95, 0.05], [0.13, 0.87]]
    return Simulation(game, dynamics, sender_strategy=sender_strategy, receiver_strategy=receiver_strategy)


@pytest.fixture(name='almost_converged_simulation_with_eu_metric')
def fixture_almost_converged_simulation_with_eu_metric(game, dynamics):
    sender_strategy = [[0.9, 0.1], [0.05, 0.95]]
    receiver_strategy = [[0.95, 0.05], [0.13, 0.87]]
    simulation_metrics = [ExpectedUtilityMetric()]
    return Simulation(game, dynamics, simulation_metrics=simulation_metrics,
                      sender_strategy=sender_strategy, receiver_strategy=receiver_strategy)
