#!/usr/bin/env python


from argparse import ArgumentParser
import yaml
import sys
import importlib
from runners import *  # Need to import all runners


def parse_arguments():
    mainparser = ArgumentParser('BSF')
    mainparser.add_argument('runner', help='Runner as specified in tasks.yml')
    mainparser.add_argument('task', help='Task to run as specified in tasks.yml')
    mainparser.add_argument('-s', '--source', default='source', help='Location of source to be build')
    return mainparser.parse_args()


def get_config(cfg):
    with open(cfg, 'r') as stream:
        return yaml.load(stream)


def get_runner_class(runner, module='runners'):
    """
    Returns the runner class specified byt the runner name
    :param runner: string with runner class name
    :param module: module where to search for runner classes
    :return: runner class
    """
    runners = inspect.getmembers(sys.modules[module], inspect.isclass)  # Returns classes in module
    runner_list = dict()
    for rn in runners:
        runner_class_name, runner_class_object = rn
        runner_name = str(runner_class_name.lower())  # Convert class name to lowercase, maybe better to use a class prop
        # dict with lower case task name and proper class name capitalization
        runner_list[runner_name] = runner_class_name
    return getattr(importlib.import_module(module), runner_list[runner])


def get_resulting_task_config(default_tasks, runner_config, task_config):
    """
    Returns the  resulting by overriding:
    - default is overriden by runner
    - runner is overriden by task
    :param default_tasks: global tasks definition and config
    :param runner_config: current runner config
    :param task_config: current task config
    :return: dictionary containing the resulting config
    """
    resulting_config = default_tasks
    resulting_config.update(runner_config)
    resulting_config.update(task_config)
    return resulting_config


def main():
    args = parse_arguments()
    runner = args.runner
    task = args.task
    default_tasks = get_config('tasks.yml')

    print 'Running %s:%s' % (runner, task)

    runner_config = dict()
    task_config = dict()

    if runner not in default_tasks:
        print 'ERROR: runner not defined in tasks'
        sys.exit(-1)
    if task not in default_tasks[runner]['tasks']:
        print 'ERROR task %s not defined in runner %s' % (task, runner)
        sys.exit(-1)

    task_definition = {tsk: default_tasks[runner]['tasks'][tsk] for tsk in default_tasks[runner]['tasks'] if tsk == task}

    if 'config' in default_tasks[runner]:
        runner_config = default_tasks[runner]['config']

    if 'config' in default_tasks[runner]['tasks'][task]:
        task_config = default_tasks[runner]['tasks'][task]['config']

    runner_class = get_runner_class(runner)
    rnr = runner_class(args.source, task_definition, runner_config, task_config)
    rnr.do(task)

if __name__ == '__main__':
    main()
