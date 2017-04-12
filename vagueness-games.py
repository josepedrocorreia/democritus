import argparse
import copy
import matplotlib.pyplot as plt
import numpy as np
import time

import yaml

from evolutionarydynamics import EvolutionaryDynamicsFactory
from statespaces import StateSpaceFactory


def plotStrategies(NMessages, NSenderActions, PerceptualSpace, Priors, Utility, Confusion, Sender, Receiver, block=False, vline=None):
    plt.clf()

    plt.subplot(2,2,1)
    plt.plot(PerceptualSpace, Priors)
    plt.ylim(ymin=0)
    plt.title('Priors')

    plt.subplot(2,4,3)
    plt.imshow(Utility, origin='upper', interpolation='none')
    plt.title('Utility')
    plt.subplot(2,4,4)
    plt.imshow(Confusion, origin='upper', interpolation='none')
    plt.title('Confusion')

    plt.subplot(2,2,3)
    for m in xrange(NSenderActions):
        MLabel = '$m_'+str(m)+'$' if m < NMessages else '$\\bot$'
        plt.plot(PerceptualSpace, Sender[:,m], label=MLabel)
    if vline:
        plt.axvline(vline, linestyle='--', color='red')
    plt.ylim(-0.1,1.1)
    plt.legend(loc='lower left')
    plt.title('Sender strategy')

    plt.subplot(2,2,4)
    for m in xrange(NMessages):
        plt.plot(PerceptualSpace, Receiver[m,:], label='$m_'+str(m)+'$')
    if vline:
        plt.axvline(vline, linestyle='--', color='red')
    plt.ylim(ymin=0)
    plt.legend(loc='lower left')
    plt.title('Receiver strategy')

    plt.show(block=block)
    plt.pause(0.01)

def normalize(Vector):
    return Vector / np.max(Vector)

def makePDF(Vector):
    if np.sum(Vector) == 0:
        Vector = np.ones(np.shape(Vector))
    return Vector / np.sum(Vector)

def makePDFPerRow(Matrix):
    return np.array([ makePDF(Row) for Row in Matrix ])

def normalizePerRow(Matrix):
    return np.array([ normalize(Row) for Row in Matrix ])
    
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

NMessages = cfg['message space']['size']
MessageSpace = range(NMessages)

LimitedPerception = cfg['perception']['limited']
Acuity = cfg['perception']['acuity']

Dynamics = EvolutionaryDynamicsFactory.create(cfg['dynamics'])

StateSpace = StateSpaceFactory.create(cfg['state space'])

Similarity = np.exp(-(StateSpace.distances ** 2 / (1.0 / Acuity) ** 2))

Utility = Similarity

Confusion = Similarity

Sender = makePDFPerRow(np.random.random((StateSpace.size(), NMessages)))
Receiver = makePDFPerRow(np.random.random((NMessages, StateSpace.size())))

converged = False
while not converged:

    ExpectedUtility = sum(StateSpace.priors[t] * Sender[t, m] * Receiver[m, x] * Utility[t, x]
                          for t in xrange(StateSpace.size()) for m in xrange(NMessages) for x in xrange(
        StateSpace.size()))
    print ExpectedUtility/np.sum(Utility)

    if not BatchMode: plotStrategies(NMessages, NMessages, StateSpace.states, StateSpace.priors, Utility, Confusion,
                                     Sender, Receiver)

    SenderBefore, ReceiverBefore = copy.deepcopy(Sender), copy.deepcopy(Receiver)

    ## Sender strategy

    Sender = Dynamics.update_sender(Sender, Receiver, StateSpace, MessageSpace, Utility)

    if LimitedPerception:
        Sender = np.dot(Confusion, Sender)

    Sender = makePDFPerRow(Sender)
    
    ## Receiver strategy
    
    Receiver = Dynamics.update_receiver(Sender, Receiver, StateSpace, MessageSpace, Utility)

    if LimitedPerception:
        Receiver = np.dot(Receiver, np.transpose(Confusion))

    Receiver = makePDFPerRow(Receiver)

    if np.sum(abs(Sender - SenderBefore)) < 0.01 and np.sum(abs(Receiver - ReceiverBefore)) < 0.01:
        converged = True
        if not BatchMode: print 'Language converged!'

MaximalElements = [ np.where(Receiver[m] == Receiver[m].max())[0] for m in xrange(NMessages) ]
Criterion1 = all(len(MaximalElements[m]) == 1 for m in xrange(NMessages))

Prototype = [ np.argmax(Receiver[m]) for m in xrange(NMessages) ]
CriterionX = all(Prototype[m1] != Prototype[m2] if m1 != m2 else True for m1 in xrange(NMessages) for m2 in xrange(NMessages))

# precision issues, otherwise Receiver[m,t1] > Receiver[m,t2]
Criterion2 = all(all(Receiver[m, t1] > Receiver[m, t2] or Receiver[m, t2] - Receiver[m, t1] < 0.01 for t1 in xrange(
    StateSpace.size()) for t2 in xrange(StateSpace.size()) if
                     Similarity[t1, Prototype[m]] > Similarity[t2, Prototype[m]]) for m in xrange(NMessages))

Criterion3 = all(all(
    Sender[t, m1] > Sender[t, m2] or Sender[t, m2] - Sender[t, m1] < 0.01 for m1 in xrange(NMessages) for m2 in
    xrange(NMessages) if Similarity[t, Prototype[m1]] > Similarity[t, Prototype[m2]]) for t in xrange(
    StateSpace.size()))

if Criterion1 and CriterionX and Criterion2 and Criterion3 and not BatchMode:
    print 'Language is proper vague language'
elif not BatchMode:
    print 'Language is NOT properly vague'

if not BatchMode: plotStrategies(NMessages, NMessages, StateSpace.states, StateSpace.priors, Utility, Confusion, Sender,
                                 Receiver,
                                 block=True)

# Outputting to file
SenderOutputFilename = args.output_prefix + '-sender.csv'
ReceiverOutputFilename = args.output_prefix + '-receiver.csv'
np.savetxt(SenderOutputFilename, Sender, delimiter=',')
np.savetxt(ReceiverOutputFilename, Receiver, delimiter=',')