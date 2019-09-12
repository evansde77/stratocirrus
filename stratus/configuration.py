
import configparser

from stratus.versions import make_package_version



class PackageConfig(dict):


    def __init__(self):
        self.conf = None
        self.parser = None
        self.loaded = False

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
        self.loaded = True

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

    def sections(self):
        return list(self.keys())

    def get_section(self, section, defaults=None):
        """
        get section as a dict, using default settings
        from the dictionary provided

        :param section: name of section to get
        :param defaults: dict of default key:values
        :return: dict mashup of defaults and anything from the config section
          overlaying those defaults
        """
        results = {}
        if defaults:
            results.update(defaults)
        if self.has_section(section):
            results.update(self[section])
        return results

    def parameters(self, section):
        if not self.has_section(section):
            return []
        return list(self[section].keys())

    def get(self, section, param):
        return super().get(section, {}).get(param)

    def get_as_type(self, section, parameter, make_type=str, allow_none=True):
        val = self.get(section, parameter)
        if val is None and allow_none:
            return val
        return make_type(val)



    @property
    def package_version(self):
        return self.get_as_type('metadata', 'version', make_package_version, allow_none=False)

    @property
    def package_name(self):
        return self.get_as_type('metadata', 'name', allow_none=False)



if __name__ == '__main__':
    c = PackageConfig()
    c.load('/Users/devans/PycharmProjects/stratocirrus/setup.cfg')
    print(c.sections())
    print(c.parameters('metadata'))
    pv = c.get_as_type('metadata', 'version', make_package_version)
    print(pv)
    print(c.package_name)
