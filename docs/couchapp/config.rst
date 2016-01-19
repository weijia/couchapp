.. _couchapp-config:

Configuration
===============================================================================

.. highlight:: javascript


Local Configuration
----------------------------------------------------------------------

The following config files are placed in each CouchApp directory.


``.couchapprc`` and ``couchapp.json``
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Every CouchApp **MUST** have a ``.couchapprc`` file in the application directory;
the ``couchapp.json`` is optional.

Both files are a JSON object which contains configuration
parameters that the command-line app uses to build and push your CouchApp.
Note that if they contain the same fields, the ``.couchapprc`` will win.

The ``couchapp generate`` and ``couchapp init`` commands
create a default version of this file for you.

So, what's diff between ``.couchapprc`` and ``couchapp.json``?
Usually, we will put not only configs but some metadata into ``couchapp.json``.
``couchapp.json`` will be published via ``couchapp push``;
the ``.couchapprc`` won't.


The valid fields in ``.couchapprc``:

:env: Place your db credentials here. This field is ``.couchapprc`` only.

:extensions: List of your :ref:`custom extensions <couchapp-extend-extensions>`.

:hooks: Your :ref:`custom hooks <couchapp-extend-hooks>`.

:vendors: List of your :ref:`vendor handlers <couchapp-extend-vendor>`.

::

    {
        "env": {
            // ...
        },
        "extensions": [
            // ...
        ],
        "hooks": {
            // ...
        },
        "vendors": [
            // ...
        ]
    }

The valid fields in ``couchapp.json``:

*Changed in version 1.1*

The ``env`` is not available here. Also, do not place any private
credentials in this file. This file will be distributed via ``couchapp push``.

::

    {
        // other metadata here
        // "name": "myCouchApp",
        // "version": 1.0,
        // ...
        "extensions": [
            // ...
        ],
        "hooks": {
            // ...
        },
        "vendors": [
            // ...
        ]
        // ...
    }


Example
**************************************************

The most common use for the ``.couchapprc`` file is to specify one or
more CouchDB databases to use as the destination for the
``couchapp push`` command. Destination databases are listed under the
``env`` key of the ``.couchapprc`` file as follows:

::

    {
      "env" : {
        "default" : {
          "db" : "http://localhost:5984/mydb"
        },
        "prod" : {
          "db" : "http://admin:password@myhost.com/mydb"
        }
      }
    }

In this example, two environments are specified: ``default``, which pushes
to a local CouchDB instance without any authentication, and ``prod``,
which pushes to a remote CouchDB that requires authentication.
Once these sections are defined in ``.couchapprc``, you can push to your
local CouchDB by running::
    
    couchapp push

(the environment name ``default`` is used when no environment is specified) 
and push to the remote machine using::

    couchapp push prod

For a more complete discussion of the ``env`` section of the ``.couchapprc``
file, see the `Managing Design
Documents <http://guide.couchdb.org/draft/managing.html#configuring>`_
chapter of **CouchDB: The Definitive Guide**.


``.couchappignore``
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

A ``.couchappignore`` file specifies intentionally untracked files that
couchapp should ignore. It's a simple json file containing an array of
regexps that will be use to ignore file.

For example:

::

    [
      ".*\\.swp$",
      ".*~$"
    ]

will ignore all files ending in ``.swp`` and ``~``. Be sure to leave out the
final , in the list.

You can check if couchapp really ignores the files by specifying the -v
option::
    
    couchapp -v push

.. note::
    Windows doesn't like files that only have an extension,
    so creating the ``.couchappignore`` file will be a challenge in windows.
    Possible solutions to creating this file are:

    Using cygwin, type::

        cd /path/to/couchapp
        touch .couchappignore

    and then notepad ``.couchappignore``.


Global Configuration
----------------------------------------------------------------------


``~/.couchapp.conf``
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

One drawback to declaring environments in the ``.couchapprc`` file is
that any usernames and passwords required to push documents are stored
in that file. If you are using source control for your CouchApp, then
those authentication credentials are checked in to your (possibly
public) source control server. To avoid this problem, the ``couchapp``
tool can also read environment configurations from a file stored in your
home directory named ``.couchapp.conf``. This file has the same syntax
as ``.couchapprc`` but has the advantage of being outside of the source
tree, so sensitive login information can be protected. 

If you already have a working ``.couchapprc`` file, simply move it to
``~/.couchapp.conf`` and run ``couchapp init`` to generate a new, empty
``.couchapprc`` file inside your CouchApp directory. If you don't have a
``.couchapprc`` file, ``couchapp`` will display the dreaded
``couchapp error: You aren't in a couchapp`` message.


``~/.couchapp/``
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Please see :ref:`couchapp-template`.


.. TODO::
    more information about other templates like vendor, view, etc.
