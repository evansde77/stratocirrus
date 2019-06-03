"""
release model API

"""
import argparse
import pkg_resources
from argparse import Namespace

def get_release_models():
    models = {}
    for entry_point in pkg_resources.iter_entry_points('stratus_release_models'):
        models[entry_point.name] = entry_point.load()
    return models





class ReleaseModel(object):


    def __init__(self):
        self.parser = None
        self.subcommand = None
        self.opts = Namespace()
        self.args = []

    def configure_parser(self, action):
        self.parser = argparse.ArgumentParser()
        subparsers = self.parser.add_subparsers(help='action commands', dest='action')
        customizer = getattr(self, f"customize_parser_{action}")
        self.subcommand = subparsers.add_parser(action)
        customizer(self.parser)



    def customize_parser_new(self, p):
        pass

    def customize_parser_build(self, p):
        pass

    def customize_parser_publish(self, p):
        pass

    def customize_parser_closeout(self, p):
        pass

    def run_parser(self, args):
        self.opts = self.parser.parse_args(args)

    def new(self):
        pass

    def build(self):
        pass

    def publish(self):
        pass


    def closeout(self):
        pass
