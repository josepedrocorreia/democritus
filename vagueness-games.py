import argparse
import copy
import matplotlib.pyplot as plt
import numpy as np
import time

import yaml

from democritus import utils
from democritus.evolutionary_dynamics import EvolutionaryDynamicsFactory
from democritus.messages import MessagesFactory
from democritus.state_spaces import StateSpaceFactory


def plotStrategies(MessageSpace, StateSpace, Utility, Confusion, Sender, Receiver, block=False, vline=None):
    plt.clf()

    plt.subplot(2, 2, 1)
    plt.plot(StateSpace.states, StateSpace.priors)
    plt.ylim(ymin=0)
    plt.title('Priors')

    plt.subplot(2, 4, 3)
    plt.imshow(Utility, origin='upper', interpolation='none')
    plt.title('Utility')
    plt.subplot(2, 4, 4)
    plt.imshow(Confusion, origin='upper', interpolation='none')
    plt.title('Confusion')

    plt.subplot(2, 2, 3)
    for m in xrange(MessageSpace.size()):
        plt.plot(StateSpace.states, Sender[:, m], label='$m_' + str(m + 1) + '$')
    if vline:
        plt.axvline(vline, linestyle='--', color='red')
    plt.ylim(-0.1, 1.1)
    plt.legend(loc='lower left')
    plt.title('Sender strategy')

    plt.subplot(2, 2, 4)
    for m in xrange(MessageSpace.size()):
        plt.plot(StateSpace.states, Receiver[m, :], label='$m_' + str(m + 1) + '$')
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
argparser.add_argument('configfile', type=file)
argparser.add_argument('--output-prefix', default=time.strftime('%Y%m%d-%H%M%S'))
args = argparser.parse_args()

BatchMode = args.batch
ConfigFile = args.configfile

## Initialization

cfg = yaml.load(ConfigFile)

StateSpace = StateSpaceFactory.create(cfg['state space'])

MessageSpace = MessagesFactory.create(cfg['messages'])

LimitedPerception = cfg['perception']['limited']
Acuity = cfg['perception']['acuity']

Dynamics = EvolutionaryDynamicsFactory.create(cfg['dynamics'])

Similarity = np.exp(-(StateSpace.distances ** 2 / (1.0 / Acuity) ** 2))

Utility = Similarity

Confusion = Similarity

Sender = utils.make_row_stochastic(np.random.random((StateSpace.size(), MessageSpace.size())))
Receiver = utils.make_row_stochastic(np.random.random((MessageSpace.size(), StateSpace.size())))

converged = False
while not converged:

    ExpectedUtility = sum(StateSpace.priors[t] * Sender[t, m] * Receiver[m, x] * Utility[t, x]
                          for t in xrange(StateSpace.size()) for m in xrange(MessageSpace.size()) for x in xrange(
        StateSpace.size()))
    print ExpectedUtility / np.sum(Utility)

    if not BatchMode: plotStrategies(MessageSpace, StateSpace, Utility, Confusion, Sender, Receiver)

    SenderBefore, ReceiverBefore = copy.deepcopy(Sender), copy.deepcopy(Receiver)

    ## Sender strategy

    Sender = Dynamics.update_sender(Sender, Receiver, StateSpace, MessageSpace, Utility)

    if LimitedPerception:
        Sender = np.dot(Confusion, Sender)

    Sender = utils.make_row_stochastic(Sender)

    ## Receiver strategy

    Receiver = Dynamics.update_receiver(Sender, Receiver, StateSpace, MessageSpace, Utility)

    if LimitedPerception:
        Receiver = np.dot(Receiver, np.transpose(Confusion))

    Receiver = utils.make_row_stochastic(Receiver)

    if np.sum(abs(Sender - SenderBefore)) < 0.01 and np.sum(abs(Receiver - ReceiverBefore)) < 0.01:
        converged = True
        if not BatchMode: print 'Language converged!'

MaximalElements = [np.where(Receiver[m] == Receiver[m].max())[0] for m in xrange(MessageSpace.size())]
Criterion1 = all(len(MaximalElements[m]) == 1 for m in xrange(MessageSpace.size()))

Prototype = [np.argmax(Receiver[m]) for m in xrange(MessageSpace.size())]
CriterionX = all(
    Prototype[m1] != Prototype[m2] if m1 != m2 else True for m1 in xrange(MessageSpace.size()) for m2 in xrange(
        MessageSpace.size()))

# precision issues, otherwise Receiver[m,t1] > Receiver[m,t2]
Criterion2 = all(all(Receiver[m, t1] > Receiver[m, t2] or Receiver[m, t2] - Receiver[m, t1] < 0.01 for t1 in xrange(
    StateSpace.size()) for t2 in xrange(StateSpace.size()) if
                     Similarity[t1, Prototype[m]] > Similarity[t2, Prototype[m]]) for m in xrange(MessageSpace.size()))

Criterion3 = all(all(
    Sender[t, m1] > Sender[t, m2] or Sender[t, m2] - Sender[t, m1] < 0.01 for m1 in xrange(MessageSpace.size()) for m2
    in
    xrange(MessageSpace.size()) if Similarity[t, Prototype[m1]] > Similarity[t, Prototype[m2]]) for t in xrange(
    StateSpace.size()))

if Criterion1 and CriterionX and Criterion2 and Criterion3 and not BatchMode:
    print 'Language is proper vague language'
elif not BatchMode:
    print 'Language is NOT properly vague'

if not BatchMode: plotStrategies(MessageSpace, StateSpace, Utility, Confusion, Sender, Receiver, block=True)

# Outputting to file
SenderOutputFilename = args.output_prefix + '-sender.csv'
ReceiverOutputFilename = args.output_prefix + '-receiver.csv'
np.savetxt(SenderOutputFilename, Sender, delimiter=',')
np.savetxt(ReceiverOutputFilename, Receiver, delimiter=',')
