.. _couchapp-template:

App Template
============

Most of the time, you will use ``couchapp generate`` to create a new
CouchApp with the default directory layout, example functions, and
vendor directories. If you find yourself creating multiple CouchApps
that always contain the same third-party or in-house files and
libraries, you might consider creating a custom app template containing
these files and using the ``--template`` option of the generate command
to create your customized CouchApps.

After creating a new couchapp, you will have a project structure that
looks something like `this template project <https://github.com/jchris/proto>`_.
The following libraries_ are included with your new CouchApp by default.


``~/.couchapp``
---------------

Custom templates are stored as subdirectories under the
``~/.couchapp/templates`` directory. The name of the subdirectory is
used in the ``--template`` option to specify which template files are
to be used in the ``couchapp generate`` command. The default template
name is *app*, so by creating ``~/.couchapp/templates/app`` and placing
files and directories under that path, you can replace almost all of the
default files created by ``couchapp generate``.


Libraries
---------

CouchDB API `jquery.couch.js`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The JQuery library included with CouchDB itself for use by the Futon
admin console is used to interact with couchdb. 

`Documentation <http://daleharvey.github.io/jquery.couch.js-docs/symbols/>`_


CouchApp Loader `jquery.couch.app.js`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A utility for loading design document classes into your Javascript
application


Mustache_
~~~~~~~~~

A simple template framework


.. _Mustache: https://github.com/janl/mustache.js
.. _jquery.couch.app.js: https://github.com/couchapp/couchapp/tree/master/couchapp/templates/vendor/couchapp/_attachments
.. _jquery.couch.js: https://github.com/apache/couchdb-jquery-couch
