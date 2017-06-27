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


def plotStrategies(game, Confusion, Sender, Receiver, block=False, vline=None):
    plt.clf()

    plt.subplot(2, 2, 1)
    plt.plot(game.states.elements, game.states.priors)
    plt.ylim(ymin=0)
    plt.title('Priors')

    plt.subplot(2, 4, 3)
    plt.imshow(game.utility, origin='upper', interpolation='none')
    plt.title('Utility')
    plt.subplot(2, 4, 4)
    plt.imshow(Confusion, origin='upper', interpolation='none')
    plt.title('Confusion')

    plt.subplot(2, 2, 3)
    for m in range(game.messages.size()):
        plt.plot(game.states.elements, Sender[:, m], label='$m_' + str(m + 1) + '$')
    if vline:
        plt.axvline(vline, linestyle='--', color='red')
    plt.ylim(-0.1, 1.1)
    plt.legend(loc='lower left')
    plt.title('Sender strategy')

    plt.subplot(2, 2, 4)
    for m in range(game.messages.size()):
        plt.plot(game.states.elements, Receiver[m, :], label='$m_' + str(m + 1) + '$')
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

BatchMode = args.batch
ConfigFile = open(args.configfile, 'r')

## Initialization

cfg = Specification.from_dict(yaml.load(ConfigFile))

game = GameFactory.create(cfg['game'])
StateSpace = game.states
MessageSpace = game.messages
Utility = game.utility
Similarity = game.similarity

LimitedPerception = cfg['perception']['limited']
Acuity = cfg['perception']['acuity']

Dynamics = DynamicsFactory.create(cfg['dynamics'])

Confusion = Similarity

Sender = utils.make_row_stochastic(np.random.random((StateSpace.size(), MessageSpace.size())))
Receiver = utils.make_row_stochastic(np.random.random((MessageSpace.size(), StateSpace.size())))

converged = False
while not converged:

    ExpectedUtility = sum(StateSpace.priors[t] * Sender[t, m] * Receiver[m, x] * Utility[t, x]
                          for t in range(StateSpace.size()) for m in range(MessageSpace.size()) for x in range(
        StateSpace.size()))
    print(ExpectedUtility / np.sum(Utility))

    if not BatchMode: plotStrategies(game, Confusion, Sender, Receiver)

    SenderBefore, ReceiverBefore = copy.deepcopy(Sender), copy.deepcopy(Receiver)

    ## Sender strategy

    Sender = Dynamics.update_sender(Sender, Receiver, game)

    if LimitedPerception:
        Sender = np.dot(Confusion, Sender)

    Sender = utils.make_row_stochastic(Sender)

    ## Receiver strategy

    Receiver = Dynamics.update_receiver(Sender, Receiver, game)

    if LimitedPerception:
        Receiver = np.dot(Receiver, np.transpose(Confusion))

    Receiver = utils.make_row_stochastic(Receiver)

    if np.sum(abs(Sender - SenderBefore)) < 0.01 and np.sum(abs(Receiver - ReceiverBefore)) < 0.01:
        converged = True
        if not BatchMode: print('Language converged!')

if not BatchMode: plotStrategies(game, Confusion, Sender, Receiver, block=True)

# Outputting to file
SenderOutputFilename = args.output_prefix + '-sender.csv'
ReceiverOutputFilename = args.output_prefix + '-receiver.csv'
np.savetxt(SenderOutputFilename, Sender, delimiter=',')
np.savetxt(ReceiverOutputFilename, Receiver, delimiter=',')
