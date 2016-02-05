.. _couchapp-usage:

Command Line Usage
==================

.. toctree::


.. highlight:: shell


.. warning::

    There are many undocumented commands.
    We need your help!


Full command line usage
-----------------------

.. literalinclude:: usage.txt


Commands
--------


``generate``
+++++++++++++

Allows you to generate a basic couchapp. It can also
be used to create :ref:`template <couchapp-template>` of functions. e.g.::

    $ couchapp generate myapp
    $ cd myapp
    $ couchapp generate view someview


``init``
+++++++++

Initialize a CouchApp. When run in the folder of your
application it create a default ``.couchapprc`` file. This file is
needed by couchapp to find your application. Use this command when
you clone your application from an external repository (``git``, ``hg``):

::

    $ cd mycouchapp
    $ couchapp init


``push``
++++++++++

Push a couchapp to one or more CouchDB_ server.

::

    $ cd mycouchapp
    $ couchapp push http://someserver:port/mydb

-  ``--no-atomic`` option allows you to send attachments one by one.
   By default all attachments are sent inline.
-  ``--export`` options allows you to get the JSON document created.
   Combined with ``--output``, you can save the result in a file.
-  ``--force``: force attachment sending
-  ``--docid`` option allows you to set a custom docid for this
   couchapp


``pushapps``
+++++++++++++

Like ``push`` but on a folder containing couchapps.
It allows you to send multiple couchapps at once.

::

    $ ls somedir/
    app1/ app2/ app3/
    $ couchapp pushapps somedir/ http://localhost:5984/mydb


``pushdocs``
+++++++++++++

Like pushapps but for docs. It allows you to send a
folder containing simple document. With this command you can populate
your CouchDB_ with documents. Anotther way to do it is to create a
``_docs`` folder at the top of your couchapp folder.


.. _CouchDB: http://couchdb.apache.org


``startapp``
++++++++++++

It's an alias of ``generate app NAME``, e.g.::

    $ couchapp startapp myapp
