"""
cirrus package harness


"""
import os

from stratus.repository import PackageRepo, repo_directory
from stratus.configuration import PackageConfig
from stratus.command_framework import inspect_command




def current_package(dirname=None, command=None, args=None, context=None):
    if dirname is None:
        dirname = repo_directory()
    if args:
        command = inspect_command(args=args, context=context)
    return StratusPackage(package=dirname, command=command)



class StratusPackage(object):
    """
    Helper for dealing with a stratus package which is essentially
    a directory in a repo that contains certain things like a
    setup.cfg and all the little bits that python uses for packaging

    Also provides API helpers into the config files, a git repo helper
    and the various assistants for manipulating common parts of the
    package config
    """

    def __init__(self, repo=None, package=None, command=None):
        self.repo = PackageRepo(repo)
        self.dir = package or os.getcwd()
        self.command = command or inspect_command()
        self._config = None

    @property
    def configuration(self):
        if self._config is None:
            if os.path.exists(self.setup_cfg):
                self._config = PackageConfig()
                self._config.load(self.setup_cfg)
            else:
                self._config = PackageConfig()
        return self._config

    @property
    def setup_cfg(self):
        return os.path.join(self.dir, 'setup.cfg')

    @property
    def setup_py(self):
        return os.path.join(self.dir, 'setup.py')

    @property
    def manifest_in(self):
        return os.path.join(self.dir, 'MANIFEST.in')

    def current_version(self):
        """
        get the current version field from the setup.cfg version field
        wrapped in a PackageVersion helper

        :return: stratus.versions.PackageVersion instance
        """
        return self.configuration.package_version

    def package_name(self):
        return self.configuration.package_name



if __name__ == '__main__':
    cp = current_package()
    print(cp)
    print(cp.dir)
    print(cp.repo)
    print(cp.setup_cfg)
    print(cp.current_version())
