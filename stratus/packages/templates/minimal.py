
"""
minimal template handler installs:

setup.cfg
setup.py
MANIFEST.in
README.md
GH standard gitignore file
requirements installed via install_requires


"""
import os
import getpass

from stratus.packages.template import PackageTemplate
from stratus.package import current_package


SETUP_CFG=\
"""
[metadata]
name = {package}
version = {version}
author = {author}
author-email = {email}
home-page = {url}
description = {description}
long-description = file: README.md
license = MIT
license-file = COPYING
platform = any
keywords = {keywords}
classifiers =
  {classifiers}
    
[options]
zip_safe = false
include_package_data = true
packages = {code_package}
test_suite = tests/unit
setup_requires =
    setuptools>38.3.0
install_requires =
    {requirements}
tests_require =
    tox
    mock
    pytest


[stratus.branches]
remote={git_remote}
master={git_master}
develop={git_develop}
release_prefix={release_prefix}
feature_prefix={feature_prefix}

"""

SETUP_PY=\
"""
#!/usr/bin/env python
#
# stratus-generated setup.py using Minimal template
# 
#

from setuptools import setup

setup()

"""


class Minimal(PackageTemplate):
    """
    minimal package setup template

    """

    def customize_parser_new(self, p):
        p.add_argument('--repo', '-r', help="Path to repo", default=None)
        p.add_argument('--git-master', default='master')
        p.add_argument('--git-remote', default='origin')
        p.add_argument('--git-develop', default='develop')
        p.add_argument('--version', '-v', default='0.0.0', help='initial version number')
        p.add_argument('--package', '-p', required=True, help='pypi package name')
        p.add_argument('--namespace', '-n', default=None, help='create package namespace with __init__.py using this name')
        p.add_argument('--author', '-a', default=getpass.getuser())
        p.add_argument('--url', default=None, help='package URL or webpage')
        p.add_argument('--email', default=f"{getpass.getuser()}.@gmail.com")
        p.add_argument('--description', default="", help="short description of package")
        p.add_argument('--requirements', nargs='+', default=[], help='initial list of dependencies for install_requires')



    def new(self):
        repo = self.opts.repo or os.getcwd()
        pkg = current_package(repo)



        # init repo branches
        for br in (self.opts.git_master, self.opts.git_develop):
            pkg.repo.initialize_branch(br, self.opts.git_remote)


        # create directories


        # create files


