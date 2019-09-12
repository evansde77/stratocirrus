
import semver
import datetime


def today():
    return int(datetime.date.today().strftime('%Y%m%d'))


def make_package_version(v):
    """
    helper to create a PackageVersion instance from the raw config
    string

    :param v: version string
    :return: PackageVersion instance
    """
    pv = PackageVersion()
    pv.parse_version(v)
    return pv


class PackageVersion(dict):


    def __init__(self, v=None, major=None, minor=None, micro=None, build=None, prerelease=None):
        super(PackageVersion, self).__init__()
        self.pre_token = 'pre'
        self.build_token = 'build'
        self['major'] = major
        self['minor'] = minor
        self['patch'] = micro
        self['build'] = build
        self['prerelease'] = prerelease
        if v:
            self.parse_version(v)

    def parse_version(self, v):
        self.update(semver.parse(v))

    def __str__(self):
        pre = None
        build = None
        if self['prerelease']:
            pre = f"{self.pre_token}.{self['prerelease']}"
        if self['build']:
            build = f"{self.build_token}.{self['build']}"
        v = semver.format_version(
            self.major,
            self.minor,
            self.patch,
            prerelease=self['prerelease'],
            build=self['build']
        )
        return v

    def _version_info(self):
        return semver.parse_version_info(str(self))

    @property
    def major(self):
        return self['major']

    @major.setter
    def major(self, x):
        self['major'] = x

    @property
    def minor(self):
        return self['minor']

    @minor.setter
    def minor(self, x):
        self['minor'] = x

    @property
    def micro(self):
        return self['patch']

    @micro.setter
    def micro(self, x):
        self['patch'] = x

    @property
    def patch(self):
        return self['patch']

    @patch.setter
    def patch(self, x):
        self['patch'] = x


    @property
    def pre(self):
        return self['prerelease']

    @pre.setter
    def pre(self, x):
        self['prerelease'] = x

    @property
    def build(self):
        return self['build']

    @build.setter
    def build(self, x):
        self['build'] = x

    def bump_major(self):
        v = semver.bump_major(str(self))
        self.parse_version(v)
        return v

    def bump_minor(self):
        v = semver.bump_minor(str(self))
        self.parse_version(v)
        return v

    def bump_micro(self):
        return self.bump_patch()

    def bump_patch(self):
        v = semver.bump_patch(str(self))
        self.parse_version(v)
        return v

    def bump_pre(self, token=None):
        v = semver.bump_prerelease(str(self), token=self.pre_token)
        self.parse_version(v)
        return v

    def bump_build(self, token=None):
        if token:
            self.build_token = token
        v = semver.bump_build(str(self), token=self.build_token)
        self.parse_version(v)
        return v

    def finalize(self):
        return semver.finalize_version(str(self))

    def new_dev_release(self):
        v = self.bump_build(token='dev')
        return v

    def new_dated_release(self, date_id=None):
        if date_id is None:
            date_id = today()
        self['build'] = f"date.{date_id}"
        return str(self)





if __name__ == '__main__':
    v1 = PackageVersion("1.2.3")
    v2 = PackageVersion("3.4.5-pre.2")
    v3 = PackageVersion(major=2, minor=3, micro=1)
    print(v1.major, v1.minor, v1.micro)
    print(v2.major, v2.minor, v2.micro, v2.pre, v2.build)
    print(v2.build)
    v2.bump_major()
    print(v2.major)
    print(v2.minor)
    print(v2.micro)
    print(v2.finalize())
    print(today())
    print(v2.new_dated_release())
    print(v3.new_dev_release())










