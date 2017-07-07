import argparse
import time

import numpy as np

from democritus.simulation import SimulationSpecReader

# Read arguments
argparser = argparse.ArgumentParser()
argparser.add_argument('--batch', action='store_true')
argparser.add_argument('configfile')
argparser.add_argument('--output-prefix', default=time.strftime('%Y%m%d-%H%M%S'))
args = argparser.parse_args()
batch_mode = args.batch

# Run
simulation = SimulationSpecReader.read_from_file(args.configfile)
simulation.run_until_converged(max_steps=1, plot_steps=not batch_mode, block_at_end=True)

# Output to file
sender_output_filename = args.output_prefix + '-sender.csv'
receiver_output_filename = args.output_prefix + '-receiver.csv'
np.savetxt(sender_output_filename, simulation.get_current_sender_strategy(), delimiter=',')
np.savetxt(receiver_output_filename, simulation.get_current_receiver_strategy(), delimiter=',')
