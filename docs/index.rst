#################
django CMS Helper
#################

django CMS Helper is a set of commandline utilities to help developers of Django applications.

Being born in the `django CMS <http://django-cms.org>`_ ecosystem it has an informed approach
to testing django CMS applications, but without any attempt at **forcing** them.

It's a modified version of django CMS's own ``develop.py`` script, allowing you to work with your
application even without having a full project - which is not always possible or convenient - set
up.

It does this by spawning its own virtual project - a basic generic project built in to itself -
that's ready to integrate with your application with just a little extra configuration.

Commands provided:

* give you access to a Django shell
* run the Django check command
* compile and update locale message
* help manage Django and South migrations
* perform static analysis using pyflakes
* build an authors list automatically

Features available in test cases:

* help setting up and running tests
* provides a robust and flexible wat to create ``request`` objects
* tries to guess migration modules layout for some *known* applications
* enables ``faulthandler`` if available

django CMS Helper was created by Iacopo Spalletti.

============
Installation
============

Installing from pip::

    pip install djangocms-helper

or::

    pip install djangocms-helper[cms]

to install it along with django CMS

Installing from source::

    pip install git+https://github.com/nephila/djangocms-helper#egg=djangocms-helper

============
Requirements
============

* django CMS 3.0 (django CMS 3.0.4 is required for pyflake command), optional;
  required only to work with ``--cms`` option
* docopt
* tox
* dj-database-url


.. toctree::
   :maxdepth: 2

   introduction
   reference
   settings
   runner
   basetest
   development
   contributing
   history
