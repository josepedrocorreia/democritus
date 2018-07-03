from __future__ import division

import numpy as np

from democritus import utils
from democritus.types import BivariateFunction, SenderStrategy, ReceiverStrategy, WCSMunsellPalette, \
    WCSMunsellSenderStrategy, WCSMunsellReceiverStrategy


class BivariateFunctionFactory(object):
    @staticmethod
    def create_identity(size):
        return BivariateFunction(np.identity(size))

    @staticmethod
    def create_nosofsky(distances, decay):
        return BivariateFunction(np.exp(-(distances ** 2) / (decay ** 2)))

    @staticmethod
    def read_from_file(file_name):
        return BivariateFunction(np.loadtxt(file_name, delimiter=','))


class SenderStrategyFactory(object):
    @staticmethod
    def create_random(states, messages):
        values = utils.make_row_stochastic(np.random.random((states.size(), messages.size())))
        if isinstance(states, WCSMunsellPalette):
            sender_strategy = WCSMunsellSenderStrategy(states, messages, values)
        else:
            sender_strategy = SenderStrategy(states, messages, values)
        return sender_strategy

    @staticmethod
    def create_zeros(states, messages):
        values = np.zeros((states.size(), messages.size()))
        if isinstance(states, WCSMunsellPalette):
            sender_strategy = WCSMunsellSenderStrategy(states, messages, values)
        else:
            sender_strategy = SenderStrategy(states, messages, values)
        return sender_strategy


class ReceiverStrategyFactory(object):
    @staticmethod
    def create_random(messages, actions):
        values = utils.make_row_stochastic(np.random.random((messages.size(), actions.size())))
        if isinstance(actions, WCSMunsellPalette):
            receiver_strategy = WCSMunsellReceiverStrategy(messages, actions, values)
        else:
            receiver_strategy = ReceiverStrategy(messages, actions, values)
        return receiver_strategy

    @staticmethod
    def create_zeros(messages, actions):
        values = np.zeros((messages.size(), actions.size()))
        if isinstance(actions, WCSMunsellPalette):
            receiver_strategy = WCSMunsellReceiverStrategy(messages, actions, values)
        else:
            receiver_strategy = ReceiverStrategy(messages, actions, values)
        return receiver_strategy
