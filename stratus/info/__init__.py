"""
stratus info command


"""
import sys
import json
import argparse


import stratus
from stratus.command_framework import inspect_command
from stratus.package import current_package
from stratus.logger import stratus_logger


def info_parser(args):
    p = argparse.ArgumentParser("stratus info command")
    p.add_argument('--version', default=False, action='store_true')
    p.add_argument('--package', default=False, action='store_true')
    p.add_argument('--stratus-version', default=False, action='store_true')
    p.add_argument('--format', choices=('json', 'logger'), default='logger')
    opts = p.parse_args(args)
    return opts


def version_info():
    p = current_package()
    v = str(p.current_version())
    return {"package_version": v}

def stratus_version():
    return {"stratus_version": stratus.__version__}

def package_name():
    p = current_package()
    return {"package_name": p.package_name()}


def format_logger(resp):
    stratus_logger.info("stratus info:")
    for k,v in resp.items():
        stratus_logger.info(f"{k}={v}")

def format_json(resp):
    data = {"stratus_info": resp}
    msg = json.dumps(data, indent=2)
    sys.stdout.write(f"{msg}")


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    sc = inspect_command(
        args,
        context=['stratus', 'info']
    )
    opts = info_parser(sc._opts)
    resp = {}
    if opts.version:
        resp.update(version_info())
    if opts.stratus_version:
        resp.update(stratus_version())
    if opts.package:
        resp.update(package_name())

    if opts.format == 'json':
        format_json(resp)
    else:
        format_logger(resp)

