import pytest

from democritus.dynamics import *
from democritus.exceptions import MissingFieldInSpecification
from democritus.game import SimMaxGame
from democritus.messages import MessageSet
from democritus.states import *


# Dynamics

def test_dynamics_update_sender():
    dynamics = Dynamics()
    with pytest.raises(NotImplementedError):
        dynamics.update_sender(None, None, None)


def test_dynamics_update_receiver():
    dynamics = Dynamics()
    with pytest.raises(NotImplementedError):
        dynamics.update_receiver(None, None, None)


# DynamicsFactory

def test_dynamics_factory_types():
    dynamics_spec = Specification.from_dict({'type': 'replicator'})
    assert type(DynamicsFactory.create(dynamics_spec)) is ReplicatorDynamics

    dynamics_spec = Specification.from_dict({'type': 'best response'})
    assert type(DynamicsFactory.create(dynamics_spec)) is BestResponseDynamics

    dynamics_spec = Specification.from_dict({'type': 'quantal response', 'rationality': 10})
    assert type(DynamicsFactory.create(dynamics_spec)) is QuantalResponseDynamics


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


# ReplicatorDynamics

@pytest.fixture(name='game')
def fixture_game():
    states = StateSet(['t1', 't2'], [0.6, 0.4])
    messages = MessageSet(['m1', 'm2'])
    similarity = [[2, 0.5], [0.1, 1]]
    utility = similarity
    return SimMaxGame(states, messages, utility, similarity, False)


def test_replicator_dynamics_update_sender(game):
    dynamics = ReplicatorDynamics()
    sender_strategy = np.array([[0.3, 0.7], [0.4, 0.6]])
    receiver_strategy = np.array([[0.2, 0.8], [0.9, 0.1]])
    new_sender_strategy = dynamics.update_sender(sender_strategy, receiver_strategy, game)
    assert np.round(new_sender_strategy, decimals=3).tolist() == [[0.156, 0.844], [0.742, 0.258]]


def test_replicator_dynamics_update_receiver(game):
    dynamics = ReplicatorDynamics()
    sender_strategy = np.array([[0.3, 0.7], [0.4, 0.6]])
    receiver_strategy = np.array([[0.2, 0.8], [0.9, 0.1]])
    new_receiver_strategy = dynamics.update_receiver(sender_strategy, receiver_strategy, game)
    assert np.round(new_receiver_strategy, decimals=3).tolist() == [[0.382, 0.618], [0.968, 0.032]]


def test_replicator_dynamics_update_sender_with_imprecision(game):
    game.imprecise = True
    dynamics = ReplicatorDynamics()
    sender_strategy = np.array([[0.3, 0.7], [0.4, 0.6]])
    receiver_strategy = np.array([[0.2, 0.8], [0.9, 0.1]])
    new_sender_strategy = dynamics.update_sender(sender_strategy, receiver_strategy, game)
    assert np.round(new_sender_strategy, decimals=3).tolist() == [[0.273, 0.727], [0.689, 0.311]]


def test_replicator_dynamics_update_receiver_with_imprecision(game):
    game.imprecise = True
    dynamics = ReplicatorDynamics()
    sender_strategy = np.array([[0.3, 0.7], [0.4, 0.6]])
    receiver_strategy = np.array([[0.2, 0.8], [0.9, 0.1]])
    new_receiver_strategy = dynamics.update_receiver(sender_strategy, receiver_strategy, game)
    assert np.round(new_receiver_strategy, decimals=3).tolist() == [[0.620, 0.380], [0.938, 0.062]]


# BestResponseDynamics

def test_best_response_dynamics_update_sender(game):
    dynamics = BestResponseDynamics()
    sender_strategy = np.array([[0.3, 0.7], [0.4, 0.6]])
    receiver_strategy = np.array([[0.2, 0.8], [0.9, 0.1]])
    new_sender_strategy = dynamics.update_sender(sender_strategy, receiver_strategy, game)
    assert np.round(new_sender_strategy, decimals=3).tolist() == [[0, 1], [1, 0]]


