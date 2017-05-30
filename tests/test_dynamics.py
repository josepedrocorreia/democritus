import pytest

from democritus.dynamics import *

# Dynamics
from democritus.messages import MessageSet
from democritus.states import *


def test_dynamics_update_sender():
    dynamics = Dynamics()
    with pytest.raises(NotImplementedError):
        dynamics.update_sender(None, None, None, None, None)


def test_dynamics_update_receiver():
    dynamics = Dynamics()
    with pytest.raises(NotImplementedError):
        dynamics.update_receiver(None, None, None, None, None)


# DynamicsFactory

def test_dynamics_factory_types():
    assert type(DynamicsFactory.create({'type': 'replicator'})) is ReplicatorDynamics
    assert type(DynamicsFactory.create({'type': 'best response'})) is BestResponseDynamics
    assert type(DynamicsFactory.create({'type': 'quantal response', 'rationality': 10})) is QuantalResponseDynamics


def test_dynamics_factory_missing_type_defaults_to_replicator():
    dynamics = DynamicsFactory.create({})
    assert type(dynamics) is ReplicatorDynamics


def test_dynamics_factory_unknown_type_raises_exception():
    with pytest.raises(ValueError):
        DynamicsFactory.create({'type': '???????'})


def test_dynamics_factory_quantal_response_missing_rationality_raises_exception():
    with pytest.raises(ValueError):
        DynamicsFactory.create({'type': 'quantal response'})


# ReplicatorDynamics

def test_replicator_dynamics_update_sender():
    dynamics = ReplicatorDynamics()
    states = StateSet(['t1', 't2'], [0.6, 0.4])
    messages = MessageSet(['m1', 'm2'])
    utility = [[2, 0], [0, 1]]
    sender_strategy = np.array([[0.3, 0.7], [0.4, 0.6]])
    receiver_strategy = np.array([[0.2, 0.8], [0.9, 0.1]])
    new_sender_strategy = dynamics.update_sender(sender_strategy, receiver_strategy, states, messages, utility)
    assert np.round(new_sender_strategy, decimals=3).tolist() == [[0.087, 0.913], [0.842, 0.158]]


def test_replicator_dynamics_update_receiver():
    dynamics = ReplicatorDynamics()
    states = StateSet(['t1', 't2'], [0.6, 0.4])
    messages = MessageSet(['m1', 'm2'])
    utility = [[2, 0], [0, 1]]
    sender_strategy = np.array([[0.3, 0.7], [0.4, 0.6]])
    receiver_strategy = np.array([[0.2, 0.8], [0.9, 0.1]])
    new_receiver_strategy = dynamics.update_receiver(sender_strategy, receiver_strategy, states, messages, utility)
    assert np.round(new_receiver_strategy, decimals=3).tolist() == [[0.36, 0.64], [0.969, 0.031]]


# BestResponseDynamics

def test_best_response_dynamics_update_sender():
    dynamics = BestResponseDynamics()
    states = StateSet(['t1', 't2'], [0.6, 0.4])
    messages = MessageSet(['m1', 'm2'])
    utility = [[2, 0], [0, 1]]
    sender_strategy = np.array([[0.3, 0.7], [0.4, 0.6]])
    receiver_strategy = np.array([[0.2, 0.8], [0.9, 0.1]])
    new_sender_strategy = dynamics.update_sender(sender_strategy, receiver_strategy, states, messages, utility)
    assert np.round(new_sender_strategy, decimals=3).tolist() == [[0, 1], [1, 0]]


def test_best_response_dynamics_update_receiver():
    dynamics = BestResponseDynamics()
    states = StateSet(['t1', 't2'], [0.6, 0.4])
    messages = MessageSet(['m1', 'm2'])
    utility = [[2, 0], [0, 1]]
    sender_strategy = np.array([[0.3, 0.7], [0.4, 0.6]])
    receiver_strategy = np.array([[0.2, 0.8], [0.9, 0.1]])
    new_receiver_strategy = dynamics.update_receiver(sender_strategy, receiver_strategy, states, messages, utility)
    assert np.round(new_receiver_strategy, decimals=3).tolist() == [[1, 0], [1, 0]]
