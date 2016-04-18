# -*- coding: utf-8 -*-

import shutil
import tempfile
import os

from couchapp.errors import AppError
from couchapp.util import discover_apps, iscouchapp, rcpath, split_path
from couchapp.util import sh_open, remove_comments, is_empty_dir, setup_dir
from couchapp.util import setup_dirs

from mock import patch
from nose.tools import raises


@patch('couchapp.util.user_rcpath')
@patch('couchapp.util._rcpath')
def test_rcpath_cached(_rcpath, user_rcpath):
    '''
    Global ``_rcpath`` is not None already
    '''
    assert _rcpath == rcpath()
    assert not user_rcpath.called


@patch.dict('couchapp.util.os.environ', clear=True)
@patch('couchapp.util.user_rcpath', return_value=['/mock/couchapp.conf'])
def test_rcpath_empty_env(user_rcpath):
    '''
    Empty ``COUCHAPPCONF_PATH``
    '''
    import couchapp.util as util
    util._rcpath = None
    assert rcpath() == ['/mock/couchapp.conf'], rcpath()
    assert user_rcpath.called


@patch.dict('couchapp.util.os.environ',
            {'COUCHAPPCONF_PATH': '/mock:/tmp/fake.conf'})
@patch('couchapp.util.os.listdir')
@patch('couchapp.util.os.path.isdir')
@patch('couchapp.util.user_rcpath')
def test_rcpath_env(user_rcpath, isdir, listdir):
    '''
    With ``COUCHAPPCONF_PATH`` set
    '''
    import couchapp.util as util
    util._rcpath = None

    def _isdir(path):
        return True if path == '/mock' else False

    def _listdir(path):
        return ['foo', 'bar', 'couchapp.conf'] if path == '/mock' else []

    isdir.side_effect = _isdir
    listdir.side_effect = _listdir

    assert rcpath() == ['/mock/couchapp.conf', '/tmp/fake.conf'], rcpath()
    assert not user_rcpath.called


@patch('couchapp.util.os.path.isfile', return_value=True)
def test_iscouchapp(isfile):
    assert iscouchapp('/mock_dir') == True
    isfile.assert_called_with('/mock_dir/.couchapprc')


@patch('couchapp.util.os.listdir', return_value=['foo'])
@patch('couchapp.util.os.path.isdir', return_value=True)
@patch('couchapp.util.iscouchapp', return_value=True)
def test_discover_apps(iscouchapp_, isdir, listdir):
    assert discover_apps('/mock_dir') == ['/mock_dir/foo']
    isdir.assert_called_with('/mock_dir/foo')
    listdir.assert_called_with('/mock_dir')


@patch('couchapp.util.os.listdir', return_value=['foo'])
@patch('couchapp.util.os.path.isdir', return_value=True)
@patch('couchapp.util.iscouchapp', return_value=True)
def test_discover_apps_relative_path(iscouchapp_, isdir, listdir):
    assert discover_apps('mock_dir') == ['mock_dir/foo']
    isdir.assert_called_with('mock_dir/foo')
    listdir.assert_called_with('mock_dir')


@patch('couchapp.util.os.listdir', return_value=['.git', 'foo'])
@patch('couchapp.util.os.path.isdir', return_value=True)
@patch('couchapp.util.iscouchapp', return_value=True)
def test_discover_apps_hidden_file(iscouchapp_, isdir, listdir):
    '''
    Test case for a dir including hidden file
    '''
    assert discover_apps('mock_dir') == ['mock_dir/foo']
    isdir.assert_called_with('mock_dir/foo')
    listdir.assert_called_with('mock_dir')


def test_split_path_rel():
    '''
    Test case for util.split_path with relative path
    '''
    assert split_path('foo/bar') == ['foo', 'bar']


def test_split_path_abs():
    '''
    Test case for util.split_path with abs path
    '''
    path = os.path.realpath('/foo/bar')
    assert split_path(path) == [os.path.realpath('/foo'), 'bar']


def test_sh_open():
    '''
    Test case for ``util.sh_open``
    '''
    out, err = sh_open('echo mock')
    assert out.startswith('mock'), out
    assert not err, err


def test_remove_comments():
    text = '''{
    "mock": 42  // truth
}'''
    expect = '{\n    "mock": 42  \n}'

    ret = remove_comments(text)
    assert ret == expect

    # testing for multiline comments
    text = '''{
    "mock": 42,  // truth
    /* foo
    bar
    */
    "fake": true}'''
    ret = remove_comments(text)
    expect = '{\n    "mock": 42,  \n    \n    "fake": true}'

    assert ret == expect


class test_is_empty_dir_true():
    def setup(self):
        self.tmpdir = tempfile.mkdtemp()

    def test(self):
        assert is_empty_dir(self.tmpdir) is True

    def teardown(self):
        shutil.rmtree(self.tmpdir)


class test_is_empty_dir_false():
    def setup(self):
        self.tmpdir = tempfile.mkdtemp()
        self.tmpfile = tempfile.NamedTemporaryFile(dir=self.tmpdir,
                                                   delete=False)
        self.tmpfile.close()

    def test(self):
        assert is_empty_dir(self.tmpdir) is False

    def teardown(self):
        shutil.rmtree(self.tmpdir)


@patch('couchapp.util.os.mkdir')
def test_setup_dir(mkdir):
    setup_dir('/mock')
    assert mkdir.called


class test_setup_dir_exists():
    def setup(self):
        '''
        /tmpdir/
            *empty*
        '''
        self.tmpdir = tempfile.mkdtemp()

    @patch('couchapp.util.os.mkdir')
    def test(self, mkdir):
        setup_dir(self.tmpdir, require_empty=True)
        assert not mkdir.called

    def teardown(self):
        shutil.rmtree(self.tmpdir)


class test_setup_dir_exists_not_empty():
    def setup(self):
        '''
        /tmpdir/
            tmpfile
        '''
        self.tmpdir = tempfile.mkdtemp()
        self.tmpfile = tempfile.NamedTemporaryFile(dir=self.tmpdir,
                                                   delete=False)
        self.tmpfile.close()

    @raises(AppError)
    def main(self):
        setup_dir(self.tmpdir, require_empty=True)

    @patch('couchapp.util.os.mkdir')
    def test(self, mkdir):
        self.main()
        assert not mkdir.called

    def teardown(self):
        shutil.rmtree(self.tmpdir)


class test_setup_dir_exists_empty_not_required():
    def setup(self):
        '''
        /tmpdir/
            tmpfile
        '''
        self.tmpdir = tempfile.mkdtemp()
        self.tmpfile = tempfile.NamedTemporaryFile(dir=self.tmpdir,
                                                   delete=False)
        self.tmpfile.close()

    @patch('couchapp.util.os.mkdir')
    def test(self, mkdir):
        setup_dir(self.tmpdir, require_empty=False)
        assert not mkdir.called

    def teardown(self):
        shutil.rmtree(self.tmpdir)


class test_setup_dir_exists_not_dir():
    def setup(self):
        '''
        /strangefile
        '''
        self.tmpfile = tempfile.NamedTemporaryFile(delete=True)

    @raises(AppError)
    def main(self):
        setup_dir(self.tmpfile.name)

    @patch('couchapp.util.os.mkdir')
    def test(self, mkdir):
        self.main()
        assert not mkdir.called

    def teardown(self):
        del self.tmpfile


@patch('couchapp.util.setup_dir')
def test_setup_dirs(setup_dir):
    plist = ['/mock', '/fake', '/mock/app', '/42']
    setup_dirs(plist)

    assert setup_dir.called
