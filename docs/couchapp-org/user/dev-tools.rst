.. _dev-tools:

CouchApp Development Tools
==========================

To develop a CouchApp, you will need a way to get your javascript,
html and other resources onto your CouchDB instance.
Typically this is done with a CouchApp command line tool
that maps application assets and CouchDB views, lists, shows,
etc into one or more Design Documents.

- :ref:`filesystem-mapping.html` - ``couchapp.py``
  and erica_ (mentioned below) implement a consistent
  filesystem-to-design-document mapping

.. note::
    The original CouchApp command line tools were created in 2008 / 2009 by
    @benoitc and @jchris. They still work, and have been feature complete
    for a long time. ``couchapp`` has been replaced and is compatible with the
    old ``couchapp`` tool.


cURL
----

The simplest way to develop a couchapp would be to use ``curl`` from the
command line.


`CouchApp command line tool <couchapp-python.html>`_
------------------------------------------------------

The `CouchApp command line tool <couchapp-python.html>`_ is used to
generate code templates in your application and to push your changes to
an instance of CouchDB, among other things. Here is how to get started
with the CouchApp command line tool:

-  `Installing couchapp <installing.html>`_
-  `Couchapp configuration <couchapp-config.html>`_
-  `The couchapp command line tool <couchapp-usage.html>`_
-  `Extending the couchapp command line tool <couchapp-extend.html>`_
-  `Using couchapp with multiple design documents <multiple-design-docs.html>`_

.. note::
    There can be confusion with the term *CouchApp* because it can refer to
    this tool, named *CouchApp*, or a general application served from
    CouchDB. This is probably due to the fact that the CouchApp command line
    tool, as known as ``couchapp.py`` , was the first full way of developing a
    CouchApp.


node.couchapp.js_
-----------------

.. _node.couchapp.js: https://github.com/mikeal/node.couchapp.js

-  http://japhr.blogspot.com/2010/04/quick-intro-to-nodecouchappjs.html

This is an alternative tooling to the Python couchapp utility that is
instead written in Node.js. It uses a much simpler folder structure than
it's Python counterpart and is a generally more minimalist/simplified
way of writing couchapps. Note that you cannot use Python couchapp to
push couchapps written using node.couchapp.js_ into CouchDB and vice versa.


erica_
-------

.. _erica: https://github.com/benoitc/erica

erica_ is an Erlang-based command line tool that is compatible with
the Python and Node.js CouchApp tools.


Kanso_
-------

.. _Kanso: http://kan.so/

A comprehensive, framework-agnostic build tool for CouchApps.

The Kanso_ command line tool can build projects designed for
node.couchapp.js, or even the Python couchapp tool, while providing many
other options for building your app. These build steps and other code
can be shared using the online `package
repository <http://kan.so/packages>`_. Compiling coffee-script, ``.less``
CSS templates etc. is as easy as including the relevant package.

NPM for CouchApps
+++++++++++++++++++

Kanso_ also lets you merge design docs together, which allows reusable
components built with any of the available couchapp tools. The Kanso_
tool can help you manage dependencies and share code between projects,
as well as providing a library of JavaScript modules for use with
CouchDB.


soca_
------

.. _soca: https://github.com/quirkey/soca

soca_ is a command line tool written in ruby for building and pushing
couchapps. It is similar to the canonical couchapp python tool, with a
number of key differences:

-  local directories do not have to map 1-1 to the design docs directory
-  lifecycle management & deployment hooks for easily adding or
   modifying the design document with ruby tools or plugins.
-  architected around using Sammy.js, instead of Evently, which is
   bundled with the python tool. Sammy.js is a Sinatra inspired
   browser-side RESTframework which is used by default.

Unlike a traditional couchapp, a soca_ couchapp is one way - your source
directory structure is actually 'compiled' into into the couchapp
``_design`` document format.

Compile time plugins:

-  Compass
-  CoffeeScript
-  Mustache
-  JavaScript bundling for CouchDB and the browser


Reupholster_
------------

.. _Reupholster: http://reupholster.iriscouch.com/reupholster/_design/app/index.html

Reupholster_ is geared for CouchApp beginners and simple CouchApps.
What Reupholster_ does is allows you to experience writing a CouchApp as fast
as possible, with very little learning curve. It just feels like you are
editing a normal web project.
