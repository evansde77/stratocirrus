"""
cirrus package harness


"""
import os

from stratus.repository import PackageRepo
from stratus.configuration import Configuration



def current_package(dirname=None):
    return StatusPackage(dirname)


class StatusPackage(object):


    def __init__(self, repo=None, package=None):
        self.repo = PackageRepo(repo)
        self.dir = package or os.getcwd()
        self._config = None

    @property
    def configuration(self):
        if self._config is None:
            if os.path.exists(self.setup_cfg):
                self._config = Configuration()
                self._config.load(self.setup_cfg)
            else:
                self._config = Configuration()
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
        :return:
        """
