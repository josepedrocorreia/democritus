import pytest

from democritus.runner import *
from democritus.simulation import Simulation


class TestSimulationRunner(object):
    def test_constructor_missing_configfile_argument_throws_exception(self):
        with pytest.raises(SystemExit):
            SimulationRunner([])

    def test_constructor_defaults(self, config_file_name):
        simulation_runner = SimulationRunner([config_file_name])
        assert type(simulation_runner.simulation) is Simulation
        assert simulation_runner.args.configfile == config_file_name
        assert simulation_runner.args.max_steps == 100
        assert simulation_runner.args.batch is False
        assert not simulation_runner.args.output_prefix == ''
        assert simulation_runner.args.output_dir == '.'

    def test_constructor_max_steps_argument(self, config_file_name):
        simulation_runner = SimulationRunner([config_file_name, '--max-steps=99'])
        assert simulation_runner.args.max_steps == 99

    def test_constructor_batch_argument(self, config_file_name):
        simulation_runner = SimulationRunner([config_file_name, '--batch'])
        assert simulation_runner.args.batch is True

    def test_constructor_output_prefix_argument(self, config_file_name):
        simulation_runner = SimulationRunner([config_file_name, '--output-prefix=some_prefix'])
        assert simulation_runner.args.output_prefix == 'some_prefix'

    def test_constructor_output_dir_argument(self, config_file_name, tmpdir):
        simulation_runner = SimulationRunner([config_file_name, '--output-dir=%s' % str(tmpdir)])
        assert simulation_runner.args.output_dir == str(tmpdir)

    def test_constructor_output_dir_argument_non_existent_dir(self, config_file_name):
        with pytest.raises(SystemExit):
            SimulationRunner([config_file_name, '--output-dir=dir?????????'])

    def test_run(self, config_file_name, tmpdir):
        simulation_runner = SimulationRunner([config_file_name])
        assert simulation_runner.simulation.current_step == 0
        simulation_runner.args.max_steps = 1
        simulation_runner.args.batch = True
        simulation_runner.args.output_prefix = 'test_run'
        simulation_runner.args.output_dir = str(tmpdir)
        simulation_runner.run()
        assert simulation_runner.simulation.current_step == 1

    def test_write_results(self, config_file_name, tmpdir):
        simulation_runner = SimulationRunner([config_file_name])
        simulation_runner.args.output_prefix = 'test_write_results'
        simulation_runner.args.output_dir = str(tmpdir)
        assert not os.path.exists(os.path.join(str(tmpdir), 'test_write_results-sender.csv'))
        assert not os.path.exists(os.path.join(str(tmpdir), 'test_write_results-receiver.csv'))
        simulation_runner.write_results()
        assert os.path.isfile(os.path.join(str(tmpdir), 'test_write_results-sender.csv'))
        assert os.path.isfile(os.path.join(str(tmpdir), 'test_write_results-receiver.csv'))
