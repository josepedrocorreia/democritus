import pytest

from democritus.metrics import SimulationMetric, SenderNormalizedEntropyMetric, \
    ReceiverNormalizedEntropyMetric, ExpectedUtilityMetric


class TestSimulationMetric(object):
    def test_calculate_raises_exception(self, converged_simulation):
        simulation = converged_simulation
        metric = SimulationMetric()
        with pytest.raises(NotImplementedError):
            metric.calculate(simulation)

    def test_plot_raises_exception(self, converged_simulation):
        metric = SimulationMetric()
        with pytest.raises(NotImplementedError):
            metric.plot([], None)


class TestExpectedUtilityMetric(object):
    def test_calculate(self, almost_converged_simulation):
        simulation = almost_converged_simulation
        metric = ExpectedUtilityMetric()
        expected_utility = metric.calculate(simulation)
        assert expected_utility == pytest.approx(0.849, abs=5e-4)


class TestSenderNormalizedEntropyMetric(object):
    def test_calculate(self, almost_converged_simulation):
        simulation = almost_converged_simulation
        metric = SenderNormalizedEntropyMetric()
        sender_entropy = metric.calculate(simulation)
        assert sender_entropy == pytest.approx(0.378, abs=5e-4)


class TestReceiverNormalizedEntropyMetric(object):
    def test_calculate(self, almost_converged_simulation):
        simulation = almost_converged_simulation
        metric = ReceiverNormalizedEntropyMetric()
        receiver_entropy = metric.calculate(simulation)
        assert receiver_entropy == pytest.approx(0.422, abs=5e-4)
