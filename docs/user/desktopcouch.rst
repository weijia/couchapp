.. _couchdesktop:

CouchApps and DesktopCouch
==========================

In **version 0.7**, ``couchapp.py`` has a new feature allowing you
to push, clone and browse CouchApps in the local CouchDB installed with
`desktopcouch <http://freedesktop.org/wiki/Specifications/desktopcouch>`_,
so users of linux distributions where desktopcouch has been ported
won't have to install another CouchDB to test and will be able to pair
it with other desktop.


How it works?
-------------

To push to your local couchdb installed with desktopcouch:

::

    couchapp push desktopcouch://testdb 

To clone:

::

    couchapp clone desktopcouch://testdb/_design/test test1 

To browse and use your application:

::

    couchapp browse . desktopcouch://mydb 

and with push option :

::

    couchapp push --browse . desktopcouch://mydb
