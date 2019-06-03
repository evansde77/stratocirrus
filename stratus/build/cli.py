#!/usr/bin/env python
"""

development environment builder cli

"""
from arghandler import subcmd, ArgumentHandler

ENV_TYPES = {
    'venv': 'python -m venv',
    'virtualenv': 'virtualenv venv',
    'pipenv': 'pipenv penv',
    'conda': 'conda env'
}



def _add_env_type(p):
    p.add_argument('type', nargs=1, help="environment type", choices=ENV_TYPES.keys())


@subcmd('setup')
def setup_command(parser, context, args):
    _add_env_type(parser)
    parser.add_argument('-p', '--python', default=None, help='python binary to use')
    opts = parser.parse_args(args)
    print(opts)
    print(context)


@subcmd('build', help = 'build')
def new_command(parser, context, args):
    _add_env_type(parser)
    parser.add_argument('-p', '--python', default=None, help='python binary to use')
    opts = parser.parse_args(args)
    print(opts)
    print(context)


@subcmd('run', help='run')
def run_command(parser, context, args):
    _add_env_type(parser)
    opts = parser.parse_known_args(args)
    print(opts)
    forward = context.cargs[1:]
    print(forward)





def main():
    handler = ArgumentHandler(use_subcommand_help=True)
    handler.run()  # echo will be called and 'hello world' will be printed

    # parser = argparse.ArgumentParser(
    #     description='development environment builder command'
    # )
    # parser.add_argument('command', nargs='?')
    # subparsers = parser.add_subparsers(dest='command')
    #
    #
    # new_command = add_new_subcommand(subparsers)
    # #setup_command = add_setup_subcommand(subparsers)
    #
    # opts = parser.parse_args()
    # print(opts)
