# -*- coding: utf-8 -*-

import unittest2 as unittest

from getopt import GetoptError

from couchapp import dispatch
from couchapp.commands import globalopts
from couchapp.errors import CommandLineError


class DispatchTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_unknown_command(self):
        with self.assertRaises(CommandLineError):
            dispatch._dispatch(['unknown_command'])

        assert dispatch.dispatch(['unknown_command']) == -1

    def test_parseopts_short_flag(self):
        opts = {}
        args = dispatch.parseopts(['-v', 'generate', 'app', 'test-app'], globalopts, opts)
        assert args == ['generate', 'app', 'test-app']
        assert opts['debug'] is None
        assert opts['help'] is None
        assert opts['version'] is None
        assert opts['verbose'] == True
        assert opts['quiet'] is None

    def test_parseopts_long_flag(self):
        opts = {}
        args = dispatch.parseopts(['--version'], globalopts, opts)
        assert args == []
        assert opts['debug'] is None
        assert opts['help'] is None
        assert opts['version'] == True
        assert opts['verbose'] is None
        assert opts['quiet'] is None

    def test_parseopts_invalid_flag(self):
        with self.assertRaises(GetoptError):
            dispatch.parseopts(['-X'], globalopts, {})

        with self.assertRaises(GetoptError):
            dispatch.parseopts(['--unkown'], globalopts, {})

    def test__parse_invalid_flag(self):
        with self.assertRaises(CommandLineError):
            dispatch._parse(['-X'])

        with self.assertRaises(CommandLineError):
            dispatch._parse(['init', '-X'])

        with self.assertRaises(CommandLineError):
            dispatch._parse(['--unkown'])

    def test__parse_help(self):
        cmd, options, cmdoptions, args = dispatch._parse(['help'])
        assert cmd == 'help'

        cmd, options, cmdoptions, args = dispatch._parse([])
        assert cmd == 'help'

        cmd, options, cmdoptions, args = dispatch._parse(['-h'])
        assert cmd == 'help'
        assert options['help'] == True

    def test__parse_subcmd_options(self):
        cmd, options, cmdoptions, args = dispatch._parse(['push', '-b', 'http://localhost'])
        assert cmd == 'push'
        assert cmdoptions['browse'] == True


if __name__ == '__main__':
    unittest.main()
