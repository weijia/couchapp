# -*- coding: utf-8 -*-

from couchapp.util import rcpath

from mock import patch


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
