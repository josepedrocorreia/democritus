from __future__ import division

import argparse
import time
from builtins import range

import numpy as np

from democritus.simulation import SimulationSpecReader

## Read arguments

argparser = argparse.ArgumentParser()
argparser.add_argument('--batch', action='store_true')
argparser.add_argument('configfile')
argparser.add_argument('--output-prefix', default=time.strftime('%Y%m%d-%H%M%S'))
args = argparser.parse_args()

batch_mode = args.batch

# Initialization
simulation = SimulationSpecReader.read_from_file(args.configfile)
game = simulation.game
dynamics = simulation.dynamics

while not simulation.converged:

    sender_strategy = simulation.get_current_sender_strategy()
    receiver_strategy = simulation.get_current_receiver_strategy()

    expected_utility = sum(game.states.priors[t] * sender_strategy[t, m] * receiver_strategy[m, x] * game.utility[t, x]
                           for t in range(game.states.size()) for m in range(game.messages.size()) for x in range(
        game.states.size()))
    print(expected_utility / np.sum(game.utility))

    if not batch_mode:
        simulation.plot()

    simulation.step()

if not batch_mode:
    print('Language converged!')
    simulation.plot(block=True)

# Outputting to file
sender_output_filename = args.output_prefix + '-sender.csv'
receiver_output_filename = args.output_prefix + '-receiver.csv'
np.savetxt(sender_output_filename, simulation.get_current_sender_strategy(), delimiter=',')
np.savetxt(receiver_output_filename, simulation.get_current_receiver_strategy(), delimiter=',')
