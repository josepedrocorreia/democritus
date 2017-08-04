from builtins import range

import numpy as np


class SimulationMetric(object):
    def calculate(self, simulation):
        raise NotImplementedError('Subclasses of SimulationMetric must implement \'calculate\' method')

    def plot(self, measurements, axis):
        raise NotImplementedError('Subclasses of SimulationMetric must implement \'plot\' method')


class ExpectedUtilityMetric(SimulationMetric):
    name = 'Expected utility'

    def calculate(self, simulation):
        game = simulation.game
        sender_strategy = simulation.get_current_sender_strategy()
        receiver_strategy = simulation.get_current_receiver_strategy()

        expected_utility = sum(
            game.states.priors[t] * sender_strategy[t, m] * receiver_strategy[m, x] * game.utility[t, x]
            for t in range(game.number_of_states())
            for m in range(game.number_of_messages())
            for x in range(game.number_of_actions()))
        maximum_expected_utility = sum(game.states.priors[t] * np.max(game.utility[t])
                                       for t in range(game.number_of_states()))
        return expected_utility / maximum_expected_utility

    def plot(self, measurements, axis):
        axis.set_title(self.name)
        axis.plot(list(range(len(measurements))), measurements, marker='.')
        axis.set_ylim(ymin=0)
        axis.set_xlim(xmin=0)


class SenderNormalizedEntropyMetric(SimulationMetric):
    name = 'Sender entropy'

    def calculate(self, simulation):
        game = simulation.game
        sender_strategy = simulation.get_current_sender_strategy()
        entropy = -sum(
            np.log(sender_strategy[c, a]) * sender_strategy[c, a] if sender_strategy[c, a] != 0 else 0
            for c in range(game.number_of_states())
            for a in range(game.number_of_messages()))
        normalization_factor = game.number_of_states() * np.log(game.number_of_messages())
        return entropy / normalization_factor

    def plot(self, measurements, axis):
        axis.set_title(self.name)
        axis.plot(list(range(len(measurements))), measurements, marker='.')
        axis.set_ylim(ymin=0)
        axis.set_xlim(xmin=0)


class ReceiverNormalizedEntropyMetric(SimulationMetric):
    name = 'Receiver entropy'

    def calculate(self, simulation):
        game = simulation.game
        receiver_strategy = simulation.get_current_receiver_strategy()
        entropy = -sum(
            np.log(receiver_strategy[c, a]) * receiver_strategy[c, a] if receiver_strategy[c, a] != 0 else 0
            for c in range(game.number_of_messages())
            for a in range(game.number_of_actions()))
        normalization_factor = game.number_of_messages() * np.log(game.number_of_actions())
        return entropy / normalization_factor

    def plot(self, measurements, axis):
        axis.set_title(self.name)
        axis.plot(list(range(len(measurements))), measurements, marker='.')
        axis.set_ylim(ymin=0)
        axis.set_xlim(xmin=0)
