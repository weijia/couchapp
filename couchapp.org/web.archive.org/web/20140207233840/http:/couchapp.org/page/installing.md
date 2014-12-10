# **[CouchApp.org](/web/20140209095238/http://couchapp.org/page/index):**
[Installing CouchApp](/web/20140209095238/http://couchapp.org/page/installing)

## Installing

The newest install instructions are always in the [README](/web/20140209095238
/https://github.com/couchapp/couchapp/blob/master/README.rst)

## Requirements

  * Python 2.x >= 2.5 (Python 3.x will be supported soon)
  * the header files of the Python version that is used, which are included e.g. in the according development package `python-dev` (may have a different name depending on your system)

## Installing on all UNIXs

To install couchapp using easy_install you must make sure you have a recent
version of distribute installed:

    
    
    $ curl -O http://python-distribute.org/distribute_setup.py
    $ sudo python distribute_setup.py
    $ sudo easy_install pip
    

To install or upgrade to the latest released version of couchapp:

    
    
    $ sudo pip install couchapp
    $ sudo pip install --upgrade couchapp
    

To install/upgrade development version :

    
    
    $ sudo pip install git+http://github.com/couchapp/couchapp.git#egg=Couchapp
    

## Installing in a sandboxed environnement.

If you want to work in a sandboxed environnement which is recommended if you
don't want to not "pollute" your system, you can use
[virtualenv](/web/20140209095238/http://pypi.python.org/pypi/virtualenv) :

    
    
    $ curl -O http://python-distribute.org/distribute_setup.py
    $ sudo python distribute_setup.py
    $ easy_install pip
    $ pip install virtualenv
    

Then to install couchapp :

    
    
    $ pip -E couchapp_env install couchapp
    

This command create a sandboxed environment in `couchapp_env` folder. To
activate and work in this environment:

    
    
    $ cd couchapp_env && . ./bin/activate
    

Then you can work on your couchapps. I usually have a `couchapps` folder in
`couchapp_env` where I put my couchapps.

## Installing from source :

Follow instructions [here](/web/20140209095238/http://couchapp.org/page
/installing-from-source)

## Installing on Mac OS X

### Using CouchApp Standalone executable :

Download [Couchapp-0.8.1-macosx.zip](/web/20140209095238/https://github.com/do
wnloads/couchapp/couchapp/couchapp-0.8.1-macosx.zip) on
[Github](/web/20140209095238/http://github.com/) then double-click on the
installer.

### Using the Python metapackage for Mac OS X 10.5 or Mac OS X 10.6

  * For Mac OS X 10.6: Download [Couchapp-0.7.5-py2.6-macosx10.6.zip](/web/20140209095238/https://github.com/downloads/couchapp/couchapp/Couchapp-0.7.5-py2.6-macosx10.6.zip) then double-click on the installer.

  * For Mac OS X 10.5: Download [Couchapp-0.7.5-py2.5-macosx10.5.zip](/web/20140209095238/https://github.com/downloads/couchapp/couchapp/Couchapp-0.7.5-py2.5-macosx10.5.zip) .

### Using Homebrew

To install easily couchapp on Mac OS X, it may be easier to use
[Homebrew](/web/20140209095238/http://github.com/mxcl/homebrewbrew) to install
`pip`.

Once you [installed Homebrew](/web/20140209095238/http://wiki.github.com/mxcl/
homebrew/installation), do :

    
    
    $ brew install pip
    $ env ARCHFLAGS="-arch i386 -arch x86_64" pip install couchapp
    

## Installing on Ubuntu

If you use [Ubuntu](http://www.ubuntu.com/-, you can update your system with
packages from our PPA by adding `ppa:couchapp/couchapp` to your system's
Software Sources.

Follow **instructions**
[here](/web/20140209095238/https://launchpad.net/~couchapp/+archive/couchapp).

## Installing on Windows

There are currently 2 methods to install on windows:

  * [Standalone Executable 0.8.1](/web/20140209095238/https://github.com/downloads/couchapp/couchapp/couchapp-0.8.1-win.zip) Does not require Python
  * [Python installer for Python 2.7](/web/20140209095238/http://couchapp.org/page/windows-python-installers) Requires Python

In case the above is not updated, check out the [downloads
section](/web/20140209095238/https://github.com/couchapp/couchapp/downloads)
in GitHub

## Example:

Files attached to _Installing CouchApp_:

  * [Couchapp-0.7-Installer-screenshot.png](/web/20140209095238/http://couchapp.org/pages/installing/Couchapp-0.7-Installer-screenshot.png) (image/png)

