import pytest

from democritus.dynamics import *


# Dynamics

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
