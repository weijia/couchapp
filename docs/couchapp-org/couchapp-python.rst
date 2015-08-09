couchapp (python)
=================

The `couchapp <couchapp-python.md>`__ command line tool is written in
Python and used to generate code templates in your application and to
push your changes to an instance of couchdb, among other things. Here is
how to get started with the CouchApp command line tool:

-  `Installing couchapp <installing.md>`__
-  `Couchapp configuration <couchapp-config.md>`__
-  `The couchapp command line tool <couchapp-usage.md>`__
-  `Extending the couchapp command line tool <couchapp-extend.md>`__
-  `Using couchapp with multiple design
   documents <multiple-design-docs.md>`__
-  `The Filesystem Mapping <filesystem-mapping.md>`__

There can be confusion with the term 'CouchApp' because it can refer to
this tool, named 'CouchApp', or a general application served from
CouchDB. This is probably due to the fact that the CouchApp command line
tool was the first full way of developing a CouchApp.

The Generated Application
~~~~~~~~~~~~~~~~~~~~~~~~~

After creating a new couchapp, you will have a project structure that
looks something like `this template
project <https://github.com/jchris/proto>`__. The following libraries
are included with your new couchapp by default:

`Evently <evently.md>`__
^^^^^^^^^^^^^^^^^^^^^^^^

A declarative, couchdb friendly JQuery library for writing Javascript
applications

CouchDB API (`jquery.couch.js <http://github.com/apache/couchdb/blob/trunk/share/www/script/jquery.couch.js>`__)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The JQuery library included with CouchDB itself for use by the Futon
admin console is used to interact with couchdb. Some `limited
documentation <http://www.couch.io/page/library-jquery-couch-js-database>`__
is available from Couchone.

CouchApp Loader (`jquery.couch.app.js <https://github.com/couchapp/couchapp/blob/master/couchapp/templates/vendor/_attachments/jquery.couch.app.js>`__)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A utility for loading design document classes into your Javascript
application

Pathbinder (`jquery.pathbinder.js <http://couchapp.couchone.com/docs/_design/docs/index.html#/topic/pathbinder>`__)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A tiny framework for triggering events based on paths in URL hash.

`Mustache <https://github.com/janl/mustache.js>`__
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A simple template framework
