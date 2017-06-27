from __future__ import division

import argparse
import copy
import time
from builtins import range

import matplotlib.pyplot as plt
import numpy as np
import yaml

from democritus import utils
from democritus.dynamics import DynamicsFactory
from democritus.game import GameFactory
from democritus.specification import Specification


def plot_strategies(game, sender_strategy, receiver_strategy, block=False, vline=None):
    plt.clf()

    plt.subplot(2, 2, 1)
    plt.plot(game.states.elements, game.states.priors)
    plt.ylim(ymin=0)
    plt.title('Priors')

    plt.subplot(2, 4, 3)
    plt.imshow(game.utility, origin='upper', interpolation='none')
    plt.title('Utility')
    plt.subplot(2, 4, 4)
    plt.imshow(game.similarity, origin='upper', interpolation='none')
    plt.title('Similarity')

    plt.subplot(2, 2, 3)
    for m in range(game.messages.size()):
        plt.plot(game.states.elements, sender_strategy[:, m], label='$m_' + str(m + 1) + '$')
    if vline:
        plt.axvline(vline, linestyle='--', color='red')
    plt.ylim(-0.1, 1.1)
    plt.legend(loc='lower left')
    plt.title('Sender strategy')

    plt.subplot(2, 2, 4)
    for m in range(game.messages.size()):
        plt.plot(game.states.elements, receiver_strategy[m, :], label='$m_' + str(m + 1) + '$')
    if vline:
        plt.axvline(vline, linestyle='--', color='red')
    plt.ylim(ymin=0)
    plt.legend(loc='lower left')
    plt.title('Receiver strategy')

    plt.show(block=block)
    plt.pause(0.01)


## Read arguments

argparser = argparse.ArgumentParser()
argparser.add_argument('--batch', action='store_true')
argparser.add_argument('configfile')
argparser.add_argument('--output-prefix', default=time.strftime('%Y%m%d-%H%M%S'))
args = argparser.parse_args()

batch_mode = args.batch
config_file = open(args.configfile, 'r')

## Initialization

cfg = Specification.from_dict(yaml.load(config_file))
game = GameFactory.create(cfg['game'])
dynamics = DynamicsFactory.create(cfg['dynamics'])

sender_strategy = utils.make_row_stochastic(np.random.random((game.states.size(), game.messages.size())))
receiver_strategy = utils.make_row_stochastic(np.random.random((game.messages.size(), game.states.size())))

converged = False
while not converged:

    expected_utility = sum(game.states.priors[t] * sender_strategy[t, m] * receiver_strategy[m, x] * game.utility[t, x]
                           for t in range(game.states.size()) for m in range(game.messages.size()) for x in range(
        game.states.size()))
    print(expected_utility / np.sum(game.utility))

    if not batch_mode:
        plot_strategies(game, sender_strategy, receiver_strategy)

    sender_before, receiver_before = copy.deepcopy(sender_strategy), copy.deepcopy(receiver_strategy)

    ## Sender strategy

    sender_strategy = dynamics.update_sender(sender_strategy, receiver_strategy, game)

    if game.imprecise:
        sender_strategy = np.dot(game.similarity, sender_strategy)

    sender_strategy = utils.make_row_stochastic(sender_strategy)

    ## Receiver strategy

    receiver_strategy = dynamics.update_receiver(sender_strategy, receiver_strategy, game)

    if game.imprecise:
        receiver_strategy = np.dot(receiver_strategy, np.transpose(game.similarity))

    receiver_strategy = utils.make_row_stochastic(receiver_strategy)

    if np.sum(abs(sender_strategy - sender_before)) < 0.01 and np.sum(abs(receiver_strategy - receiver_before)) < 0.01:
        converged = True
        if not batch_mode: print('Language converged!')

if not batch_mode:
    plot_strategies(game, sender_strategy, receiver_strategy, block=True)

# Outputting to file
sender_output_filename = args.output_prefix + '-sender.csv'
receiver_output_filename = args.output_prefix + '-receiver.csv'
np.savetxt(sender_output_filename, sender_strategy, delimiter=',')
np.savetxt(receiver_output_filename, receiver_strategy, delimiter=',')
