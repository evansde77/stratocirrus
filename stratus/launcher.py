#!/usr/bin/env python
"""
command launcher/delegator

"""

import sys, os, signal
import subprocess
from stratus.logger import stratus_logger


def python_bin_dir():
    """
    use sys.executable to determine the bin dir
    for the active python.
    """
    return os.path.dirname(sys.executable)


def available_binaries(dirname):
    result = {}
    for b in os.listdir(dirname):
        p = os.path.join(dirname, b)
        if os.path.isfile(p) and os.access(p, os.X_OK):
            result[b] = p
    return result


def install_signal_handlers():
    """
    Need to catch SIGINT to allow the command to be CTRL-C'ed

    """
    def signal_handler(signal, frame):
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)


def run_command(cmd):
    """
    run the delegated command with the CTRL-C signal handler
    in place
    """
    install_signal_handlers()
    return subprocess.call(cmd, shell=False)



class DelegationRule(object):
    """
    Helper to implement delegation to another CLI tool

    :param name: Name of the rule/command to delegate to
    :param command: The name of the command that will be used to delegate to the binary
    :param cd (optional): Boolean indicating that the working dir should be changed
       upon execution
    :param cd_func (optional): Lambda/function to return the directory for the cd operation

    """
    def __init__(self, command=None, name=None, **options):
        self.name = name
        self.command = command
        self.bin = None
        self.cd = options.get('cd', True)
        self.cd_func = lambda: os.path.abspath(os.environ.get('GIT_PREFIX', '.'))


class Delegate(dict):
    """
    Delegate commands from a suite to individual underlying command line
    implementations installed as entrypoints.

    This allows diverse CLI tools to get combined into a suite of commands
    that can be aggregated under eg a git alias.

    :param dirname: Location of binaries for delegation, defaults to python bin dir
    :param num_pop: Number of initial cli args to pop before delegating
    """
    def __init__(self, dirname=None, **rules):
        super(Delegate).__init__()
        for n, r in rules.items():
            if isinstance(r, str):
                self[n] = DelegationRule(name=n, command=r)
            elif isinstance(r, DelegationRule):
                r.name = n
                self[n] = r
            else:
                raise RuntimeError(f"not a Delegation Rule or string: {r}")
        self._dirname = dirname or python_bin_dir()
        self.skip_args = 1

    def __call__(self, *args):
        """
        _operator(*args)_

        Given a set of command line args,

        :param args:
        :return:
        """
        if len(args) == 0 or args[0] in ('-h', '--help'):
            # missing command or help
            print(f"Print out help here")
            sys.exit(0)
        cli_args = list(args)
        command = cli_args[0]
        if command not in self:
            msg = f"Cannot find delegation rule for command: {command}"
            stratus_logger.error(msg)
            sys.exit(1)

        rule = self[command]
        command_alias = rule.command
        map = available_binaries(self._dirname)
        rule.bin = map[command_alias]
        self._run(rule, *cli_args[self.skip_args:])


    def _run(self, rule, *args):

        initial_dir = os.getcwd()
        if rule.cd:
            new_dir = rule.cd_func()
            os.chdir(new_dir)
        try:
            command = [rule.bin]
            command.extend(args)
            exit_code = run_command(command)
        except Exception as ex:
            msg = "Exception Details:\n{}".format(ex)
            stratus_logger.error(msg)
            raise
        finally:
            # always return to previous dir
            if rule.cd:
                os.chdir(initial_dir)
        return exit_code


def main():
    d = Delegate(
        release='stratus-release',
        build=DelegationRule(command='stratus-build'),
        info=DelegationRule(command='stratus-info')
    )
    d(*sys.argv[1:])
