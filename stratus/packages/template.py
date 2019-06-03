import argparse
import pkg_resources
from argparse import Namespace


def get_package_templates():
    models = {}
    for entry_point in pkg_resources.iter_entry_points('stratus_package_templates'):
        models[entry_point.name] = entry_point.load()
    return models


class PackageTemplate(object):


    def __init__(self):
        self.parser = None
        self.subcommand = None
        self.opts = Namespace()
        self.args = []

    def configure_parser(self, action):
        self.parser = argparse.ArgumentParser()
        subparsers = self.parser.add_subparsers(help='template commands', dest='template')
        customizer = getattr(self, f"customize_parser_{action}", lambda x: x)
        self.subcommand = subparsers.add_parser(action)
        customizer(self.parser)

    def run_parser(self, args):
        self.opts = self.parser.parse_args(args)