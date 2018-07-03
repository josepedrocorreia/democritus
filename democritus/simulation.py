from collections import OrderedDict

import matplotlib.pyplot as plt
import numpy as np

from democritus.factories import SenderStrategyFactory, ReceiverStrategyFactory
from democritus.metrics import ExpectedUtilityMetric, SenderNormalizedEntropyMetric, ReceiverNormalizedEntropyMetric


class SimulationMetricConverter(object):
    @staticmethod
    def create(name):
        name = name.lower()
        if name == 'expected utility':
            return ExpectedUtilityMetric()
        elif name == 'sender entropy':
            return SenderNormalizedEntropyMetric()
        elif name == 'receiver entropy':
            return ReceiverNormalizedEntropyMetric()
        else:
            raise ValueError('Unknown simulation metric with name: %s', name)


class SimulationMeasurementsCollector(object):
    def __init__(self, simulation_metrics):
        self.metrics = OrderedDict()
        self.measurements = OrderedDict()
        for metric_name in simulation_metrics:
            metric_name = metric_name.lower()
            self.metrics[metric_name] = SimulationMetricConverter.create(metric_name)
            self.measurements[metric_name] = []

    def number_of_metrics(self):
        return len(self.metrics)

    def get_metric_class(self, metric_name):
        return self.metrics.get(metric_name.lower())

    def get_measurements(self, metric_name):
        return self.measurements.get(metric_name.lower())

    def calculate_all(self, simulation):
        for metric_name, metric_class in self.metrics.items():
            measurements = self.measurements.get(metric_name)
            new_measurement = metric_class.calculate(simulation)
            measurements.append(new_measurement)
            self.measurements[metric_name] = measurements

    def plot(self):
        metric_names = list(self.metrics.keys())
        n_metrics = len(metric_names)
        for i in range(n_metrics):
            axi = plt.subplot2grid((n_metrics, 1), (i, 0))
            metric_class = self.metrics.get(metric_names[i])
            metric_class.plot(self.measurements[metric_names[i]], axi)
        plt.tight_layout(h_pad=0.5, w_pad=0)


class Simulation(object):
    def __init__(self, game, dynamics, simulation_metrics=None, sender_strategy=None, receiver_strategy=None):
        self.game = game
        self.dynamics = dynamics
        self.current_step = 0
        self.sender_strategies = []
        self.receiver_strategies = []
        if sender_strategy is None:
            sender_strategy = SenderStrategyFactory.create_random(game.states, game.messages)
        if receiver_strategy is None:
            receiver_strategy = ReceiverStrategyFactory.create_random(game.messages, game.actions)
        self.sender_strategies.append(sender_strategy)
        self.receiver_strategies.append(receiver_strategy)
        self.measurements_collector = SimulationMeasurementsCollector(simulation_metrics or [])
        self.measurements_collector.calculate_all(self)
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
        if np.sum(abs(self.get_current_sender_strategy().values - previous_sender_strategy.values)) < 0.01 \
                and np.sum(abs(self.get_current_receiver_strategy().values - previous_receiver_strategy.values)) < 0.01:
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

        self.measurements_collector.calculate_all(self)

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
        n_rows = 2
        n_cols = (4 if self.game.confusion is not None else 2)
        states_plot_span = n_cols // 2
        utility_plot_span = n_cols // 2 // (2 if self.game.confusion is not None else 1)
        strategy_plot_span = n_cols // 2
        plot_grid_shape = (n_rows, n_cols)

        plt.figure(0)
        ax1 = plt.subplot2grid(plot_grid_shape, (0, 0), colspan=states_plot_span)
        ax1.set_title('Priors')
        self.game.states.plot(ax1)

        ax2 = plt.subplot2grid(plot_grid_shape, (0, states_plot_span), colspan=utility_plot_span)
        ax2.set_title('Utility')
        self.game.utility.plot(ax2)
        if self.game.confusion is not None:
            ax4 = plt.subplot2grid(plot_grid_shape, (0, states_plot_span + utility_plot_span),
                                   colspan=utility_plot_span)
            ax4.set_title('Confusion')
            self.game.confusion.plot(ax4)

        ax5 = plt.subplot2grid(plot_grid_shape, (1, 0), colspan=strategy_plot_span)
        ax5.set_title('Sender strategy')
        self.get_current_sender_strategy().plot(ax5)

        ax6 = plt.subplot2grid(plot_grid_shape, (1, strategy_plot_span), colspan=strategy_plot_span)
        ax6.set_title('Receiver strategy')
        self.get_current_receiver_strategy().plot(ax6)

        if self.measurements_collector.number_of_metrics() > 0:
            plt.figure(1)
            self.measurements_collector.plot()

        plt.figure(0)
        plt.tight_layout(h_pad=0.5, w_pad=0)
        plt.show(block=block)
        plt.pause(0.00001)
