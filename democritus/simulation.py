import matplotlib.pyplot as plt
import numpy as np

from democritus import utils


class Simulation(object):
    def __init__(self, game, dynamics, simulation_metrics=None, sender_strategy=None, receiver_strategy=None):
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
        self.simulation_measurements = []
        if simulation_metrics is not None:
            for metric in simulation_metrics:
                measurement = metric.calculate(self)
                self.simulation_measurements.append((metric, [measurement]))
        # TODO: Fix differently
        self.first_plot = True
        plt.rcParams['toolbar'] = 'None'
        plt.style.use('seaborn-deep')

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

        for metric, measurements in self.simulation_measurements:
            new_measurement = metric.calculate(self)
            measurements.append(new_measurement)

    def run_until_converged(self, max_steps=100, plot_steps=False, block_at_end=False):
        if type(max_steps) is not int:
            raise TypeError('Value of max_steps should be int')

        while self.current_step < max_steps and not self.converged():
            if plot_steps:
                self.plot()
            self.step()

        if plot_steps:
            self.plot(block=block_at_end)

    def plot(self, block=False):
        n_metrics = len(self.simulation_measurements)
        metric_plot_span = 4
        n_rows = 3 if n_metrics > 0 else 2
        n_cols = n_metrics * metric_plot_span if n_metrics > 0 else metric_plot_span
        plot_grid_shape = (n_rows, n_cols)
        states_plot_span = n_cols // 2
        utility_plot_span = n_cols // 4
        strategy_plot_span = n_cols // 2

        plt.clf()

        plt.subplot2grid(plot_grid_shape, (0, 0), colspan=states_plot_span)
        plt.title('Priors')
        self.game.states.plot()

        plt.subplot2grid(plot_grid_shape, (0, states_plot_span), colspan=utility_plot_span)
        plt.imshow(self.game.utility, origin='upper', interpolation='none')
        plt.title('Utility')
        plt.subplot2grid(plot_grid_shape, (0, states_plot_span + utility_plot_span), colspan=utility_plot_span)
        plt.imshow(self.game.similarity, origin='upper', interpolation='none')
        plt.title('Similarity')

        plt.subplot2grid(plot_grid_shape, (1, 0), colspan=strategy_plot_span)
        sender_strategy = self.get_current_sender_strategy()
        for m in range(self.game.messages.size()):
            plt.plot(self.game.states.elements, sender_strategy[:, m], label='$m_' + str(m + 1) + '$', marker='.')
        plt.ylim(-0.1, 1.1)
        plt.legend(loc='lower left')
        plt.title('Sender strategy')

        plt.subplot2grid(plot_grid_shape, (1, strategy_plot_span), colspan=strategy_plot_span)
        receiver_strategy = self.get_current_receiver_strategy()
        for m in range(self.game.messages.size()):
            plt.plot(self.game.states.elements, receiver_strategy[m, :], label='$m_' + str(m + 1) + '$', marker='.')
        plt.ylim(ymin=0)
        plt.legend(loc='lower left')
        plt.title('Receiver strategy')

        for i in range(n_metrics):
            # TODO: make this more readable
            plt.subplot2grid(plot_grid_shape, (2, i * metric_plot_span), colspan=metric_plot_span)
            simulation_measurement = self.simulation_measurements[i]
            plt.plot(list(range(self.current_step + 1)), simulation_measurement[1], marker='.')
            plt.ylim(ymin=0)
            plt.title(simulation_measurement[0].name)

        if self.first_plot:
            plt.tight_layout(h_pad=0.5, w_pad=0)
        self.first_plot = False
        plt.show(block=block)
        plt.pause(0.000001)
