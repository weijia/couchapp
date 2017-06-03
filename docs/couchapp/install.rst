.. _install:

Installation
============

The newest install instructions are always in the
`README <https://github.com/couchapp/couchapp/blob/master/README.rst>`__

In case the below is not updated, check out the `release section
<https://github.com/couchapp/couchapp/releases>`_ in GitHub.


Requirements
------------

-  Python 2.x >= 2.6 (Python 3.x will be supported soon)
-  the header files of the Python version that is used, which are
   included e.g. in the according development package ``python-dev``
   (may have a different name depending on your system)


Installing on all UNIXs
-----------------------

To install couchapp using ``pip`` you must make sure you have a
recent version of ``pip`` installed:

::

    $ curl -O https://bootstrap.pypa.io/get-pip.py
    $ sudo python get-pip.py

To install or upgrade to the latest released version of couchapp:

::

    $ sudo pip install couchapp
    $ sudo pip install --upgrade couchapp

To install/upgrade development version:

::

    $ sudo pip install git+https://github.com/couchapp/couchapp.git


Installing in a sandboxed environment
-------------------------------------

If you want to work in a sandboxed environment, which is recommended if
you don't want to *pollute* your system, you can use `virtualenv
<http://pypi.python.org/pypi/virtualenv>`_ ::

    $ curl -O https://bootstrap.pypa.io/get-pip.py
    $ sudo python get-pip.py
    $ sudo pip install virtualenv

To create a sandboxed environment in ``couchapp_env`` folder,
activate and work in this environment::

    $ cd /where/the/sandbox/live
    $ virtualenv couchapp_env
    $ source couchapp_env/bin/activate

Then to install couchapp::

    $ pip install couchapp

Then you can work on your CouchApps. I usually have a ``couchapps``
folder in ``couchapp_env`` where I put my couchapps.


Installing on Mac OS X
----------------------

.. warning::
    This section is out-of-date.
    We need you help for testing on newer OSX with newer ``couchapp.py``


Using CouchApp Standalone executable
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Download
`couchapp-1.0.0-macosx.zip
<https://github.com/downloads/couchapp/couchapp/couchapp-1.0.0-macosx.zip>`_
on `Github <http://github.com/>`_ then double-click on the installer.


Using `Homebrew`_
~~~~~~~~~~~~~~~~~

.. _Homebrew: http://brew.sh/

To install easily couchapp on Mac OS X, it may be easier to use
`Homebrew`_ to install ``pip``.

Once you installed `Homebrew`_,
issue ``brew search pip`` and will get following message:

    Homebrew provides pip via: `brew install python`. However you will then
    have two Pythons installed on your Mac, so alternatively you can install
    pip via the instructions at:
    https://pip.readthedocs.io/en/stable/instal

I will recommend that just install python from `Homebrew`_,
because you will usually get a newer version of python than system base's::

    $ brew install python

And let's check the installation of python::

    $ where python
    /usr/local/bin/python
    /usr/bin/python

    $ where pip
    /usr/local/bin/pip

The path prefixed with ``/usr/local/`` is from `Homebrew`_.
Everythings look fine, and issue::

    $ pip install couchapp

``pip`` will install packages into
``~/Library/Python/2.7/lib/python/site-packages`` usually.
Also you can verify the location via::

    $ pip show --files couchapp

Now, the executable is here::

    ~/Library/Python/2.7/bin/couchapp

Don't forget to add ``~/Library/Python/2.7/bin`` to your ``PATH``.
There is more discussion about installation on macOS, please checkout
`issue 240 <https://github.com/couchapp/couchapp/pull/240>`_ for
more information.


Installing on Debian/Ubuntu
---------------------------

There is a package in Debian repository.
Thanks to `@gfa <https://github.com/gfa>`_!

::

    sudo apt-get update
    sudo apt-get install couchapp


Installing on Windows
---------------------
There are currently 2 methods to install on windows:

-  `Standalone Executable
   1.0.2 <https://github.com/couchapp/couchapp/releases/download/1.0.2/couchapp-1.0.2-win32.exe>`_
   Does not require Python
-  `Python installer for Python 2.7 <windows-python-installers.md>`_
   Requires Python


Previous Release
----------------

Please check out both `release section
<https://github.com/couchapp/couchapp/releases>`_ and
`download section
<https://github.com/couchapp/couchapp/downloads>`_
in GitHub.

Note that the download section in GitHub is `deprecated
<https://github.com/blog/1302-goodbye-uploads>`_.
