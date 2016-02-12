import os
import sys

from test_cli import CliTestCase as _CliTestCase

from nose.plugins.skip import SkipTest


if sys.platform != 'win32':
    raise SkipTest('windows only testing')


class WinExeTestCase(_CliTestCase):

    def __init__(self, *args, **kwargs):
        super(WinExeTestCase, self).__init__(*args, **kwargs)

        # check for executable
        self.exe

    @property
    def exe(self):
        exe = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                           '..', 'dist', 'couchapp.exe')
        if not os.path.exists(exe):
            raise SkipTest('Windows standalone executable not found '
                           'in {0}'.format(exe))
        return exe

    @property
    def cmd(self):
        return 'cd {tempdir} && {exe}'.format(
            tempdir=self.tempdir, exe=self.exe)
