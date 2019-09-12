"""
build command.

Delegates most of the work to builder plugins

"""
import sys

from stratus.package import current_package


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    cp = current_package(
        args=args,
        context=['stratus', 'build']
    )
    plugin_cls = cp.command.fetch_plugin()
    plugin = plugin_cls(cp)
    plugin()




if __name__ == '__main__':
    main(['stratus', 'build', 'venv', 'setup', '--python', 'python3.7', '--name', 'venv'])
    main(['stratus', 'build', 'venv', 'create', '--clean', '--python', 'python3.7', '--name', 'venv'])
    main(['stratus', 'build', 'venv', 'update', '--clean'])
    main(['stratus', 'build', 'venv', 'delete'])
    main(['stratus', 'build', 'venv', 'run' , "python", "src/test/scriptyscript.py"])