CouchApp: Web application hosted in Apache CouchDB
==================================================

CouchApps are JavaScript and HTML5 applications served directly from CouchDB.
If you can fit your application into those constraints,
then you get CouchDB's scalability and flexibility **for free**
(and deploying your app is as simple as replicating it to the production server).

.. note::
    The original CouchApp command line tools were created in 2008 / 2009 by
    @benoitc and @jchris. They still work, and have been feature complete
    for a long time. ``couchapp`` has been replaced and is compatible with the
    old ``couchapp`` tool.

There are also tools for deploying browser-based
apps to JSON web servers and `PouchDB <http://pouchdb.com/>`_
is the future of browser based sync apps. It can sync with the same sync
protocols but uses the built-in storage of HTML5.


Getting Started
---------------

- `What is CouchApp? <what-is-couchapp.html>`_
- The `Standalone Applications <http://guide.couchdb.org/draft/standalone.html>`_
  and `Managing Design Documents <http://guide.couchdb.org/draft/managing.html>`_
  chapters of the O'Reilly CouchDB book
- `Getting Started Tutorial <../getting-started.html>`_
- `Video Tutorials and Screencasts <videos.html>`_
- `Help with installing and running individual
  applications <application-help.html>`_
- `Using backbone.js with CouchApps <backbone.html>`_


CouchApp Development Tools
--------------------------

To develop a CouchApp, you will need a way to get your javascript,
html and other resources onto your CouchDB instance.
Typically this is done with a CouchApp command line tool
that maps application assets and CouchDB views, lists, shows,
etc into one or more Design Documents.

- `CouchApp Filesystem Mapping <filesystem-mapping.html>`_ - ``couchapp.py``
  and erica_ (mentioned below) implement a consistent
  filesystem-to-design-document mapping


``curl``
~~~~~~~~~

The simplest way to develop a couchapp would be to use curl from the
command line.


`CouchApp command line tool <couchapp-python.html>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The `CouchApp command line tool <couchapp-python.html>`_ is used to
generate code templates in your application and to push your changes to
an instance of CouchDB, among other things. Here is how to get started
with the CouchApp command line tool:

-  `Installing couchapp <installing.html>`_
-  `Couchapp configuration <couchapp-config.html>`_
-  `The couchapp command line tool <couchapp-usage.html>`_
-  `Extending the couchapp command line tool <couchapp-extend.html>`_
-  `Using couchapp with multiple design
   documents <multiple-design-docs.html>`_

.. note::
    There can be confusion with the term *CouchApp* because it can refer to
    this tool, named *CouchApp*, or a general application served from
    CouchDB. This is probably due to the fact that the CouchApp command line
    tool, as known as ``couchapp.py`` , was the first full way of developing a
    CouchApp.


node.couchapp.js_
~~~~~~~~~~~~~~~~~

.. _node.couchapp.js: https://github.com/mikeal/node.couchapp.js

-  http://japhr.blogspot.com/2010/04/quick-intro-to-nodecouchappjs.html

This is an alternative tooling to the Python couchapp utility that is
instead written in Node.js. It uses a much simpler folder structure than
it's Python counterpart and is a generally more minimalist/simplified
way of writing couchapps. Note that you cannot use Python couchapp to
push couchapps written using node.couchapp.js_ into CouchDB and vice versa.


erica_
~~~~~~~

.. _erica: https://github.com/benoitc/erica

erica_ is an Erlang-based command line tool that is compatible with
the Python and Node.js CouchApp tools.


Kanso_
~~~~~~~

.. _Kanso: http://kan.so/

A comprehensive, framework-agnostic build tool for CouchApps.

The Kanso_ command line tool can build projects designed for
node.couchapp.js, or even the Python couchapp tool, while providing many
other options for building your app. These build steps and other code
can be shared using the online `package
repository <http://kan.so/packages>`_. Compiling coffee-script, ``.less``
CSS templates etc. is as easy as including the relevant package.

NPM for CouchApps
^^^^^^^^^^^^^^^^^^^

Kanso_ also lets you merge design docs together, which allows reusable
components built with any of the available couchapp tools. The Kanso_
tool can help you manage dependencies and share code between projects,
as well as providing a library of JavaScript modules for use with
CouchDB.


soca_
~~~~~~

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
~~~~~~~~~~~~

.. _Reupholster: http://reupholster.iriscouch.com/reupholster/_design/app/index.html

Reupholster_ is geared for CouchApp beginners and simple CouchApps.
What Reupholster_ does is allows you to experience writing a CouchApp as fast
as possible, with very little learning curve. It just feels like you are
editing a normal web project.


JavaScript Application Programming
----------------------------------

.. _jquery.couch.js: https://github.com/apache/couchdb/blob/trunk/share/www/script/jquery.couch.js
.. _documentation for jquery.couch.js: http://daleharvey.github.com/jquery.couch.js-docs/symbols/index.html

All application logic in a couchapp is provided by JavaScript.
There is a library called `jquery.couch.js`_ that is distributed
with every CouchDB installation.
Here is the `documentation for jquery.couch.js`_


Example Applications
~~~~~~~~~~~~~~~~~~~~

You can download the following applications and try them out yourself.


`Pages <https://github.com/couchone/pages>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The wiki software behind couchapp.org(old site)

-  `Installing Pages <pages-install.html>`_
-  `Pages Application Walkthrough <NotesOnPagesFiles.html>`_

A couchapp for keeping teams on the same page


Sofa_
^^^^^

.. _Sofa: https://github.com/jchris/sofa

Standalone CouchDB Blog, used by the O'Reilly CouchDB book.

.. note:: 
    Sofa_ does not work as well with couchdb 1.0.1 or 1.0.2, the edit and create
    new pages do not work. Also, there is a different version of mustache.js
    in the ``/design_doc/lib`` directory that is used to render all the
    ``_list`` functions. The normal mustache.js file is in the vendor/couchapp
    directory. )


`TweetEater <https://github.com/doppler/TweetEater>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A Couchapp which displays tweets harvested from Twitter's streaming API
by an accompanying Ruby program.


More Examples
-------------

Please check out the `List of CouchApps <list-of-couchapps.html>`_.


Other resources
---------------

- `Search The CouchDB Mailing List/IRC
  Archive <http://archive.couchdb.org/>`_
- `CouchApps with DesktopCouch <desktopcouch.html>`_
- `Roadmap <roadmap.html>`_
- `Mailing List <http://groups.google.com/group/couchapp>`_
- `Contributing to CouchApp <how-to-contribute.html>`_
- `Some development notes <development-notes.html>`_
- `The CouchApp Garden project <garden.html>`_
- `eNotes CouchApp
  Tutorial <http://materials.geoinfo.tuwien.ac.at/tutorials/couchapp>`_
- #couchapp at freenode
