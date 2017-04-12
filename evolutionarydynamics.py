import numpy as np

from utils import make_row_stochastic


class EvolutionaryDynamics(object):
    def update_sender(self, sender_strategy, receiver_strategy, state_space, message_space, utility):
        raise NotImplementedError('Subclasses of EvolutionaryDynamics must implement update_sender method')

    def update_receiver(self, sender_strategy, receiver_strategy, state_space, message_space, utility):
        raise NotImplementedError('Subclasses of EvolutionaryDynamics must implement update_receiver method')


class ReplicatorDynamics(EvolutionaryDynamics):
    def update_sender(self, sender_strategy, receiver_strategy, state_space, message_space, utility):
        n_states = state_space.size()
        n_messages = len(message_space)
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
        n_messages = len(message_space)
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


class BestResponseDynamics(EvolutionaryDynamics):
    def update_sender(self, sender_strategy, receiver_strategy, state_space, message_space, utility):
        n_states = state_space.size()
        n_messages = len(message_space)
        expected_utility = np.array(
            [[np.dot(receiver_strategy[m], utility[t]) for m in xrange(n_messages)] for t in xrange(n_states)])
        new_sender_strategy = np.zeros((n_states, n_messages))
        for t in xrange(n_states):
            for m in xrange(n_messages):
                new_sender_strategy[t, m] = 1 if expected_utility[t, m] == max(expected_utility[t]) else 0
        return make_row_stochastic(new_sender_strategy)

    def update_receiver(self, sender_strategy, receiver_strategy, state_space, message_space, utility):
        n_states = state_space.size()
        n_messages = len(message_space)
        expected_utility = np.array(
            [[np.dot(state_space.priors * sender_strategy[:, m], utility[t])
              for t in xrange(n_states)]
             for m in xrange(n_messages)])
        new_receiver_strategy = np.zeros((n_messages, n_states))
        for m in xrange(n_messages):
            for t in xrange(n_states):
                new_receiver_strategy[m, t] = 1 if expected_utility[m, t] == max(expected_utility[m]) else 0
        return make_row_stochastic(new_receiver_strategy)


class QuantalResponseDynamics(EvolutionaryDynamics):
    def __init__(self, spec):
        self.rationality = spec['rationality']

    def update_sender(self, sender_strategy, receiver_strategy, state_space, message_space, utility):
        n_states = state_space.size()
        n_messages = len(message_space)
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
        n_messages = len(message_space)
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


class EvolutionaryDynamicsFactory(object):
    @staticmethod
    def create(spec):
        dynamics_type = spec['type']
        if dynamics_type == 'replicator':
            return ReplicatorDynamics()
        if dynamics_type == 'best response':
            return BestResponseDynamics()
        if dynamics_type == 'quantal response':
            return QuantalResponseDynamics(spec)
        # type is unknown
        raise ValueError('Invalid evolutionary dynamics specification: ' + str(spec))
