import pytest
from fixtures import *

from democritus.metrics import *


# SimulationMetric
def test_calculate_parent_class_raises_exception(converged_simulation):
    simulation = converged_simulation
    metric = SimulationMetric()
    with pytest.raises(NotImplementedError):
        metric.calculate(simulation)


# ExpectedUtilityMetric
def test_expected_utility_calculation(almost_converged_simulation):
    simulation = almost_converged_simulation
    metric = ExpectedUtilityMetric()
    expected_utility = metric.calculate(simulation)
    assert expected_utility == pytest.approx(0.849, abs=5e-4)


# SenderNormalizedEntropyMetric
def test_sender_entropy_calculation(almost_converged_simulation):
    simulation = almost_converged_simulation
    metric = SenderNormalizedEntropyMetric()
    sender_entropy = metric.calculate(simulation)
    assert sender_entropy == pytest.approx(0.378, abs=5e-4)


# ReceiverNormalizedEntropyMetric
def test_receiver_entropy_calculation(almost_converged_simulation):
    simulation = almost_converged_simulation
    metric = ReceiverNormalizedEntropyMetric()
    receiver_entropy = metric.calculate(simulation)
    assert receiver_entropy == pytest.approx(0.422, abs=5e-4)
