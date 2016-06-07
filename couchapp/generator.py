# -*- coding: utf-8 -*-
#
# This file is part of couchapp released under the Apache 2 license.
# See the NOTICE for more information.

from __future__ import with_statement

import logging
import os
import sys

from shutil import Error, copy2, copytree

from couchapp import localdoc
from couchapp.errors import AppError
from couchapp.util import is_py2exe, is_windows, relpath, setup_dir, user_path
from couchapp.util import setup_dirs

__all__ = ["init_basic", "init_template", "generate_function", "generate"]

logger = logging.getLogger(__name__)

DEFAULT_APP_TREE = (
    '_attachments',
    'filters',
    'lists',
    'shows',
    'updates',
    'views',
)

TEMPLATE_TYPES = (
    'app',
    'functions',
    'vendor',
)


def init_basic(path):
    '''
    Generate a basic CouchApp which contain following files::

        /path/
            .couchapprc
            .couchappignore
            _attachments/
            lists/
            shows/
            updates/
            views/

    .. versionadded:: 1.1
    '''
    setup_dir(path, require_empty=True)
    setup_dirs(os.path.join(path, n) for n in DEFAULT_APP_TREE)

    save_id(path, '_design/{0}'.format(os.path.split(path)[-1]))
    localdoc.document(path, create=True)


def init_template(path, template='default'):
    '''
    Generates a CouchApp via template

    :param str path: the app dir
    :param str template: the templates set name. In following example, it is
                         ``mytmpl``.

    We expect template dir has following structure::

        templates/
            app/
            functions/
            vendor/

            mytmpl/
                app/
                functions/
                vendor/

            vuejs/
                myvue/
                    app/
                    functions/
                    vendor/
                vueform/
                    app/
                    functions/
                    vendor/

    The ``templates/app`` will be used as default app template.
    ``templates/functions`` and ``templates/vender`` are default, also.

    And we can create a dir ``mytmpl`` as custom template set.
    The template set name can be nested, e.g. ``vuejs/myvue``.

    ..versionadded:: 1.1
    '''
    if template in TEMPLATE_TYPES:
        raise AppError('template name connot be {0}.'.format(TEMPLATE_TYPES))

    tmpl_name = os.path.normpath(template) if template else ''

    # copy ``<template set>/app``
    src_dir = find_template_dir(tmpl_name, 'app', raise_error=True)
    copy_helper(src_dir, path)

    # construct basic dirs
    setup_dirs((os.path.join(path, n) for n in DEFAULT_APP_TREE),
               require_empty=False)

    # add vendor
    src_dir = find_template_dir(tmpl_name, tmpl_type='vendor')
    if src_dir is None:
        logger.debug('vendor not found in template set "{0}". '
                     'fallback to default vendor.'.format(tmpl_name))
        src_dir = find_template_dir(tmpl_type='vendor')
    vendor_dir = os.path.join(path, 'vendor')
    copy_helper(src_dir, vendor_dir)

    save_id(path, '_design/{0}'.format(os.path.split(path)[-1]))
    localdoc.document(path, create=True)


def generate_function(path, func_type, name, template='default'):
    '''
    Generate function from template

    :param path: the app dir
    :param func_type: function type. e.g. ``view``, ``show``.
    :param name: the function name
    :param template: the template set

    The big picture of template dir is discribed
    in :py:func:`~couchapp.generate.init_template`.

    Here we show the detail structure of ``functions`` dir::

        functions/
            filter.js
            list.js
            map.js
            reduce.js
            show.js
            spatial.js
            update.js
            validate_doc_update.js
            ...
            myfunc.js
    '''
    tmpl_name = os.path.join(*template.split('/'))
    tmpl_dir = find_template_dir(tmpl_name, tmpl_type='functions',
                                 raise_error=True)

    file_list = []  # [(src, dest), ...]
    empty_dir = False
    if func_type == 'view':
        dir_ = os.path.join(path, 'views', name)
        empty_dir = True
        file_list.append(('map.js', 'map.js'))
        file_list.append(('reduce.js', 'reduce.js'))

    elif func_type in ('filter', 'list', 'show', 'update'):
        dir_ = os.path.join(path, '{0}s'.format(func_type))
        file_list.append(('{0}.js'.format(func_type),
                          '{0}.js'.format(name)))

    elif func_type == 'function':  # user defined function
        dir_ = path
        file_list.append(('{0}.js'.format(name),
                          '{0}.js'.format(name)))

    elif func_type == 'spatial':
        dir_ = os.path.join(path, 'spatial')
        file_list.append(('spatial.js', '{0}.js'.format(name)))

    elif func_type == 'validate_doc_update':
        dir_ = path
        file_list.append(('validate_doc_update.js', 'validate_doc_update.js'))

    else:
        raise AppError('unrecognized function type "{0}"'.format(func_type))

    setup_dir(dir_, require_empty=empty_dir)

    for src, dest in file_list:
        full_src = os.path.join(tmpl_dir, src)
        full_dest = os.path.join(dir_, dest)

        try:
            copy2(full_src, full_dest)
        except Error:
            logger.warning('function "%s" not found in "%s"', src, tmpl_dir)
        else:
            logger.debug('function "%s" generated successfully', dest)

    logger.info('enjoy the %s function, "%s"!', func_type, name)


