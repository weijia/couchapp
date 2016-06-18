.. _couchapp-usage:

Command Line Usage
===============================================================================

.. toctree::


.. highlight:: shell


.. warning::

    There are many undocumented commands.
    We need your help!


Full command line usage
----------------------------------------------------------------------

.. literalinclude:: usage.txt


Commands
----------------------------------------------------------------------


.. _cmd-generate:

``generate``
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionchanged:: 1.1
    Remove the ability to generate a whole app,
    use :ref:`cmd-init` instead.

Allows you to generate one of CouchApp components from a
:ref:`template <couchapp-template>`.
There are two type of components:

#. Functions
#. Vendor

If the template name do not be provide by user, we will use the ``default``
:ref:`template <couchapp-template>`.

For example, we can generate a ``show`` function::

    $ cd /path/to/app
    $ couchapp generate show hello
    2016-06-18 17:36:21 [INFO] enjoy the show function, "hello"!
    $ tree shows
    shows
    └── hello.js

    0 directories, 1 file


.. _cmd-init:

``init``
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionchanged:: 1.1
   Introduce different level of init.

Initialize a CouchApp. We provide three levels of initialization:

#. `The minimal init`_, with the ``-e`` command line option.
#. `The basic skeleton`_. This is the default level.
#. `Init from template`_, with the ``-t TEMPLATE`` command line option.


The Minimal Init
**************************************************

We add an option ``-e`` for ``init``. The ``e`` stands for *empty*.
If you just want to start from scratch, please choose this init level.

::

    $ couchapp init -e myapp
    $ cd myapp
    $ tree -a
    .
    ├── .couchappignore
    └── .couchapprc

    0 directories, 2 files

.. note::
    The file ``.couchapprc`` is required for ``couchapp``.


The Basic Skeleton
**************************************************

This is the default level of ``init`` command.
We will prepare some dir skeleton for you.

::

    $ couchapp init myapp
    $ cd myapp
    $ tree -a
    .
    ├── .couchappignore
    ├── .couchapprc
    ├── _attachments
    ├── _id
    ├── filters
    ├── lists
    ├── shows
    ├── updates
    └── views

    6 directories, 3 files


Init from Template
**************************************************

We can create our CouchApp from a :ref:`template <couchapp-template>`.
The :ref:`template <couchapp-template` will be handy with some hook.
For instance, someone can write an ``npm`` hook for installing
node modules during template generating.

For more info about template, please check out
:ref:`couchapp-template` section.

::

    $ couchapp init -t default myapp
    $ cd myapp
    $ tree -a
    .
    ├── .couchappignore
    ├── .couchapprc
    ├── README.md
    ├── _attachments
    │   ├── index.html
    │   ├── script
    │   │   └── app.js
    │   └── style
    │       └── main.css
    ├── _id
    ├── couchapp.json
    ├── filters
    ├── language
    ├── lists
    ├── shows
    ├── updates
    ├── vendor
    │   └── couchapp
    │       ├── _attachments
    │       │   ├── jquery.couch.app.js
    │       │   ├── jquery.couch.app.util.js
    │       │   ├── jquery.couchForm.js
    │       │   ├── jquery.couchLogin.js
    │       │   ├── jquery.couchProfile.js
    │       │   ├── jquery.mustache.js
    │       │   └── md5.js
    │       └── metadata.json
    └── views
        └── recent-items
            └── map.js

    12 directories, 18 files


.. _cmd-push:

``push``
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

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

.. _cmd-pushapps:

``pushapps``
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Like ``push`` but on a folder containing couchapps.
It allows you to send multiple couchapps at once.

::

    $ ls somedir/
    app1/ app2/ app3/
    $ couchapp pushapps somedir/ http://localhost:5984/mydb

.. _cmd_pushdocs:

``pushdocs``
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Like pushapps but for docs. It allows you to send a
folder containing simple document. With this command you can populate
your CouchDB_ with documents. Anotther way to do it is to create a
``_docs`` folder at the top of your couchapp folder.


``startapp``
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. deprecated:: 1.1
   Please use :ref:`cmd-init` instead.

It's an alias of ``init APP_NAME``, e.g.::

    $ couchapp startapp myapp


.. _CouchDB: http://couchdb.apache.org
