import pytest
import mock

from stratus.command_framework import StratusCommand, inspect_command


def test_stratus_command():
    """test instantiation & properties"""
    sc = StratusCommand(
        action='action',
        verb='verb',
        plugin='plugin',
        extras=['--extras', 'things']
    )
    assert sc.command == "stratus verb plugin action"
    assert sc.plugin == 'plugin'
    assert sc.verb == 'verb'
    assert sc.plugin_entry_point == 'stratus_verb'
    assert sc.get_plugins() == {}


def test_inspect_command_action():
    """test inspect command action style"""
    sc = inspect_command(['stratus', 'action'])
    assert sc.action == 'action'
    assert sc.verb is None
    assert sc.plugin is None


def test_inspect_command_verb():
    """test inspect for verb/action"""
    sc = inspect_command(['stratus', 'verb', 'action'])
    assert sc.verb == 'verb'
    assert sc.action == 'action'
    assert sc.plugin is None

def test_inspect_command_verb_plugin():
    """test inspect for verb/plugin/action"""
    sc = inspect_command(['stratus', 'verb', 'plugin', 'action'])
    assert sc.verb == 'verb'
    assert sc.action == 'action'
    assert sc.plugin == 'plugin'
