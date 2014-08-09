djangocms-helper
================

.. image:: https://pypip.in/v/djangocms-helper/badge.png
        :target: https://pypi.python.org/pypi/djangocms-helper
        :alt: Latest PyPI version

.. image:: https://travis-ci.org/nephila/djangocms-helper.png?branch=master
        :target: https://travis-ci.org/nephila/djangocms-helper
        :alt: Latest Travis CI build status

.. image:: https://pypip.in/d/djangocms-helper/badge.png
        :target: https://pypi.python.org/pypi/djangocms-helper
        :alt: Montly downloads


Helper for django CMS plugin development
----------------------------------------

djangocms-helper is a set of commands to handle django CMS plugins development
process.

It's a modified version of django CMS's own ``develop.py`` script, modified
to handle generic plugins development process.

Usage
-----

The command **must** be executed in the main plugin directory (i.e. in the same
directory as the ``setup.py`` file) as it needs to import files relative to the
current directory.

The basic command structure is::

    djangocms-helper <application> <command> [options ...]

where **<application>** is the django application name and **<command>** is one
of the available commands. Optins vary for each command.

Available commands
^^^^^^^^^^^^^^^^^^

test
====

Test command allows to run the application test suite using a setup similar to
the django CMS testsuite.
It requires that tests are included in ``application.tests`` module and imported
from the ``tests`` module; modules into ``tests`` directory must be named
**test_foo**.

application.tests.__init__.py::


    from .test_one import *
    from .test_two import *

application.tests.test_one.py::

    class MyTests(TestCase):

        def test_foo(self):
            pass

        def test_bar(self):
            pass


shell
=====

Starts a django shell for the test project.

compilemessages
===============

Compiles the locale messages.

makemessages
============

Updates the locale messages for the current application.

makemigrations
==============

Updates the application migrations (south migrations or Django migrations
according to the current installed Django version). For South, it automatically
handles **initial** / **auto** options.

pyflakes
========

Performs static analysis using pyflakes with the same configuration as django CMS.

authors
=======

Generates the authors list from the git log suitable for the **AUTHORS** file.

Installation
------------

Installing from pip::

    pip install djangocms-helper

Installing from source::

    pip install git+https://github.com/nephila/djangocms-helper#egg=djangocms-helper

Requirements
^^^^^^^^^^^^

* django CMS 3.0 (django CMS 3.0.4 is required for pyflake command)
* docopt
* tox
* dj-database-url

Authors
-------

`djangocms-helper` was written by `Iacopo Spalletti <i.spalletti@nephila.it>`_.
