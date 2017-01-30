# -*- coding: utf-8 -*-

from couchapp.errors import AppError
from couchapp.generator import copy_helper, find_template_dir
from couchapp.generator import init_basic, init_template, save_id
from couchapp.generator import generate, generate_vendor, generate_function

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


@patch('couchapp.generator.copy_helper')
def test_init_template_invalid_name(copy_helper):
    @raises(AppError)
    def f():
        init_template('/mock', template='app')

    @raises(AppError)
    def g():
        init_template('/mock', template='functions')

    @raises(AppError)
    def h():
        init_template('/mock', template='vendor')

    f()
    g()
    h()
    assert not copy_helper.called


@patch('couchapp.generator.localdoc')
@patch('couchapp.generator.save_id')
@patch('couchapp.generator.setup_dirs')
@patch('couchapp.generator.find_template_dir')
@patch('couchapp.generator.copy_helper')
def test_init_template_default(copy_helper, find_template_dir, setup_dirs,
                               save_id, localdoc):
    def _find_dir(*args, **kwargs):
        if (args, kwargs) == (('default', 'app'), dict(raise_error=True)):
            # we will copy ``tempaltes/app`` dir
            # and if the template not found in any paths,
            # we will raise error.
            return '/mock/.couchapp/templates/app'
        elif (args, kwargs) == (('default',), dict(tmpl_type='vendor')):
            # we will copy vendor dir
            return '/mock/.couchapp/templates/vendor'
        else:
            raise AssertionError('invalid call {}'.format((args, kwargs)))

    find_template_dir.side_effect = _find_dir

    init_template('/fake', template='default')

    assert copy_helper.called
    assert find_template_dir.called
    assert setup_dirs.called
    assert save_id.called
    assert localdoc.document.called


@patch('couchapp.generator.localdoc')
@patch('couchapp.generator.save_id')
@patch('couchapp.generator.setup_dirs')
@patch('couchapp.generator.find_template_dir')
@patch('couchapp.generator.copy_helper')
def test_init_template_with_tmpl_name(copy_helper, find_template_dir,
                                      setup_dirs, save_id, localdoc):
    def _find_dir(*args, **kwargs):
        if (args, kwargs) == (('default', 'app'), dict(raise_error=True)):
            # we will copy ``tempaltes/app`` dir
            # and if the template not found in any paths,
            # we will raise error.
            return '/mock/.couchapp/templates/app'
        elif (args, kwargs) == (('default',), dict(tmpl_type='vendor')):
            # we will copy vendor dir
            return None
        elif (args, kwargs) == (tuple(), dict(tmpl_type='vendor')):
            # ``vendor`` not found in the template set
            # consider the case of fallback to ``default``
            return '/opt/couchapp/templates/vendor'
        else:
            raise AssertionError('invalid call {}'.format((args, kwargs)))

    find_template_dir.side_effect = _find_dir

    init_template('/fake', template='default')

    assert copy_helper.called
    assert find_template_dir.called
    assert setup_dirs.called
    assert save_id.called
    assert localdoc.document.called


@patch('couchapp.generator.generate_function')
@patch('couchapp.generator.generate_vendor')
def test_generate_dispatch_function(gen_vendor, gen_func):
    generate('/mock/app', 'view', 'mock_view', template='default')

    assert gen_func.called
    assert not gen_vendor.called


@raises(AppError)
@patch('couchapp.generator.generate_function')
@patch('couchapp.generator.generate_vendor')
def test_generate_invalid_functions(gen_vendor, gen_func):
    generate('/mock/app', 'strange', 'mock_func', template='default')

    assert not gen_func.called
    assert not gen_vendor.called


@patch('couchapp.generator.generate_function')
@patch('couchapp.generator.generate_vendor')
def test_generate_dispatch_to_vendor(gen_vendor, gen_func):
    generate('/mock/app', 'vendor', 'myvendor', template='default')

    assert not gen_func.called
    assert gen_vendor.called


@patch('couchapp.generator.copy_helper')
@patch('couchapp.generator.setup_dir')
@patch('couchapp.generator.find_template_dir', return_value='/vendor/boostrap')
def test_generate_vendor(find_template_dir, setup_dir, copy_helper):
    generate_vendor('/app', 'boostrap')

    assert find_template_dir.called
    setup_dir.assert_called_with('/app/vendor')
    copy_helper.assert_called_with('/vendor/boostrap', '/app/vendor')


@patch('couchapp.generator.copy2')
@patch('couchapp.generator.setup_dir')
@patch('couchapp.generator.find_template_dir', return_value='/funcs/view')
def test_generate_function_view(find_template_dir, setup_dir, copy2):
    generate_function('/app', 'view', 'mock')

    assert find_template_dir.called
    setup_dir.assert_called_with('/app/views/mock', require_empty=True)
    copy2.assert_any_call('/funcs/view/map.js', '/app/views/mock/map.js')
    copy2.assert_any_call('/funcs/view/reduce.js', '/app/views/mock/reduce.js')


@patch('couchapp.generator.copy2')
@patch('couchapp.generator.setup_dir')
@patch('couchapp.generator.find_template_dir', return_value='/funcs')
def test_generate_function_list(find_template_dir, setup_dir, copy2):
    generate_function('/app', 'list', 'mock')

    assert find_template_dir.called
    setup_dir.assert_called_with('/app/lists', require_empty=False)
    copy2.assert_called_with('/funcs/list.js', '/app/lists/mock.js')


@patch('couchapp.generator.copy2')
@patch('couchapp.generator.setup_dir')
@patch('couchapp.generator.find_template_dir', return_value='/funcs')
def test_generate_function_user_func(find_template_dir, setup_dir, copy2):
    generate_function('/app', 'function', 'mock')

    assert find_template_dir.called
    setup_dir.assert_called_with('/app', require_empty=False)
    copy2.assert_called_with('/funcs/mock.js', '/app/mock.js')


@patch('couchapp.generator.copy2')
@patch('couchapp.generator.setup_dir')
@patch('couchapp.generator.find_template_dir', return_value='/funcs')
def test_generate_function_spatial(find_template_dir, setup_dir, copy2):
    generate_function('/app', 'spatial', 'mock')

    assert find_template_dir.called
    setup_dir.assert_called_with('/app/spatial', require_empty=False)
    copy2.assert_called_with('/funcs/spatial.js', '/app/spatial/mock.js')


@patch('couchapp.generator.copy2')
@patch('couchapp.generator.setup_dir')
@patch('couchapp.generator.find_template_dir', return_value='/funcs')
def test_generate_function_validate_doc(find_template_dir, setup_dir, copy2):
    generate_function('/app', 'validate_doc_update', 'mock')

    assert find_template_dir.called
    setup_dir.assert_called_with('/app', require_empty=False)
    copy2.assert_called_with('/funcs/validate_doc_update.js',
                             '/app/validate_doc_update.js')


@raises(AppError)
@patch('couchapp.generator.copy2')
@patch('couchapp.generator.setup_dir')
@patch('couchapp.generator.find_template_dir', return_value='/funcs')
def test_generate_function_unkown(find_template_dir, setup_dir, copy2):
    generate_function('/app', 'magic', 'mock')

    assert find_template_dir.called
    assert not setup_dir.called
    assert not copy2.called
