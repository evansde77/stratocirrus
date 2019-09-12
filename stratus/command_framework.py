"""
Implement a base and helper setup for doing multi-command entry points

like:

stratus <opts>
stratus verb <opts>
stratus verb action <opts>
stratus verb plugin action <opts>

to cover some of the boiler plate needed for setting up commands

"""
import sys
import argparse
import pkg_resources



def inspect_command(args=None, context=None):
    """
    util to parse command line args looking for positional args that
    match verb/plugin/action style commands and returns a StratusCommand
    instance

    :param args: Command line args "stratus etc"
    :return: StratusCommand instance
    """
    if args is None:
        args = sys.argv
    if context is not None:
        args = context + args
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("stratus", default='stratus')
    p.add_argument("one", default=None, nargs='?')
    p.add_argument("two", default=None, nargs='?')
    p.add_argument("three", default=None, nargs='?')
    opts, everything_else = p.parse_known_args(args)

    if all([opts.one is not None, opts.two is None, opts.three is None]):
        return StratusCommand(
            action=opts.one,
            verb=None,
            plugin=None,
            extras=everything_else
        )
    if all([opts.one is not None, opts.two is not None, opts.three is None]):
        return StratusCommand(
            action=opts.two,
            verb=opts.one,
            plugin=None,
            extras=everything_else
        )
    if all([opts.one is not None, opts.two is not None, opts.three is not None]):
        return StratusCommand(
            action=opts.three,
            verb=opts.one,
            plugin=opts.two,
            extras=everything_else
        )




class StratusCommand:
    """
    All the args, settings and defaults for a given command


    """
    def __init__(self, verb=None, plugin=None, action=None, extras=None):
        self._verb = verb
        self._plugin = plugin
        self._action = action
        self._opts = [] or extras

    @property
    def command(self):
       return ' '.join(x for x in ['stratus', self._verb, self._plugin, self._action] if x is not None)


    @property
    def verb(self):
        return self._verb

    @property
    def plugin(self):
        return self._plugin

    @property
    def action(self):
        return self._action

    @property
    def plugin_entry_point(self):
        if self._plugin is None:
            return None
        return f"stratus_{self.verb}"

    @property
    def opts(self):
        return self._opts

    def get_plugins(self):
        """
        look up any available entry point plugins for this command using
        the plugin name based on the command pattern

        :return: dict of plugin classes found
        """
        plugins = {}
        for entry_point in pkg_resources.iter_entry_points(self.plugin_entry_point):
            plugins[entry_point.name] = entry_point.load()
        return plugins

    def fetch_plugin(self):
        plugs = self.get_plugins()
        if self.plugin not in plugs:
            raise RuntimeError(f"No plugin named {self.plugin} found in entrypoint: {self.plugin_entry_point}")
        return plugs[self.plugin]



if __name__ == '__main__':
    sc = inspect_command(['stratus', 'build', 'venv', 'setup'])
    print(sc.command)
    sc = inspect_command(['build', 'venv', 'setup'], context=['stratus'])
    print(sc.command)
    sc = inspect_command(['venv', 'setup'], context=['stratus', 'build'])
    print(sc.command)

