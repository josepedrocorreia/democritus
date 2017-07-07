import matplotlib.pyplot as plt
import numpy as np
import yaml

from democritus import utils
from democritus.dynamics import DynamicsFactory
from democritus.game import GameFactory
from democritus.specification import Specification


class SimulationSpecReader(object):
    @staticmethod
    def read_from_file(filename):
        config_file = open(filename, 'r')
        spec = Specification.from_dict(yaml.load(config_file))
        return SimulationSpecReader.read(spec)

    @staticmethod
    def read(spec):
        game_spec = spec.get_or_fail('game')
        dynamics_spec = spec.get_or_fail('dynamics')
        game = GameFactory.create(game_spec)
        dynamics = DynamicsFactory.create(dynamics_spec)
        return Simulation(game, dynamics)


class Simulation(object):
    def __init__(self, game, dynamics, sender_strategy=None, receiver_strategy=None):
        self.game = game
        self.dynamics = dynamics
        self.current_step = 0
        self.sender_strategies = []
        self.receiver_strategies = []
        if sender_strategy is None:
            sender_strategy = utils.make_row_stochastic(np.random.random((game.states.size(), game.messages.size())))
        if receiver_strategy is None:
            receiver_strategy = utils.make_row_stochastic(np.random.random((game.messages.size(), game.states.size())))
        self.sender_strategies.append(np.array(sender_strategy))
        self.receiver_strategies.append(np.array(receiver_strategy))

    def get_sender_strategy(self, step):
        return self.sender_strategies[step]

    def get_receiver_strategy(self, step):
        return self.receiver_strategies[step]

    def get_current_sender_strategy(self):
        return self.get_sender_strategy(self.current_step)

    def get_current_receiver_strategy(self):
        return self.get_receiver_strategy(self.current_step)

    def converged(self):
        if self.current_step < 1:
            return False
        previous_sender_strategy = self.get_sender_strategy(self.current_step - 1)
        previous_receiver_strategy = self.get_receiver_strategy(self.current_step - 1)
        if np.sum(abs(self.get_current_sender_strategy() - previous_sender_strategy)) < 0.01 \
                and np.sum(abs(self.get_current_receiver_strategy() - previous_receiver_strategy)) < 0.01:
            return True
        else:
            return False

    def step(self):
        sender_strategy = self.get_current_sender_strategy()
        receiver_strategy = self.get_current_receiver_strategy()

        new_sender_strategy = self.dynamics.update_sender(sender_strategy, receiver_strategy, self.game)
        new_receiver_strategy = self.dynamics.update_receiver(sender_strategy, receiver_strategy, self.game)

        self.sender_strategies.append(new_sender_strategy)
        self.receiver_strategies.append(new_receiver_strategy)
        self.current_step += 1

    def run_until_converged(self, max_steps=100, plot_steps=False, block_at_end=False):
        while self.current_step < max_steps and not self.converged():
            # Metrics stuff
            # sender_strategy = simulation.get_current_sender_strategy()
            # receiver_strategy = simulation.get_current_receiver_strategy()
            #
            # expected_utility = sum(
            #     game.states.priors[t] * sender_strategy[t, m] * receiver_strategy[m, x] * game.utility[t, x]
            #     for t in range(game.states.size()) for m in range(game.messages.size()) for x in range(
            #         game.states.size()))
            # print(expected_utility / np.sum(game.utility))
            if plot_steps:
                self.plot()
            self.step()

        if plot_steps:
            self.plot(block=block_at_end)

    def plot(self, block=False):
        plt.clf()

        plt.subplot(2, 2, 1)
        plt.plot(self.game.states.elements, self.game.states.priors)
        plt.ylim(ymin=0)
        plt.title('Priors')

        plt.subplot(2, 4, 3)
        plt.imshow(self.game.utility, origin='upper', interpolation='none')
        plt.title('Utility')
        plt.subplot(2, 4, 4)
        plt.imshow(self.game.similarity, origin='upper', interpolation='none')
        plt.title('Similarity')

        plt.subplot(2, 2, 3)
        sender_strategy = self.get_current_sender_strategy()
        for m in range(self.game.messages.size()):
            plt.plot(self.game.states.elements, sender_strategy[:, m], label='$m_' + str(m + 1) + '$')
        plt.ylim(-0.1, 1.1)
        plt.legend(loc='lower left')
        plt.title('Sender strategy')

        plt.subplot(2, 2, 4)
        receiver_strategy = self.get_current_receiver_strategy()
        for m in range(self.game.messages.size()):
            plt.plot(self.game.states.elements, receiver_strategy[m, :], label='$m_' + str(m + 1) + '$')
        plt.ylim(ymin=0)
        plt.legend(loc='lower left')
        plt.title('Receiver strategy')

        plt.show(block=block)
        plt.pause(0.01)
