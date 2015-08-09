CouchApp: Web application hosted in Apache CouchDB
==================================================

CouchApps are JavaScript and HTML5 applications served directly from CouchDB.
If you can fit your application into those constraints,
then you get CouchDB's scalability and flexibility **for free**
(and deploying your app is as simple as replicating it to the production server).

.. note::
    The original CouchApp command-line tools were created in 2008 / 2009 by
    @benoitc and @jchris. They still work, and have been feature complete
    for a long time.

    Couchapp has been replaced and is compatible with the
    old couchapp tool. There are also new tools for deploying browser-based
    apps to JSON web servers and `PouchDB <http://pouchdb.com/>`__
    is the future of browser based sync apps. It can sync with the same sync
    protocols but uses the built-in storage of HTML5.


Getting Started
---------------

.. toctree::
    :maxdepth: 1
    what-is-couchapp

-  `What the HTTP is CouchApp? <what-is-couchapp.md>`__
-  The `Standalone
   Applications <http://guide.couchdb.org/editions/1/en/standalone.html>`__
   and `Managing Design
   Documents <http://guide.couchdb.org/editions/1/en/managing.html>`__
   chapters of the O'Reilly CouchDB book
-  `Getting Started Tutorial <getting-started.md>`__
-  `Video Tutorials and Screencasts <videos.md>`__
-  `Help with installing and running individual
   applications <application-help.md>`__
-  `Using backbone.js in CouchApps <backbone.md>`__


CouchApp Development Tools
--------------------------

To develop a CouchApp, you will need a way to get your javascript, html
and other resources onto your CouchDB instance. Typically this is done
with a CouchApp command line tool that maps application assets and
CouchDB views, lists, shows, etc into one or more Design Documents.

-  `CouchApp Filesystem Mapping <filesystem-mapping.md>`__ - couchapp.py
   and erica (mentioned below) implement a consistent
   filesystem-to-design-document mapping

Curl
~~~~

The simplest way to develop a couchapp would be to use curl from the
command line.

`CouchApp <couchapp-python.md>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

command line tool (python)

The `CouchApp <couchapp-python.md>`__ command line tool is used to
generate code templates in your application and to push your changes to
an instance of couchdb, among other things. Here is how to get started
with the CouchApp command line tool:

-  `Installing couchapp <installing.md>`__
-  `Couchapp configuration <couchapp-config.md>`__
-  `The couchapp command line tool <couchapp-usage.md>`__
-  `Extending the couchapp command line tool <couchapp-extend.md>`__
-  `Using couchapp with multiple design
   documents <multiple-design-docs.md>`__

There can be confusion with the term 'CouchApp' because it can refer to
this tool, named 'CouchApp', or a general application served from
CouchDB. This is probably due to the fact that the CouchApp command line
tool was the first full way of developing a CouchApp.

CouchApp command line tool (node.couchapp.js)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  https://github.com/mikeal/node.couchapp.js
-  http://japhr.blogspot.com/2010/04/quick-intro-to-nodecouchappjs.html

This is an alternative tooling to the Python couchapp utility that is
instead written in Node.js. It uses a much simpler folder structure than
it's Python counterpart and is a generally more minimalist/simplified
way of writing couchapps. Note that you cannot use Python couchapp to
push couchapps written using node.couchapp.js into Couch and vice versa.

erica
~~~~~

`erica <https://github.com/benoitc/erica>`__ is an Erlang- based command
line tool that is compatible with the Python and Node.js "couchapp"
tools.

Kanso
~~~~~

A comprehensive, framework-agnostic build tool for CouchApps.

The Kanso command-line tool can build projects designed for
node.couchapp.js, or even the Python couchapp tool, while providing many
other options for building your app. These build steps and other code
can be shared using the online `package
repository <http://kan.so/packages>`__. Compiling coffee-script, .less
CSS templates etc. is as easy as including the relevant package.

**"NPM for CouchApps"**

Kanso also lets you merge design docs together, which allows reusable
components built with any of the available couchapp tools. The Kanso
tool can help you manage dependencies and share code between projects,
as well as providing a library of JavaScript modules for use with
CouchDB.

`Kanso Homepage <http://kan.so/>`__

soca
~~~~