def generate_vendor(path, name, template='default'):
    '''
    Generate vendor from template set

    :param path: the app dir
    :param name: the vendor name
    :param template: the template set
    '''
    tmpl_name = os.path.join(*template.split('/'))
    tmpl_dir = find_template_dir(tmpl_name, tmpl_type='vendor',
                                 raise_error=True)

    vendor_dir = os.path.join(path, 'vendor')
    setup_dir(vendor_dir)

    copy_helper(tmpl_dir, vendor_dir)

    logger.debug('vendor dir "%s"', tmpl_dir)
    logger.info('vendor "%s" generated successfully', name)


def copy_helper(src, dest):
    '''
    copy helper similar to ``shutil.copytree``

    But we do not require ``dest`` non-exist

    :param str src: source dir
    :param str dest: destination dir

    e.g::

        foo/
            bar.txt

        baz/
            *empty dir*

    ``copy_helper('foo', 'bar')`` will copy ``bar.txt`` as ``baz/bar.txt``.

    ..versionchanged: 1.1
    '''
    if not os.path.isdir(src):
        raise OSError('source "{0}" is not a directory'.format(src))

    setup_dir(dest, require_empty=False)

    for p in os.listdir(src):
        _src = os.path.join(src, p)
        _dest = os.path.join(dest, p)

        if os.path.isdir(_src):
            copytree(_src, _dest)
        else:
            copy2(_src, _dest)


def find_template_dir(tmpl_name='default', tmpl_type='', raise_error=False):
    '''
    Find template dir for different platform

    :param tmpl_name: The template name under ``templates``.
                      It can be empty string.
                      If it is set to ``default``, we will use consider
                      the tmpl_name as empty.
                      e.g. ``mytmpl`` mentioned in the docstring of
                      :py:func:`~couchapp.generate.init_template`
    :param tmpl_type: the type of template.
                      e.g. 'app', 'functions', 'vendor'
    :param bool raise_error: raise ``AppError`` if not found
    :return: the absolute path or ``None`` if not found

    We will check the ``<search path>/templates/<tmpl_name>/<tmpl_type>`` is
    dir or not. The first matched win.

    For posix platform, the search locations are following:
    - ~/.couchapp/
    - <module dir path>/
    - <module dir path>/../
    - /usr/share/couchapp/
    - /usr/local/share/couchapp/
    - /opt/couchapp/

    For darwin (OSX) platform, we have some extra search locations:
    - ${HOME}/Library/Application Support/Couchapp/

    For windows with standlone binary (py2exe):
    - <executable dir path>/
    - <executable dir path>/../

    For windows with python interpreter:
    - ${USERPROFILE}/.couchapp/
    - <module dir path>/
    - <module dir path>/../
    - <python prefix>/Lib/site-packages/couchapp/

    ..versionchanged:: 1.1
    '''
    if tmpl_type and tmpl_type not in TEMPLATE_TYPES:
        raise AppError('invalid template type "{0}"'.format(tmpl_type))

    if tmpl_name == 'default':
        tmpl_name = ''

    modpath = os.path.dirname(__file__)
    search_paths = user_path() + [
        modpath,
        os.path.join(modpath, '..'),
    ]

    if os.name == 'posix':
        search_paths.extend([
            '/usr/share/couchapp',
            '/usr/local/share/couchapp',
            '/opt/couchapp',
        ])
    elif is_py2exe():
        search_paths.append(os.path.dirname(sys.executable))
    elif is_windows():
        search_paths.append(
            os.path.join(sys.prefix, 'Lib', 'site-packages', 'couchapp')
        )

    # extra path for darwin
    if sys.platform.startswith('darwin'):
        search_paths.append(
            os.path.expanduser('~/Library/Application Support/Couchapp')
        )

    # the first win!
    for path in search_paths:
        path = os.path.normpath(path)
        path = os.path.join(path, 'templates', tmpl_name, tmpl_type)
        if os.path.isdir(path):
            logger.debug('template path match: "{0}"'.format(path))
            return path

        logger.debug('template search path: "{0}" not found'.format(path))

    if raise_error:
        logger.info('please use "-d" to checkout search paths.')
        raise AppError('template "{0}/{1}" not found.'.format(
            tmpl_name, tmpl_type))

    return None


def generate(path, kind, name, **opts):
    kinds = ('view', 'list', 'show', 'filter', 'function', 'vendor', 'update',
             'spatial')
    if kind not in kinds:
        raise AppError("Can't generate '{0}' in your couchapp. "
                       'generator is unknown.'.format(kind))

    if kind == 'vendor':
        return generate_vendor(path, name, opts.get('template', 'default'))
    generate_function(path, kind, name, opts.get('template', 'default'))


def save_id(app_path, name):
    '''
    Save ``name`` into ``app_path/_id`` file.
    if file exists, we will overwride it.

    :param str app_dir:
    :param str name:
    '''
    with open(os.path.join(app_path, '_id'), 'wb') as f:
        f.write(name)
