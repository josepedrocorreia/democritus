from __future__ import division

from builtins import range

import numpy as np

from democritus.exceptions import InvalidValueInSpecification
from democritus.utils import make_row_stochastic


class DynamicsFactory(object):
    @staticmethod
    def create(spec):
        dynamics_type = spec.get('type') or 'replicator'
        if dynamics_type == 'replicator':
            return ReplicatorDynamics()
        if dynamics_type == 'best response':
            return BestResponseDynamics()
        if dynamics_type == 'quantal response':
            rationality_spec = spec.get_or_fail('rationality')
            return QuantalResponseDynamics(rationality_spec)
        else:
            raise InvalidValueInSpecification(spec, 'type', dynamics_type)


class Dynamics(object):
    def update_sender(self, sender_strategy, receiver_strategy, game):
        raise NotImplementedError('Subclasses of Dynamics must implement update_sender method')

    def update_receiver(self, sender_strategy, receiver_strategy, game):
        raise NotImplementedError('Subclasses of Dynamics must implement update_receiver method')


class ReplicatorDynamics(Dynamics):
    def update_sender(self, sender_strategy, receiver_strategy, game):
        n_states = game.states.size()
        n_messages = game.messages.size()
        expected_utility = np.array(
            [[np.dot(receiver_strategy[m], game.utility[t]) for m in range(n_messages)] for t in
             range(n_states)])
        new_sender_strategy = np.zeros((n_states, n_messages))
        for t in range(n_states):
            for m in range(n_messages):
                new_sender_strategy[t, m] = sender_strategy[t, m] * \
                                            expected_utility[t, m] * n_messages / sum(expected_utility[t])
        return make_row_stochastic(new_sender_strategy)

    def update_receiver(self, sender_strategy, receiver_strategy, game):
        n_states = game.states.size()
        n_messages = game.messages.size()
        expected_utility = np.array(
            [[np.dot(game.states.priors * sender_strategy[:, m], game.utility[t])
              for t in range(n_states)]
             for m in range(n_messages)])
        new_receiver_strategy = np.zeros((n_messages, n_states))
        for m in range(n_messages):
            for t in range(n_states):
                new_receiver_strategy[m, t] = receiver_strategy[m, t] * \
                                              (expected_utility[m, t] * n_states + 0) / (sum(expected_utility[m]) + 0)
        return make_row_stochastic(new_receiver_strategy)


class BestResponseDynamics(Dynamics):
    def update_sender(self, sender_strategy, receiver_strategy, game):
        n_states = game.states.size()
        n_messages = game.messages.size()
        expected_utility = np.array(
            [[np.dot(receiver_strategy[m], game.utility[t]) for m in range(n_messages)] for t in
             range(n_states)])
        new_sender_strategy = np.zeros((n_states, n_messages))
        for t in range(n_states):
            for m in range(n_messages):
                new_sender_strategy[t, m] = 1 if expected_utility[t, m] == max(expected_utility[t]) else 0
        return make_row_stochastic(new_sender_strategy)

    def update_receiver(self, sender_strategy, receiver_strategy, game):
        n_states = game.states.size()
        n_messages = game.messages.size()
        expected_utility = np.array(
            [[np.dot(game.states.priors * sender_strategy[:, m], game.utility[t])
              for t in range(n_states)]
             for m in range(n_messages)])
        new_receiver_strategy = np.zeros((n_messages, n_states))
        for m in range(n_messages):
            for t in range(n_states):
                new_receiver_strategy[m, t] = 1 if expected_utility[m, t] == max(expected_utility[m]) else 0
        return make_row_stochastic(new_receiver_strategy)


class QuantalResponseDynamics(Dynamics):
    def __init__(self, rationality):
        self.rationality = rationality

    def update_sender(self, sender_strategy, receiver_strategy, game):
        n_states = game.states.size()
        n_messages = game.messages.size()
        expected_utility = np.array(
            [[np.dot(receiver_strategy[m], game.utility[t]) for m in range(n_messages)] for t in
             range(n_states)])
        new_sender_strategy = np.zeros((n_states, n_messages))
        for t in range(n_states):
            for m in range(n_messages):
                new_sender_strategy[t, m] = np.exp(self.rationality * expected_utility[t, m]) / \
                                            sum(np.exp(self.rationality * expected_utility[t]))
        return make_row_stochastic(new_sender_strategy)

    def update_receiver(self, sender_strategy, receiver_strategy, game):
        n_states = game.states.size()
        n_messages = game.messages.size()
        expected_utility = np.array(
            [[np.dot(game.states.priors * sender_strategy[:, m], game.utility[t])
              for t in range(n_states)]
             for m in range(n_messages)])
        new_receiver_strategy = np.zeros((n_messages, n_states))
        for m in range(n_messages):
            for t in range(n_states):
                new_receiver_strategy[m, t] = np.exp(self.rationality * expected_utility[m, t]) / \
                                              sum(np.exp(self.rationality * expected_utility[m]))
        return make_row_stochastic(new_receiver_strategy)
