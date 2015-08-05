# -*- coding: utf-8 -*-

import unittest2 as unittest

from couchapp import dispatch
from couchapp.errors import CommandLineError


class DispatchTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_unknown_command(self):
        with self.assertRaises(CommandLineError):
            dispatch._dispatch(['unknown_command'])


if __name__ == '__main__':
    unittest.main()
