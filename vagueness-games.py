from democritus.simulation_runner import SimulationRunner

runner = SimulationRunner()
runner.run(block_at_end=False)
runner.write_results()
