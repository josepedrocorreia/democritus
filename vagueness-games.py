import sys
import copy

from numpy import random as random

import matplotlib.pyplot as plt

# Switch to ConfigObj?
import ConfigParser

from PerceptualSpaces import *

def plotStrategies(NMessages, NSpeakerActions, PerceptualSpace, Priors, Utility, Confusion, Speaker, Hearer, block=False, vline=None):
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
    for m in xrange(NSpeakerActions):
        MLabel = '$m_'+str(m)+'$' if m < NMessages else '$\\bot$'
        plt.plot(PerceptualSpace, Speaker[:,m], label=MLabel)
    if vline:
        plt.axvline(vline, linestyle='--', color='red')
    plt.ylim(-0.1,1.1)
    plt.legend(loc='lower left')
    plt.title('Speaker strategy')

    plt.subplot(2,2,4)
    for m in xrange(NMessages):
        plt.plot(PerceptualSpace, Hearer[m,:], label='$m_'+str(m)+'$')
    if vline:
        plt.axvline(vline, linestyle='--', color='red')
    plt.ylim(ymin=0)
    plt.legend(loc='lower left')
    plt.title('Hearer strategy')

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
    
## Batch mode

if len(sys.argv) == 1:
    BatchMode = False
else:
    BatchMode = True

if BatchMode:
    if len(sys.argv) < 2:
        print "Usage: python", sys.argv[0], "<configuration file>"
        sys.exit(1)
    else:
        ConfigFile = sys.argv[1]
else:
    ConfigFile = 'default.cfg'
    
## Settings - Signaling game
cfg = ConfigParser.ConfigParser()
cfg.read(ConfigFile)

NStates = cfg.getint('Signaling game', 'Number of states')
PriorDistributionType = cfg.get('Signaling game', 'Prior distribution') # add additional options (central tendency, deviation, ...)

NMessages = cfg.getint('Signaling game', 'Number of messages')
OptOutOption = cfg.getboolean('Signaling game', 'Opt-out option')

LimitedPerception = cfg.getboolean('Signaling game', 'Limited perception') # make complex object
Acuity = cfg.getint('Signaling game', 'Perceptual acuity')

Rationality = 20

Dynamics = cfg.get('Signaling game', 'Evolutionary dynamics')

## Initialization

PerceptualSpace = PerceptualSpace(NStates).state_space

if PriorDistributionType == 'uniform':
    Priors = UniformPerceptualSpace(NStates).prior_distribution
elif PriorDistributionType == 'normal':
    Priors = NormalPerceptualSpace(NStates).prior_distribution
    Priors = makePDF(Priors)
elif PriorDistributionType == 'degenerate':
    Priors = np.zeros(NStates)
    Priors[NStates/2] = 1
elif PriorDistributionType == 'bimodal':
    Priors1 = makePDF(stats.norm.pdf(PerceptualSpace, loc=0, scale=0.1))
    Priors2 = makePDF(stats.norm.pdf(PerceptualSpace, loc=1, scale=0.1))
    Priors = makePDF(Priors1 + Priors2)

Distance = np.array([[ abs(x - y)
                     for y in PerceptualSpace ]
                    for x in PerceptualSpace ])

Similarity = np.exp(-(Distance**2 / (1.0 / Acuity)**2))

Utility = Similarity

Confusion = Similarity

if OptOutOption: 
    NSpeakerActions = NMessages + 1 # speaker can opt-out
else:
    NSpeakerActions = NMessages

Speaker = makePDFPerRow(random.random((NStates,NSpeakerActions)))
Hearer = makePDFPerRow(random.random((NMessages,NStates)))

# only used when there is an opt-out option
Cost = np.sum(Utility) / NStates**2 if OptOutOption else 0

