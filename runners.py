from pipeline import ReleaseWorker

import inspect


def _parse_step_config(step):
    # Apply step specific step_config. Defaults are defined in step method level
    if type(step) is dict:           # Step contains additional config
        step_name = step.keys()[0]   # Steps should be a dict with one single item
        step_config = step[step_name]
    else:
        step_name = step
        step_config = dict()
    return step_name, step_config


class Runner(object):
    """Base runner class"""
    def __init__(self, source, task_definition, runner_config, task_config):
        self.source = source
        self.config = runner_config
        self.config.update(task_config)
        self.task = task_definition
        self.pipeline = None  # Should be initialized by the child class

    def configure(self):
        """Configuration should be done at child level"""
        pass

    def do(self, task):
        """Ideally, child classes should not override this method"""
        self.configure()
        steps = self.task[task]['steps']
        for step in steps:
            print('-'*120 + '\nRunning step %s' % step)
            step_name, step_config = _parse_step_config(step)

            step_method = getattr(self.pipeline, step_name)        # Get the method
            valid_args = inspect.getargspec(step_method).args[1:]  # See what arguments from task config are applicable
            print valid_args
            # Compute step config
            step_resulting_config = self.config
            step_resulting_config.update(step_config)

            step_arguments = {arg: (step_resulting_config[arg])
                              for arg in valid_args
                              if arg in step_resulting_config}  # Dict with applicable args

            step_method(**step_arguments)  # Run step


class Release(Runner):

    def configure(self):
        self.pipeline = ReleaseWorker(source=self.source)
        self.pipeline.binary_repo = 'Foo'  # This should be an object from some manager class