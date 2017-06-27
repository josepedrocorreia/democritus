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
    dynamics_spec = Specification.from_dict({})
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

states = StateSet(['t1', 't2'], [0.6, 0.4])
messages = MessageSet(['m1', 'm2'])
similarity = [[2, 0], [0, 1]]
utility = similarity
game = SimMaxGame(states, messages, utility, similarity)


def test_replicator_dynamics_update_sender():
    dynamics = ReplicatorDynamics()
    sender_strategy = np.array([[0.3, 0.7], [0.4, 0.6]])
    receiver_strategy = np.array([[0.2, 0.8], [0.9, 0.1]])
    new_sender_strategy = dynamics.update_sender(sender_strategy, receiver_strategy, game)
    assert np.round(new_sender_strategy, decimals=3).tolist() == [[0.087, 0.913], [0.842, 0.158]]


def test_replicator_dynamics_update_receiver():
    dynamics = ReplicatorDynamics()
    sender_strategy = np.array([[0.3, 0.7], [0.4, 0.6]])
    receiver_strategy = np.array([[0.2, 0.8], [0.9, 0.1]])
    new_receiver_strategy = dynamics.update_receiver(sender_strategy, receiver_strategy, game)
    assert np.round(new_receiver_strategy, decimals=3).tolist() == [[0.36, 0.64], [0.969, 0.031]]


# BestResponseDynamics

def test_best_response_dynamics_update_sender():
    dynamics = BestResponseDynamics()
    sender_strategy = np.array([[0.3, 0.7], [0.4, 0.6]])
    receiver_strategy = np.array([[0.2, 0.8], [0.9, 0.1]])
    new_sender_strategy = dynamics.update_sender(sender_strategy, receiver_strategy, game)
    assert np.round(new_sender_strategy, decimals=3).tolist() == [[0, 1], [1, 0]]


def test_best_response_dynamics_update_receiver():
    dynamics = BestResponseDynamics()
    sender_strategy = np.array([[0.3, 0.7], [0.4, 0.6]])
    receiver_strategy = np.array([[0.2, 0.8], [0.9, 0.1]])
    new_receiver_strategy = dynamics.update_receiver(sender_strategy, receiver_strategy, game)
    assert np.round(new_receiver_strategy, decimals=3).tolist() == [[1, 0], [1, 0]]


# QuantalResponseDynamics

def test_quantal_response_dynamics_update_sender():
    dynamics = QuantalResponseDynamics(5)
    sender_strategy = np.array([[0.3, 0.7], [0.4, 0.6]])
    receiver_strategy = np.array([[0.2, 0.8], [0.9, 0.1]])
    new_sender_strategy = dynamics.update_sender(sender_strategy, receiver_strategy, game)
    assert np.round(new_sender_strategy, decimals=3).tolist() == [[0.001, 0.999], [0.971, 0.029]]


def test_quantal_response_dynamics_update_receiver():
    dynamics = QuantalResponseDynamics(5)
    sender_strategy = np.array([[0.3, 0.7], [0.4, 0.6]])
    receiver_strategy = np.array([[0.2, 0.8], [0.9, 0.1]])
    new_receiver_strategy = dynamics.update_receiver(sender_strategy, receiver_strategy, game)
    assert np.round(new_receiver_strategy, decimals=3).tolist() == [[0.731, 0.269], [0.953, 0.047]]
