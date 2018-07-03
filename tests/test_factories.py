import numpy as np

from democritus.factories import BivariateFunctionFactory, SenderStrategyFactory, ReceiverStrategyFactory
from democritus.types import WCSMunsellSenderStrategy, SenderStrategy, ReceiverStrategy, WCSMunsellReceiverStrategy


class TestBivariateFunctionFactory(object):
    def test_create_identity(self):
        similarity = BivariateFunctionFactory.create_identity(3)
        assert np.round(similarity[0], decimals=3).tolist() == [1, 0, 0]
        assert np.round(similarity[1], decimals=3).tolist() == [0, 1, 0]
        assert np.round(similarity[2], decimals=3).tolist() == [0, 0, 1]

    def test_create_nosofsky(self):
        similarity = BivariateFunctionFactory.create_nosofsky(np.array([[0, 1, 2], [1, 0, 1], [2, 1, 0]]), 2)
        assert np.round(similarity[0], decimals=3).tolist() == [1, 0.779, 0.368]
        assert np.round(similarity[1], decimals=3).tolist() == [0.779, 1, 0.779]
        assert np.round(similarity[2], decimals=3).tolist() == [0.368, 0.779, 1]


class TestSenderStrategyFactory(object):
    def test_create_random(self, states, messages):
        sender_strategy = SenderStrategyFactory.create_random(states, messages)
        assert type(sender_strategy) is SenderStrategy

    def test_create_random_wcs_munsell(self, wcs_munsell_palette, messages):
        sender_strategy = SenderStrategyFactory.create_random(wcs_munsell_palette, messages)
        assert type(sender_strategy) is WCSMunsellSenderStrategy

    def test_create_zeros(self, states, messages):
        sender_strategy = SenderStrategyFactory.create_random(states, messages)
        assert type(sender_strategy) is SenderStrategy

    def test_create_zeros_wcs_munsell(self, wcs_munsell_palette, messages):
        sender_strategy = SenderStrategyFactory.create_random(wcs_munsell_palette, messages)
        assert type(sender_strategy) is WCSMunsellSenderStrategy


class TestReceiverStrategyFactory(object):
    def test_create_random(self, states, messages):
        receiver_strategy = ReceiverStrategyFactory.create_random(messages, states)
        assert type(receiver_strategy) is ReceiverStrategy

    def test_create_random_wcs_munsell(self, wcs_munsell_palette, messages):
        receiver_strategy = ReceiverStrategyFactory.create_random(messages, wcs_munsell_palette)
        assert type(receiver_strategy) is WCSMunsellReceiverStrategy

    def test_create_zeros(self, states, messages):
        receiver_strategy = ReceiverStrategyFactory.create_random(messages, states)
        assert type(receiver_strategy) is ReceiverStrategy

    def test_create_zeros_wcs_munsell(self, wcs_munsell_palette, messages):
        receiver_strategy = ReceiverStrategyFactory.create_random(messages, wcs_munsell_palette)
        assert type(receiver_strategy) is WCSMunsellReceiverStrategy
