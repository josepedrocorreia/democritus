import pytest
from fixtures import *

from democritus.simulation_metrics import *


def test_calculate_parent_class_raises_exception(converged_simulation):
    simulation = converged_simulation
    metric = SimulationMetric()
    with pytest.raises(NotImplementedError):
        metric.calculate(simulation)


def test_expected_utility_calculation(almost_converged_simulation):
    simulation = almost_converged_simulation
    metric = ExpectedUtilityMetric()
    expected_utility = metric.calculate(simulation)
    assert expected_utility == pytest.approx(0.849, abs=5e-4)


def test_sender_entropy_calculation(almost_converged_simulation):
    simulation = almost_converged_simulation
    metric = SenderNormalizedEntropyMetric()
    sender_entropy = metric.calculate(simulation)
    assert sender_entropy == pytest.approx(0.378, abs=5e-4)


def test_receiver_entropy_calculation(almost_converged_simulation):
    simulation = almost_converged_simulation
    metric = ReceiverNormalizedEntropyMetric()
    receiver_entropy = metric.calculate(simulation)
    assert receiver_entropy == pytest.approx(0.422, abs=5e-4)


def test_simulation_metrics_create_expected_utility():
    metric = SimulationMetrics.create('expected utility')
    assert type(metric) is ExpectedUtilityMetric


def test_simulation_metrics_create_expected_utility_case_insensitive():
    metric = SimulationMetrics.create('eXpEcTeD UtIlItY')
    assert type(metric) is ExpectedUtilityMetric


def test_simulation_metrics_create_sender_entropy():
    metric = SimulationMetrics.create('sender entropy')
    assert type(metric) is SenderNormalizedEntropyMetric


def test_simulation_metrics_create_receiver_entropy():
    metric = SimulationMetrics.create('receiver entropy')
    assert type(metric) is ReceiverNormalizedEntropyMetric


def test_simulation_metrics_create_unknown_metric_throws_exception():
    with pytest.raises(ValueError):
        SimulationMetrics.create('?????????????')