def test_best_response_dynamics_update_receiver(game):
    dynamics = BestResponseDynamics()
    sender_strategy = np.array([[0.3, 0.7], [0.4, 0.6]])
    receiver_strategy = np.array([[0.2, 0.8], [0.9, 0.1]])
    new_receiver_strategy = dynamics.update_receiver(sender_strategy, receiver_strategy, game)
    assert np.round(new_receiver_strategy, decimals=3).tolist() == [[1, 0], [1, 0]]


def test_best_response_dynamics_update_sender_with_imprecision(game):
    game.imprecise = True
    dynamics = BestResponseDynamics()
    sender_strategy = np.array([[0.3, 0.7], [0.4, 0.6]])
    receiver_strategy = np.array([[0.2, 0.8], [0.9, 0.1]])
    new_sender_strategy = dynamics.update_sender(sender_strategy, receiver_strategy, game)
    assert np.round(new_sender_strategy, decimals=3).tolist() == [[0.2, 0.8], [0.909, 0.091]]


def test_best_response_dynamics_update_receiver_with_imprecision(game):
    game.imprecise = True
    dynamics = BestResponseDynamics()
    sender_strategy = np.array([[0.3, 0.7], [0.4, 0.6]])
    receiver_strategy = np.array([[0.2, 0.8], [0.9, 0.1]])
    new_receiver_strategy = dynamics.update_receiver(sender_strategy, receiver_strategy, game)
    assert np.round(new_receiver_strategy, decimals=3).tolist() == [[0.952, 0.048], [0.952, 0.048]]


# QuantalResponseDynamics

def test_quantal_response_dynamics_update_sender(game):
    dynamics = QuantalResponseDynamics(5)
    sender_strategy = np.array([[0.3, 0.7], [0.4, 0.6]])
    receiver_strategy = np.array([[0.2, 0.8], [0.9, 0.1]])
    new_sender_strategy = dynamics.update_sender(sender_strategy, receiver_strategy, game)
    assert np.round(new_sender_strategy, decimals=3).tolist() == [[0.005, 0.995], [0.959, 0.041]]


def test_quantal_response_dynamics_update_receiver(game):
    dynamics = QuantalResponseDynamics(5)
    sender_strategy = np.array([[0.3, 0.7], [0.4, 0.6]])
    receiver_strategy = np.array([[0.2, 0.8], [0.9, 0.1]])
    new_receiver_strategy = dynamics.update_receiver(sender_strategy, receiver_strategy, game)
    assert np.round(new_receiver_strategy, decimals=3).tolist() == [[0.788, 0.212], [0.967, 0.033]]


def test_quantal_response_dynamics_update_sender_with_imprecision(game):
    game.imprecise = True
    dynamics = QuantalResponseDynamics(5)
    sender_strategy = np.array([[0.3, 0.7], [0.4, 0.6]])
    receiver_strategy = np.array([[0.2, 0.8], [0.9, 0.1]])
    new_sender_strategy = dynamics.update_sender(sender_strategy, receiver_strategy, game)
    assert np.round(new_sender_strategy, decimals=3).tolist() == [[0.196, 0.804], [0.872, 0.128]]


def test_quantal_response_dynamics_update_receiver_with_imprecision(game):
    game.imprecise = True
    dynamics = QuantalResponseDynamics(5)
    sender_strategy = np.array([[0.3, 0.7], [0.4, 0.6]])
    receiver_strategy = np.array([[0.2, 0.8], [0.9, 0.1]])
    new_receiver_strategy = dynamics.update_receiver(sender_strategy, receiver_strategy, game)
    assert np.round(new_receiver_strategy, decimals=3).tolist() == [[0.852, 0.148], [0.938, 0.062]]