converged = False
while not converged:
    
    ExpectedUtility = sum(Priors[t] * Speaker[t,m] * Hearer[m,x] * Utility[t,x]
               for t in xrange(NStates) for m in xrange(NMessages) for x in xrange(NStates))
    print ExpectedUtility/np.sum(Utility)

    if not BatchMode: plotStrategies(NMessages, NSpeakerActions, PerceptualSpace, Priors, Utility, Confusion, Speaker, Hearer)

    SpeakerBefore, HearerBefore = copy.deepcopy(Speaker), copy.deepcopy(Hearer)

    ## Speaker strategy
    
    UtilitySpeaker = np.array([ [ np.dot(Hearer[m], Utility[t]) - Cost if m < NMessages else 0
                                for m in xrange(NSpeakerActions) ]
                              for t in xrange(NStates) ])

    for t in xrange(NStates):
        for m in xrange(NSpeakerActions):
            if Dynamics == 'replicator':
                Speaker[t,m] = Speaker[t,m] * (UtilitySpeaker[t,m] * NSpeakerActions + Cost * NSpeakerActions) / (sum(UtilitySpeaker[t]) + Cost * NSpeakerActions)
            elif Dynamics == 'best response':
                Speaker[t,m] = 1 if UtilitySpeaker[t,m] == max(UtilitySpeaker[t]) else 0
            elif Dynamics == 'quantal best response':
                Speaker[t,m] = np.exp(Rationality * UtilitySpeaker[t,m]) / sum(np.exp(Rationality * UtilitySpeaker[t]))

    if LimitedPerception:
        Speaker = np.dot(Confusion, Speaker)

    Speaker = makePDFPerRow(Speaker)
    
    ## Hearer strategy
    
    UtilityHearer = np.array([ [ np.dot(Priors * Speaker[:,m], Utility[t])
                               for t in xrange(NStates) ]
                             for m in xrange(NMessages) ])

    for m in xrange(NMessages):
        for t in xrange(NStates):
            if Dynamics == 'replicator':
                Hearer[m,t] = Hearer[m,t] * (UtilityHearer[m,t] * NStates + 0) / (sum(UtilityHearer[m]) + 0)
            elif Dynamics == 'best response':
                Hearer[m,t] = 1 if UtilityHearer[m,t] == max(UtilityHearer[m]) else 0
            elif Dynamics == 'quantal best response':
                Hearer[m,t] = np.exp(Rationality * UtilityHearer[m,t]) / sum(np.exp(Rationality * UtilityHearer[m]))

    if LimitedPerception:
        Hearer = np.dot(Hearer, np.transpose(Confusion))

    Hearer = makePDFPerRow(Hearer)

    if np.sum(abs(Speaker - SpeakerBefore)) < 0.01 and np.sum(abs(Hearer - HearerBefore)) < 0.01:
        converged = True
        if not BatchMode: print 'Language converged!'

MaximalElements = [ np.where(Hearer[m] == Hearer[m].max())[0] for m in xrange(NMessages) ]
Criterion1 = all(len(MaximalElements[m]) == 1 for m in xrange(NMessages))

Prototype = [ np.argmax(Hearer[m]) for m in xrange(NMessages) ]
CriterionX = all(Prototype[m1] != Prototype[m2] if m1 != m2 else True for m1 in xrange(NMessages) for m2 in xrange(NMessages))

# precision issues, otherwise Hearer[m,t1] > Hearer[m,t2]
Criterion2 = all(all(Hearer[m,t1] > Hearer[m,t2] or Hearer[m,t2] - Hearer[m,t1] < 0.01 for t1 in xrange(NStates) for t2 in xrange(NStates) if Similarity[t1,Prototype[m]] > Similarity[t2,Prototype[m]]) for m in xrange(NMessages)) 

Criterion3 = all(all(Speaker[t,m1] > Speaker[t,m2] or Speaker[t,m2] - Speaker[t,m1] < 0.01 for m1 in xrange(NMessages) for m2 in xrange(NMessages) if Similarity[t,Prototype[m1]] > Similarity[t,Prototype[m2]]) for t in xrange(NStates))

if Criterion1 and CriterionX and Criterion2 and Criterion3 and not BatchMode:
    print 'Language is proper vague language'
elif not BatchMode:
    print 'Language is NOT properly vague'

if not BatchMode: plotStrategies(NMessages, NSpeakerActions, PerceptualSpace, Priors, Utility, Confusion, Speaker, Hearer, block=True)