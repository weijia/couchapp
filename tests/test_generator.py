# -*- coding: utf-8 -*-

import tempfile

from couchapp.errors import AppError
from couchapp.generator import copy_helper
from couchapp.generator import find_template_dir, init_basic, save_id

from mock import patch
from nose.tools import raises, with_setup


@patch('couchapp.generator.save_id')
@patch('couchapp.generator.setup_dirs')
@patch('couchapp.generator.setup_dir')
@patch('couchapp.generator.localdoc')
def test_init_basic(localdoc, setup_dir, setup_dirs, save_id):
    init_basic('/mock/app')

    assert setup_dir.called
    assert setup_dirs.called
    assert save_id.called
    assert localdoc.document.called


@patch('couchapp.generator.open')
def test_save_id(open_):
    save_id('/mock/app', 'someid')

    open_.assert_called_with('/mock/app/_id', 'wb')


@patch('couchapp.generator.os.path.isdir', return_value=False)
def test_find_template_dir_not_found(isdir):
    assert find_template_dir() is None
    assert isdir.called


@patch('couchapp.generator.os.path.isdir', return_value=False)
def test_find_template_dir_not_found_raise(isdir):
    @raises(AppError)
    def f():
        find_template_dir(raise_error=True)

    f()
    assert isdir.called


@patch('couchapp.generator.os.path.isdir', return_value=False)
def test_find_template_dir_template_type_error(isdir):
    @raises(AppError)
    def f():
        find_template_dir(tmpl_type='mock_type')

    f()
    assert not isdir.called


@patch('couchapp.generator.user_path', return_value=['/mock/.couchapp'])
@patch('couchapp.generator.os.path.isdir', return_value=True)
def test_find_template_dir_user_dir_first(isdir, user_path):
    ret = find_template_dir()

    assert ret == '/mock/.couchapp/templates/', ret
    assert user_path.called
    assert isdir.called


@patch('couchapp.generator.user_path', return_value=['/mock/.couchapp'])
@patch('couchapp.generator.os.path.isdir', return_value=True)
def test_find_template_dir_user_dir_first_with_type(isdir, user_path):
    ret = find_template_dir(tmpl_type='app')

    assert ret == '/mock/.couchapp/templates/app', ret
    assert user_path.called
    assert isdir.called


@raises(OSError)
def test_copy_helper_invalid_src():
    copy_helper('/mock', '/fake')


@patch('couchapp.generator.copytree')
@patch('couchapp.generator.copy2')
@patch('couchapp.generator.os.listdir', return_value=['foo', 'bar'])
@patch('couchapp.generator.os.path.isdir')
@patch('couchapp.generator.setup_dir')
def test_copy_helper_file_only(setup_dir, isdir, listdir, copy2, copytree):
    def _isdir(p):
        if p == '/mock':
            return True
        return False

    isdir.side_effect = _isdir

    copy_helper('/mock', '/fake')

    assert setup_dir.called
    assert copy2.called
    assert not copytree.called
    copy2.assert_any_call('/mock/foo', '/fake/foo')
    copy2.assert_any_call('/mock/bar', '/fake/bar')


@patch('couchapp.generator.copytree')
@patch('couchapp.generator.copy2')
@patch('couchapp.generator.os.listdir', return_value=['foo', 'bar'])
@patch('couchapp.generator.os.path.isdir', return_value=True)
@patch('couchapp.generator.setup_dir')
def test_copy_helper_dir_only(setup_dir, isdir, listdir, copy2, copytree):
    copy_helper('/mock', '/fake')

    assert setup_dir.called
    assert copytree.called
    assert not copy2.called
    copytree.assert_any_call('/mock/foo', '/fake/foo')
    copytree.assert_any_call('/mock/bar', '/fake/bar')
