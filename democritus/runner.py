import argparse
import os
import sys
import time

import numpy as np

from democritus.converters import SimulationSpecReader


def existing_dir(prospective_dir):
    if not os.path.isdir(prospective_dir):
        raise argparse.ArgumentTypeError('%s is not a valid path' % prospective_dir)
    else:
        return prospective_dir


class SimulationRunner(object):
    def __init__(self, args):
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument('configfile')
        arg_parser.add_argument('--max-steps', type=int, default=100)
        arg_parser.add_argument('--batch', action='store_true')
        arg_parser.add_argument('--output-prefix', default=time.strftime('%Y%m%d-%H%M%S'))
        arg_parser.add_argument('--output-dir', type=existing_dir, default='.')
        self.args = arg_parser.parse_args(args)
        self.simulation = SimulationSpecReader.read_from_file(self.args.configfile)

    def run(self, block_at_end=True):
        plot_steps = not self.args.batch
        self.simulation.run_until_converged(max_steps=self.args.max_steps, plot_steps=plot_steps,
                                            block_at_end=block_at_end)

    def write_results(self):
        sender_output_filename = os.path.join(self.args.output_dir, self.args.output_prefix + '-sender.csv')
        receiver_output_filename = os.path.join(self.args.output_dir, self.args.output_prefix + '-receiver.csv')
        np.savetxt(sender_output_filename, self.simulation.get_current_sender_strategy(), delimiter=',')
        np.savetxt(receiver_output_filename, self.simulation.get_current_receiver_strategy(), delimiter=',')


if __name__ == "__main__":
    runner = SimulationRunner(sys.argv[1:])
    runner.run(block_at_end=False)
    runner.write_results()
