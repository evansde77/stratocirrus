
import configparser

from stratus.versions import PackageVersion



class ConfSection(object):

    def __init__(self, name, parser):
        self._name = name



class PackageConfig(object):


    def __init__(self):
        self.conf = None
        self.parser = None,

    def load(self, filename):
        """
        read config from disk

        """
        self.parser = configparser.RawConfigParser()
        self.parser.read(filename)
        for section in self.parser.sections():
            self.setdefault(section, {})
            for option in self.parser.options(section):
                self[section].setdefault(
                    option,
                    self.parser.get(section, option)
                )

    def save(self, filename):
        """
        save this config file
        :param filename:
        :return:
        """
        with open(filename, 'w') as handle:
            self.parser.write(handle)

    def has_section(self, section):
        return section in self

    def add_section(self, section):
        if not self.has_section(section):
            self[section] = {}
            self.parser.add_section(section)


class Configuration(dict):
    """
    Wrapper and API around the setup.cfg file used to manipulate package settings

    """

    def __init__(self):
        super(Configuration, self).__init__(self)
        self.parser = None

    def load(self, filename):
        """
        read config from disk

        """
        self.parser = configparser.RawConfigParser()
        self.parser.read(filename)
        for section in self.parser.sections():
            self.setdefault(section, {})
            for option in self.parser.options(section):
                self[section].setdefault(
                    option,
                    self.parser.get(section, option)
                )

    def save(self, filename):
        """
        save this config file
        :param filename:
        :return:
        """
        with open(filename, 'w') as handle:
            self.parser.write(handle)

    def has_section(self, section):
        return section in self

    def add_section(self, section):
        if not self.has_section(section):
            self[section] = {}
            self.parser.add_section(section)

    def get_param(self, section, param, default=None):
        """
        _get_param_

        convenience param getter with section, param name and
        optional default to avoid key errors
        """
        if section not in self:
            raise KeyError('section {0} not found'.format(section))
        return self[section].get(param, default)

    def package_version(self):
        return self.get(self._PACKAGE_SECTION, {}).get('version')

    def package_name(self):
        return self.get(self._PACKAGE_SECTION, {}).get('name')

    def organisation_name(self):
        return self.get(self._PACKAGE_SECTION, {}).get('organization')

    def author_email(self):
        return self.get(self._PACKAGE_SECTION, {}).get('author_email')

    def gitflow_branch_name(self):
        return self.get(self._GITFLOW_SECTION, {}).get('develop_branch', 'develop')

    def gitflow_master_name(self):
        return self.get(self._GITFLOW_SECTION, {}).get('master_branch', 'master')

    def gitflow_origin_name(self):
        return self.get(self._GITFLOW_SECTION, {}).get('remote_origin', 'origin')

    def gitflow_feature_prefix(self):
        return self.get(self._GITFLOW_SECTION, {}).get('feature_branch_prefix', 'feature/')

    def gitflow_release_prefix(self):
        return self.get(self._GITFLOW_SECTION, {}).get('release_branch_prefix', 'release/')

    def test_where(self, suite):
        return self.test_suite(suite).get('where')

    def test_mode(self, suite):
        return self.test_suite(suite).get('mode')

