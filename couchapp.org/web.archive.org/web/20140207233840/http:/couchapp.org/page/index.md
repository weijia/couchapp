# **[CouchApp.org](/web/20140207233840/http://couchapp.org/page/index):**
[Simple JavaScript application hosted in Apache
CouchDB](/web/20140207233840/http://couchapp.org/page/index)

**CouchApps are JavaScript and HTML5 applications served directly from CouchDB. If you can fit your application into those constraints, then you get CouchDB's scalability and flexibility "for free" (and deploying your app is as simple as replicating it to the production server).**

The original CouchApp command-line tools were created in 2008 / 2009 by
@benoitc and @jchris. They still work, and have been feature complete for a
long time. Couchapp has been replaced and is compatible with the old couchapp
tool. There are also new tools for deploying browser-based apps to JSON web
servers and I think [PouchDB](/web/20140207233840/http://pouchdb.com/) is the
future of browser based sync apps. It can sync with the same sync protocols
but uses the built-in storage of HTML5.

## Get Started

  * [What the HTTP is CouchApp?](/web/20140207233840/http://couchapp.org/page/what-is-couchapp)
  * The [Standalone Applications](/web/20140207233840/http://guide.couchdb.org/editions/1/en/standalone.html) and [Managing Design Documents](/web/20140207233840/http://guide.couchdb.org/editions/1/en/managing.html) chapters of the O'Reilly CouchDB book
  * [Getting Started Tutorial](/web/20140207233840/http://couchapp.org/page/getting-started)
  * [Video Tutorials and Screencasts](/web/20140207233840/http://couchapp.org/page/videos)
  * [Help with installing and running individual applications](/web/20140207233840/http://couchapp.org/page/application-help)
  * [Using backbone.js in CouchApps](/web/20140207233840/http://couchapp.org/page/backbone)

## CouchApp Development Tools

To develop a CouchApp, you will need a way to get your javascript, html and
other resources onto your CouchDB instance. Typically this is done with a
CouchApp command line tool that maps application assets and CouchDB views,
lists, shows, etc into one or more Design Documents.

  * [CouchApp Filesystem Mapping](/web/20140207233840/http://couchapp.org/page/filesystem-mapping) \- couchapp.py and erica (mentioned below) implement a consistent filesystem-to-design-document mapping

### Curl

The simplest way to develop a couchapp would be to use curl from the command
line.

### [CouchApp](/web/20140207233840/http://couchapp.org/page/couchapp-python)
command line tool (python)

The [CouchApp](/web/20140207233840/http://couchapp.org/page/couchapp-python)
command line tool is used to generate code templates in your application and
to push your changes to an instance of couchdb, among other things. Here is
how to get started with the CouchApp command line tool:

  * [Installing couchapp](/web/20140207233840/http://couchapp.org/page/installing)
  * [Couchapp configuration](/web/20140207233840/http://couchapp.org/page/couchapp-config)
  * [The couchapp command line tool](/web/20140207233840/http://couchapp.org/page/couchapp-usage)
  * [Extending the couchapp command line tool](/web/20140207233840/http://couchapp.org/page/couchapp-extend)
  * [Using couchapp with multiple design documents](/web/20140207233840/http://couchapp.org/page/multiple-design-docs)

There can be confusion with the term 'CouchApp' because it can refer to this
tool, named 'CouchApp', or a general application served from CouchDB. This is
probably due to the fact that the CouchApp command line tool was the first
full way of developing a CouchApp.

### CouchApp command line tool (node.couchapp.js)

  * [https://github.com/mikeal/node.couchapp.js](/web/20140207233840/https://github.com/mikeal/node.couchapp.js)
  * [http://japhr.blogspot.com/2010/04/quick-intro-to-nodecouchappjs.html](/web/20140207233840/http://japhr.blogspot.com/2010/04/quick-intro-to-nodecouchappjs.html)

This is an alternative tooling to the Python couchapp utility that is instead
written in Node.js. It uses a much simpler folder structure than it's Python
counterpart and is a generally more minimalist/simplified way of writing
couchapps. Note that you cannot use Python couchapp to push couchapps written
using node.couchapp.js into Couch and vice versa.

### erica

[erica](/web/20140207233840/https://github.com/benoitc/erica) is an Erlang-
based command line tool that is compatible with the Python and Node.js
"couchapp" tools.

### Kanso

A comprehensive, framework-agnostic build tool for CouchApps.

The Kanso command-line tool can build projects designed for node.couchapp.js,
or even the Python couchapp tool, while providing many other options for
building your app. These build steps and other code can be shared using the
online [package repository](/web/20140207233840/http://kan.so/packages).
Compiling coffee-script, .less CSS templates etc. is as easy as including the
relevant package.

**"NPM for CouchApps"**

Kanso also lets you merge design docs together, which allows reusable
components built with any of the available couchapp tools. The Kanso tool can
help you manage dependencies and share code between projects, as well as
providing a library of JavaScript modules for use with CouchDB.

[Kanso Homepage](/web/20140207233840/http://kan.so/)

### soca

soca is a command line tool written in ruby for building and pushing
couchapps. It is similar to the canonical couchapp python tool, with a number
of key differences:

  * local directories do not have to map 1-1 to the design docs directory
  * lifecycle management & deployment hooks for easily adding or modifying the design document with ruby tools or plugins.
  * architected around using Sammy.js, instead of Evently, which is bundled with the python tool. Sammy.js is a Sinatra inspired browser-side RESTframework which is used by default.

Unlike a traditional couchapp, a soca couchapp is one way - your source
directory structure is actually 'compiled' into into the couchapp _design
document format.

_compile time plugins:_

  * Compass
  * CoffeeScript
  * Mustache
  * JavaScript bundling for CouchDB and the browser

[soca on Github](/web/20140207233840/https://github.com/quirkey/soca)

### Reupholster

Reupholster is geared for CouchApp beginners and simple CouchApps. What
reupholster does is allows you to experience writing a CouchApp as fast as
possible, with very little learning curve. It just feels like you are editing
a normal web project.

[Reupholster Homepage](/web/20140207233840/http://reupholster.iriscouch.com/re
upholster/_design/app/index.html)

## Javascript Application Programming

All application logic in a couchapp is provided by Javascript. There is a
library called [jquery.couch.js](/web/20140207233840/https://github.com/apache
/couchdb/blob/trunk/share/www/script/jquery.couch.js) that is distributed with
every CouchDB installation. Here is the [documentation for
jquery.couch.js](/web/20140207233840/http://daleharvey.github.com/jquery.couch
.js-docs/symbols/index.html)

### Example Applications

You can download the following applications and try them out yourself.

#### [Pages](/web/20140207233840/https://github.com/couchone/pages)

The wiki software behind couchapp.org

  * [Installing Pages](/web/20140207233840/http://couchapp.org/page/pages-install)
  * [Pages Application Walkthrough](/web/20140207233840/http://couchapp.org/page/NotesOnPagesFiles)

#### [online](/web/20140207233840/http://t.co/tiUI2dBt7l)

A couchapp for keeping teams on the same page

#### [Sofa](/web/20140207233840/https://github.com/jchris/sofa)

Standalone CouchDB Blog, used by the O'Reilly CouchDB book (note: sofa does
not work as well with couchdb 1.0.1 or 1.0.2, the edit and create new pages do
not work. Also, there is a different version of mustache.js in the
/design_doc_name/lib directory that is used to render all the _list functions.
The normal mustache.js file is in the vendor/couchapp directory. )

#### [TweetEater](/web/20140207233840/https://github.com/doppler/TweetEater)

A Couchapp which displays tweets harvested from Twitter's streaming API by an
accompanying Ruby program.

## Other resources

  * [Search The CouchDB Mailing List/IRC Archive](/web/20140207233840/http://archive.couchdb.org/)
  * [A List of CouchApps](/web/20140207233840/http://couchapp.org/page/list-of-couchapps)
  * [CouchApps with DesktopCouch](/web/20140207233840/http://couchapp.org/page/desktopcouch)
  * [Roadmap](/web/20140207233840/http://couchapp.org/page/roadmap)
  * [Mailing List](/web/20140207233840/http://groups.google.com/group/couchapp)
  * [Contributing to CouchApp](/web/20140207233840/http://couchapp.org/page/how-to-contribute)
  * [Some development notes](/web/20140207233840/http://couchapp.org/page/development-notes)
  * [The CouchApp Garden project](/web/20140207233840/http://couchapp.org/page/garden)
  * [eNotes CouchApp Tutorial](/web/20140207233840/http://materials.geoinfo.tuwien.ac.at/tutorials/couchapp)

Files attached to _Simple JavaScript application hosted in Apache CouchDB_:

  * [390460_185903128166121_700165246_n.jpg](/web/20140207233840/http://couchapp.org/pages/index/390460_185903128166121_700165246_n.jpg) (image/jpeg)
  * [N68-VS3 UCC.pdf](/web/20140207233840/http://couchapp.org/pages/index/N68-VS3%20UCC.pdf) (application/pdf)
  * [mike wazowski.jpg](/web/20140207233840/http://couchapp.org/pages/index/mike%20wazowski.jpg) (image/jpeg)
  * [demo.html](/web/20140207233840/http://couchapp.org/pages/index/demo.html) (text/html)
  * [acralyzer-master.zip](/web/20140207233840/http://couchapp.org/pages/index/acralyzer-master.zip) (application/octet-stream)
  * [untitled.txt](/web/20140207233840/http://couchapp.org/pages/index/untitled.txt) (text/plain)
  * [multiple_design_documents](/web/20140207233840/http://couchapp.org/pages/index/multiple_design_documents) (application/octet-stream)
  * [multiple_design_documents.html](/web/20140207233840/http://couchapp.org/pages/index/multiple_design_documents.html) (text/html)
  * [couchapp_blog_entry.txt](/web/20140207233840/http://couchapp.org/pages/index/couchapp_blog_entry.txt) (text/plain)

