import numpy as np
import pytest

from democritus.converters import StatesFactory, GameFactory, DynamicsFactory
from democritus.games import SimMaxGame
from democritus.metrics import ExpectedUtilityMetric
from democritus.simulation import Simulation
from democritus.specification import Specification
from democritus.types import StateSet, MessageSet, SenderStrategy, ReceiverStrategy


@pytest.fixture(name='states')
def fixture_states():
    states_spec = Specification.from_dict({'type': 'metric space', 'elements': {'type': 'numeric range', 'size': 3}})
    return StatesFactory.create(states_spec)


@pytest.fixture(name='sim_max_game')
def fixture_sim_max_game():
    states = StateSet(['t1', 't2'], [0.6, 0.4])
    messages = MessageSet(['m1', 'm2'])
    similarity = np.array([[2, 0.5], [0.1, 1]])
    utility = similarity
    return SimMaxGame(states, messages, utility, similarity, False)


@pytest.fixture(name='game')
def fixture_game():
    sim_max_2x2_spec = Specification.from_dict({'type': 'sim-max',
                                                'states': {'elements': {'type': 'numbered labels', 'size': 2}},
                                                'messages': {'elements': {'type': 'numbered labels', 'size': 2}}})
    sim_max_2x2 = GameFactory.create(sim_max_2x2_spec)
    return sim_max_2x2


@pytest.fixture(name='dynamics')
def fixture_dynamics():
    replicator = DynamicsFactory.create(Specification.from_dict({'type': 'best response'}))
    return replicator


@pytest.fixture(name='converged_simulation')
def fixture_converged_simulation(game, dynamics):
    sender_strategy = SenderStrategy(game.states, game.messages, [[1, 0], [0, 1]])
    receiver_strategy = ReceiverStrategy(game.messages, game.actions, [[1, 0], [0, 1]])
    return Simulation(game, dynamics, sender_strategy=sender_strategy, receiver_strategy=receiver_strategy)


@pytest.fixture(name='almost_converged_simulation')
def fixture_almost_converged_simulation(game, dynamics):
    sender_strategy = SenderStrategy(game.states, game.messages, [[0.9, 0.1], [0.05, 0.95]])
    receiver_strategy = ReceiverStrategy(game.messages, game.actions, [[0.95, 0.05], [0.13, 0.87]])
    return Simulation(game, dynamics, sender_strategy=sender_strategy, receiver_strategy=receiver_strategy)


@pytest.fixture(name='almost_converged_simulation_with_eu_metric')
def fixture_almost_converged_simulation_with_eu_metric(game, dynamics):
    sender_strategy = SenderStrategy(game.states, game.messages, [[0.9, 0.1], [0.05, 0.95]])
    receiver_strategy = ReceiverStrategy(game.messages, game.actions, [[0.95, 0.05], [0.13, 0.87]])
    simulation_metrics = [ExpectedUtilityMetric()]
    return Simulation(game, dynamics, simulation_metrics=simulation_metrics,
                      sender_strategy=sender_strategy, receiver_strategy=receiver_strategy)
