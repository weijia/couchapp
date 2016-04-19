# -*- coding: utf-8 -*-

from couchapp.generator import init_basic, save_id

from mock import patch


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
