# -*- coding: utf-8 -*-
#
# This file is part of couchapp released under the Apache 2 license.
# See the NOTICE for more information.

from __future__ import with_statement

import logging
import os
import shutil
import sys

from couchapp.errors import AppError
from couchapp import localdoc
from couchapp.util import is_py2exe, is_windows, relpath, setup_dir, user_path
from couchapp.util import setup_dirs

__all__ = ["init_basic", "init_template", "generate_function", "generate"]

logger = logging.getLogger(__name__)


DEFAULT_APP_TREE = ['_attachments',
                    'lists',
                    'shows',
                    'updates',
                    'views']


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
    '''
    setup_dir(path, require_empty=True)
    setup_dirs(os.path.join(path, n) for n in DEFAULT_APP_TREE)

    save_id(path, '_design/{0}'.format(os.path.split(path)[-1]))
    localdoc.document(path, create=True)


def init_template(path, template=None):
    '''
    Generates a CouchApp via template
    '''
    TEMPLATES = ['app']
    prefix = os.path.join(*template.split('/')) if template is not None else ''

    setup_dir(path, require_empty=True)

    for n in DEFAULT_APP_TREE:
        tp = os.path.join(path, n)
        os.makedirs(tp)

    for t in TEMPLATES:
        appdir = path
        if prefix:
            # we do the job twice for now to make sure an app or vendor
            # template exist in user template location
            # fast on linux since there is only one user dir location
            # but could be a little slower on windows
            for user_location in user_path():
                location = os.path.join(user_location, 'templates', prefix, t)
                if os.path.exists(location):
                    t = os.path.join(prefix, t)
                    break

        copy_helper(appdir, t)

    # add vendor
    vendor_dir = os.path.join(appdir, 'vendor')
    os.makedirs(vendor_dir)
    copy_helper(vendor_dir, '', tname="vendor")

    fid = os.path.join(appdir, '_id')
    if not os.path.isfile(fid):
        with open(fid, 'wb') as f:
            f.write('_design/{0}'.format(os.path.split(appdir)[1]))

    localdoc.document(path, create=True)


def generate_function(path, kind, name, template=None):
    functions_path = ['functions']
    if template:
        functions_path = []
        _relpath = os.path.join(*template.split('/'))
        template_dir = find_template_dir(_relpath)
    else:
        template_dir = find_template_dir()
    if template_dir:
        functions = []
        if kind == "view":
            path = os.path.join(path, "%ss" % kind, name)
            if os.path.exists(path):
                raise AppError("The view %s already exists" % name)
            functions = [('map.js', 'map.js'), ('reduce.js', 'reduce.js')]
        elif kind == "function":
            functions = [('%s.js' % name, '%s.js' % name)]
        elif kind == "vendor":
            app_dir = os.path.join(path, "vendor", name)
            try:
                os.makedirs(app_dir)
            except:
                pass
            targetpath = os.path.join(*template.split('/'))
            copy_helper(path, targetpath)
            return
        elif kind == "spatial":
            path = os.path.join(path, "spatial")
            functions = [("spatial.js", "%s.js" % name)]
        else:
            path = os.path.join(path, "%ss" % kind)
            functions = [('%s.js' % kind, "%s.js" % name)]
        try:
            os.makedirs(path)
        except:
            pass

        for template, target in functions:
            target_path = os.path.join(path, target)
            root_path = [template_dir] + functions_path + [template]
            root = os.path.join(*root_path)
            try:
                shutil.copy2(root, target_path)
            except:
                logger.warning("%s not found in %s" %
                               (template, os.path.join(*root_path[:-1])))
    else:
        raise AppError("Defaults templates not found. Check your install.")


def copy_helper(path, directory, tname="templates"):
    """ copy helper used to generate an app"""
    if tname == "vendor":
        tname = os.path.join("templates", tname)

    templatedir = find_template_dir(tname, directory)
    if templatedir:
        if directory == "vendor":
            path = os.path.join(path, directory)
            try:
                os.makedirs(path)
            except:
                pass

        for root, dirs, files in os.walk(templatedir):
            rel = relpath(root, templatedir)
            if rel == ".":
                rel = ""
            target_path = os.path.join(path, rel)
            for d in dirs:
                try:
                    os.makedirs(os.path.join(target_path, d))
                except:
                    continue
            for f in files:
                shutil.copy2(os.path.join(root, f),
                             os.path.join(target_path, f))
    else:
        raise AppError(
            "Can't create a CouchApp in %s: default template not found." %
            (path))


def find_template_dir(tmpl_name='', tmpl_type='', raise_error=False):
    '''
    Find template dir for different platform

    :param tmpl_name: The template name under ``templates``.
                      It can be empty string.
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
    '''
    if tmpl_type and tmpl_type not in TEMPLATE_TYPES:
        raise AppError('invalid template type "{0}"'.format(tmpl_type))

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
    if kind not in ['view', 'list', 'show', 'filter',
                    'function', 'vendor', 'update', 'spatial']:
        raise AppError("Can't generate {0} in your couchapp. "
                       'generator is unknown'.format(kind))

    if name is None:
        raise AppError("Can't generate {0} function, "
                       "name is missing".format(kind))

    generate_function(path, kind, name, opts.get("template"))


def save_id(app_path, name):
    '''
    Save ``name`` into ``app_path/_id`` file.
    if file exists, we will overwride it.

    :param str app_dir:
    :param str name:
    '''
    with open(os.path.join(app_path, '_id'), 'wb') as f:
        f.write(name)
