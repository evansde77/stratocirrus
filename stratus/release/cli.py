#!/usr/bin/env python
"""
release command cli

Maps the release plugin and action to the plugin code and forward rest of options to the plugin
and invoke the action

"""
from argparse import ArgumentParser, Namespace
from stratus.release.model import get_release_models


RELEASE_ACTIONS = {
    'new': 'new release',
    'build': 'build release artifacts',
    'publish': 'publish release',
    'closeout': 'merge/tag/cleanup release'
}


def build_parser():
    """
    set up the argparse parser to extract the plugin and action from the cli args
    as first two positional arguments
    :return: argparse.ArgumentParser instance
    """
    parser = ArgumentParser("release model command suite")
    models = get_release_models()
    parser.add_argument('model', nargs=1, help='release model', choices=models.keys())
    parser.add_argument('action', nargs=1, help='action', choices=RELEASE_ACTIONS.keys())
    return parser


def main():
    """
    main release command

    lookup the release plugin, then delegate to the implementation for the
    action provided

    :return:
    """
    handler = build_parser()
    opts, args = handler.parse_known_args()
    opts.model = opts.model[0]
    opts.action = opts.action[0]
    models = get_release_models()
    m = opts.model
    a = opts.action
    model = models[m]()
    model.configure_parser(a)
    model.run_parser(args)
    action = getattr(model, a)
    action()
