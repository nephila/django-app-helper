#################
django CMS Helper
#################


django-app-helper is a set of commands and helper methods
to make developing and testing reusable Django applications easier.

Being born in the django CMS ecosystem, it provides a lot of utility
functions to develop, run and test django CMS applications.

It's a modified version of django CMS's own `develop.py` script, and it allows
to develop applications without having a full project
- which is not always possible or convenient - set up.

It does this by spawning its own virtual project
- a basic generic project built in to itself -
that's ready to integrate with your application with just
a little extra configuration.

The utilities provided:

* help setting up and running tests
* give you access to a Django shell
* run the Django check command
* compile and update locale message
* help manage Django and South migrations
* perform static analysis using pyflakes
* build an authors list automatically
* setting up a Django environment

django CMS Helper was created by Iacopo Spalletti.

============
Installation
============

Installing from pip::

    pip install django-app-helper

or::

    pip install django-app-helper[cms]

to install it along with django CMS

Installing from source::

    pip install git+https://github.com/nephila/django-app-helper#egg=django-app-helper

============
Requirements
============

* django CMS 3.0 (django CMS 3.0.4 is required for pyflake command), optional;
  required only to work with ``--cms`` option
* docopt
* tox
* dj-database-url

.. warning:: Since version 0.7 django CMS is no more a hard dependency; install it
             manually to enable ``--cms`` option


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
