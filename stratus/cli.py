#!/usr/bin/env python
"""stratus

Usage:
  stratus --version
  stratus build new --type=<t>
  stratus build setup --type=<t>
  stratus build clean
  stratus build (-h | --help)
  stratus release new (--micro | --minor | --major)
  stratus release build
  stratus release upload -r=<r>
  stratus release merge --cleanup

Options:
  -h --help     Show this screen.
  --version     Show version.
  --type=<t>    type of environment builder


"""
from docopt import docopt

def main():
    arguments = docopt(__doc__, version='stratus 1.0')
    print(arguments)