soca is a command line tool written in ruby for building and pushing
couchapps. It is similar to the canonical couchapp python tool, with a
number of key differences:

-  local directories do not have to map 1-1 to the design docs directory
-  lifecycle management & deployment hooks for easily adding or
   modifying the design document with ruby tools or plugins.
-  architected around using Sammy.js, instead of Evently, which is
   bundled with the python tool. Sammy.js is a Sinatra inspired
   browser-side RESTframework which is used by default.

Unlike a traditional couchapp, a soca couchapp is one way - your source
directory structure is actually 'compiled' into into the couchapp
\_design document format.

*compile time plugins:*

-  Compass
-  CoffeeScript
-  Mustache
-  JavaScript bundling for CouchDB and the browser

`soca on Github <https://github.com/quirkey/soca>`__

Reupholster
~~~~~~~~~~~

Reupholster is geared for CouchApp beginners and simple CouchApps. What
reupholster does is allows you to experience writing a CouchApp as fast
as possible, with very little learning curve. It just feels like you are
editing a normal web project.

`Reupholster
Homepage <http://reupholster.iriscouch.com/reupholster/_design/app/index.html>`__

Javascript Application Programming
----------------------------------

All application logic in a couchapp is provided by Javascript. There is
a library called
`jquery.couch.js <https://github.com/apache/couchdb/blob/trunk/share/www/script/jquery.couch.js>`__
that is distributed with every CouchDB installation. Here is the
`documentation for
jquery.couch.js <http://daleharvey.github.com/jquery.couch.js-docs/symbols/index.html>`__

Example Applications
~~~~~~~~~~~~~~~~~~~~

You can download the following applications and try them out yourself.

`Pages <https://github.com/couchone/pages>`__
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The wiki software behind couchapp.org

-  `Installing Pages <pages-install.md>`__
-  `Pages Application Walkthrough <NotesOnPagesFiles.md>`__

A couchapp for keeping teams on the same page

`Sofa <https://github.com/jchris/sofa>`__
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Standalone CouchDB Blog, used by the O'Reilly CouchDB book (note: sofa
does not work as well with couchdb 1.0.1 or 1.0.2, the edit and create
new pages do not work. Also, there is a different version of mustache.js
in the /design\_doc\_name/lib directory that is used to render all the
\_list functions. The normal mustache.js file is in the vendor/couchapp
directory. )

`TweetEater <https://github.com/doppler/TweetEater>`__
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A Couchapp which displays tweets harvested from Twitter's streaming API
by an accompanying Ruby program.

Other resources
---------------

-  `Search The CouchDB Mailing List/IRC
   Archive <http://archive.couchdb.org/>`__
-  `A List of CouchApps <list-of-couchapps.md>`__
-  `CouchApps with DesktopCouch <desktopcouch.md>`__
-  `Roadmap <roadmap.md>`__
-  `Mailing List <http://groups.google.com/group/couchapp>`__
-  `Contributing to CouchApp <how-to-contribute.md>`__
-  `Some development notes <development-notes.md>`__
-  `The CouchApp Garden project <garden.md>`__
-  `eNotes CouchApp
   Tutorial <http://materials.geoinfo.tuwien.ac.at/tutorials/couchapp>`__

Files attached to *Simple JavaScript application hosted in Apache
CouchDB*:

-  `390460\_185903128166121\_700165246\_n.jpg <attachments/390460_185903128166121_700165246_n.jpg>`__
   (image/jpeg)
-  `N68-VS3 UCC.pdf <attachments/N68-VS3%20UCC.pdf>`__ (application/pdf)
-  `mike wazowski.jpg <attachments/mike%20wazowski.jpg>`__ (image/jpeg)
-  `demo.html <attachments/demo.html>`__ (text/html)
-  `acralyzer-master.zip <attachments/acralyzer-master.zip>`__
   (application/octet-stream)
-  `untitled.txt <attachments/untitled.txt>`__ (text/plain)
-  `multiple\_design\_documents <attachments/multiple_design_documents>`__
   (application/octet-stream)
-  `multiple\_design\_documents.html <attachments/multiple_design_documents.html>`__
   (text/html)
-  `couchapp\_blog\_entry.txt <attachments/couchapp_blog_entry.txt>`__
   (text/plain)
