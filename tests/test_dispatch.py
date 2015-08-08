# -*- coding: utf-8 -*-

from getopt import GetoptError

from couchapp import dispatch
from couchapp.commands import globalopts
from couchapp.errors import AppError, CommandLineError
from nose.tools import assert_raises
from mock import patch


def test_parseopts_short_flag():
    opts = {}
    args = dispatch.parseopts(['-v', 'generate', 'app', 'test-app'], globalopts, opts)
    assert args == ['generate', 'app', 'test-app']
    assert opts['debug'] is None
    assert opts['help'] is None
    assert opts['version'] is None
    assert opts['verbose'] == True
    assert opts['quiet'] is None


def test_parseopts_long_flag():
    opts = {}
    args = dispatch.parseopts(['--version'], globalopts, opts)
    assert args == []
    assert opts['debug'] is None
    assert opts['help'] is None
    assert opts['version'] == True
    assert opts['verbose'] is None
    assert opts['quiet'] is None


def test_parseopts_invalid_flag():
    with assert_raises(GetoptError):
        dispatch.parseopts(['-X'], globalopts, {})

    with assert_raises(GetoptError):
        dispatch.parseopts(['--unkown'], globalopts, {})


def test_parseopts_list_option():
    listopts = [('l', 'list', [], 'Test for list option')]
    opts = {}
    dispatch.parseopts(['-l', 'foo', '-l', 'bar'], listopts, opts)
    assert opts['list'] == ['foo', 'bar']


def test_parseopts_int_option():
    intopts = [('i', 'int', 100, 'Test for int option')]
    opts = {}
    dispatch.parseopts(['-i', '200'], intopts, opts)
    assert opts['int'] == 200


def test_parseopts_str_option():
    stropts = [('s', 'str', '', 'Test for int option')]
    opts = {}
    dispatch.parseopts(['-s', 'test'], stropts, opts)
    assert opts['str'] == 'test'


def test__parse_invalid_flag():
    with assert_raises(CommandLineError):
        dispatch._parse(['-X'])

    with assert_raises(CommandLineError):
        dispatch._parse(['init', '-X'])

    with assert_raises(CommandLineError):
        dispatch._parse(['--unkown'])


def test__parse_help():
    cmd, options, cmdoptions, args = dispatch._parse(['help'])
    assert cmd == 'help'

    cmd, options, cmdoptions, args = dispatch._parse([])
    assert cmd == 'help'

    cmd, options, cmdoptions, args = dispatch._parse(['-h'])
    assert cmd == 'help'
    assert options['help'] == True


def test__parse_subcmd_options():
    cmd, options, cmdoptions, args = dispatch._parse(['push', '-b', 'http://localhost'])
    assert cmd == 'push'
    assert cmdoptions['browse'] == True


def test__dispatch_debug():
    assert dispatch._dispatch(['-d']) == 0


def test__dispatch_help():
    assert dispatch._dispatch(['-h']) == 0


def test__dispatch_verbose():
    assert dispatch._dispatch(['-v']) == 0


def test__dispatch_version():
    assert dispatch._dispatch(['--version']) == 0


def test__dispatch_quiet():
    assert dispatch._dispatch(['-q']) == 0


def test__dispatch_unknown_command():
    with assert_raises(CommandLineError):
        dispatch._dispatch(['unknown_command'])


@patch('couchapp.dispatch.logger')
@patch('couchapp.dispatch._dispatch')
def test_dispatch_AppError(_dispatch, logger):
    args = ['strange']
    _dispatch.side_effect = AppError('some error')

    assert dispatch.dispatch(args) == -1
    _dispatch.assert_called_with(args)


@patch('couchapp.dispatch.logger')
@patch('couchapp.dispatch._dispatch')
def test_dispatch_CLIError(_dispatch, logger):
    '''
    Test case for CommandLineError
    '''
    args = ['strange']
    _dispatch.side_effect = CommandLineError('some error')

    assert dispatch.dispatch(args) == -1
    _dispatch.assert_called_with(args)


@patch('couchapp.dispatch.logger')
@patch('couchapp.dispatch._dispatch')
def test_dispatch_KeyboardInterrupt(_dispatch, logger):
    '''
    Test case for KeyboardInterrupt
    '''
    args = ['strange']
    _dispatch.side_effect = KeyboardInterrupt()

    assert dispatch.dispatch(args) == -1
    _dispatch.assert_called_with(args)


@patch('couchapp.dispatch.logger')
@patch('couchapp.dispatch._dispatch')
def test_dispatch_other_error(_dispatch, logger):
    '''
    Test case for general Exception
    '''
    args = ['strange']
    _dispatch.side_effect = Exception()

    assert dispatch.dispatch(args) == -1
    _dispatch.assert_called_with(args)
