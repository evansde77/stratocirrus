"""
command line interface for plugin driven package command


"""

from argparse import ArgumentParser, Namespace
from stratus.packages.template import get_package_templates


PACKAGE_ACTIONS = {
    'new': 'new package from template',
    'docker': 'new docker container template',
    'helm': 'new helm chart template'
}


def build_parser():
    """
    set up the argparse parser to extract the plugin and action from the cli args
    as first two positional arguments
    :return: argparse.ArgumentParser instance
    """
    parser = ArgumentParser("package template command suite")
    templates = get_package_templates()
    parser.add_argument('template', nargs=1, help='package template handler', choices=templates.keys())
    parser.add_argument('action', nargs=1, help='action', choices=PACKAGE_ACTIONS.keys())
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
    opts.template = opts.template[0]
    opts.action = opts.action[0]
    templates = get_package_templates()
    t = opts.template
    a = opts.action
    template = templates[t]()
    template.configure_parser(a)
    template.run_parser(args)
    action = getattr(template, a)
    action()
