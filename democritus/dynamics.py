import numpy as np

from utils import make_row_stochastic


class DynamicsFactory(object):
    @staticmethod
    def create(spec):
        dynamics_type = spec.get('type', 'replicator')
        if dynamics_type == 'replicator':
            return ReplicatorDynamics()
        if dynamics_type == 'best response':
            return BestResponseDynamics()
        if dynamics_type == 'quantal response':
            if 'rationality' not in spec:
                raise ValueError('Missing rationality in dynamics spec' + str(spec))
            return QuantalResponseDynamics(spec['rationality'])
        else:
            raise ValueError('Invalid dynamics specification: ' + str(spec))


class Dynamics(object):
    def update_sender(self, sender_strategy, receiver_strategy, state_space, message_space, utility):
        raise NotImplementedError('Subclasses of Dynamics must implement update_sender method')

    def update_receiver(self, sender_strategy, receiver_strategy, state_space, message_space, utility):
        raise NotImplementedError('Subclasses of Dynamics must implement update_receiver method')


class ReplicatorDynamics(Dynamics):
    def update_sender(self, sender_strategy, receiver_strategy, state_space, message_space, utility):
        n_states = state_space.size()
        n_messages = message_space.size()
        expected_utility = np.array(
            [[np.dot(receiver_strategy[m], utility[t]) for m in xrange(n_messages)] for t in xrange(n_states)])
        new_sender_strategy = np.zeros((n_states, n_messages))
        for t in xrange(n_states):
            for m in xrange(n_messages):
                new_sender_strategy[t, m] = sender_strategy[t, m] * \
                                            expected_utility[t, m] * n_messages / sum(expected_utility[t])
        return make_row_stochastic(new_sender_strategy)

    def update_receiver(self, sender_strategy, receiver_strategy, state_space, message_space, utility):
        n_states = state_space.size()
        n_messages = message_space.size()
        expected_utility = np.array(
            [[np.dot(state_space.priors * sender_strategy[:, m], utility[t])
              for t in xrange(n_states)]
             for m in xrange(n_messages)])
        new_receiver_strategy = np.zeros((n_messages, n_states))
        for m in xrange(n_messages):
            for t in xrange(n_states):
                new_receiver_strategy[m, t] = receiver_strategy[m, t] * \
                                              (expected_utility[m, t] * n_states + 0) / (sum(expected_utility[m]) + 0)
        return make_row_stochastic(new_receiver_strategy)


class BestResponseDynamics(Dynamics):
    def update_sender(self, sender_strategy, receiver_strategy, state_space, message_space, utility):
        n_states = state_space.size()
        n_messages = message_space.size()
        expected_utility = np.array(
            [[np.dot(receiver_strategy[m], utility[t]) for m in xrange(n_messages)] for t in xrange(n_states)])
        new_sender_strategy = np.zeros((n_states, n_messages))
        for t in xrange(n_states):
            for m in xrange(n_messages):
                new_sender_strategy[t, m] = 1 if expected_utility[t, m] == max(expected_utility[t]) else 0
        return make_row_stochastic(new_sender_strategy)

    def update_receiver(self, sender_strategy, receiver_strategy, state_space, message_space, utility):
        n_states = state_space.size()
        n_messages = message_space.size()
        expected_utility = np.array(
            [[np.dot(state_space.priors * sender_strategy[:, m], utility[t])
              for t in xrange(n_states)]
             for m in xrange(n_messages)])
        new_receiver_strategy = np.zeros((n_messages, n_states))
        for m in xrange(n_messages):
            for t in xrange(n_states):
                new_receiver_strategy[m, t] = 1 if expected_utility[m, t] == max(expected_utility[m]) else 0
        return make_row_stochastic(new_receiver_strategy)


class QuantalResponseDynamics(Dynamics):
    def __init__(self, rationality):
        self.rationality = rationality

    def update_sender(self, sender_strategy, receiver_strategy, state_space, message_space, utility):
        n_states = state_space.size()
        n_messages = message_space.size()
        expected_utility = np.array(
            [[np.dot(receiver_strategy[m], utility[t]) for m in xrange(n_messages)] for t in xrange(n_states)])
        new_sender_strategy = np.zeros((n_states, n_messages))
        for t in xrange(n_states):
            for m in xrange(n_messages):
                new_sender_strategy[t, m] = np.exp(self.rationality * expected_utility[t, m]) / \
                                            sum(np.exp(self.rationality * expected_utility[t]))
        return make_row_stochastic(new_sender_strategy)

    def update_receiver(self, sender_strategy, receiver_strategy, state_space, message_space, utility):
        n_states = state_space.size()
        n_messages = message_space.size()
        expected_utility = np.array(
            [[np.dot(state_space.priors * sender_strategy[:, m], utility[t])
              for t in xrange(n_states)]
             for m in xrange(n_messages)])
        new_receiver_strategy = np.zeros((n_messages, n_states))
        for m in xrange(n_messages):
            for t in xrange(n_states):
                new_receiver_strategy[m, t] = np.exp(self.rationality * expected_utility[m, t]) / \
                                              sum(np.exp(self.rationality * expected_utility[m]))
        return make_row_stochastic(new_receiver_strategy)
