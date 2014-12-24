================
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
        :alt: Monthly downloads

.. image:: https://coveralls.io/repos/nephila/djangocms-helper/badge.png
        :target: https://coveralls.io/r/nephila/djangocms-helper
        :alt: Test coverage

****************************************
Helper for django CMS plugin development
****************************************

djangocms-helper is a set of commands to handle django CMS plugins development
process.

It's a modified version of django CMS's own ``develop.py`` script, modified
to handle generic plugins development process.


Common options
==============

* ``--cms``: Loads configuration to properly run a django CMS-based application;
* ``--extra-settings``: Path to a helper file to set extra settings; see
  `Customizing settings`_ for details;

*****
Usage
*****

The command **must** be executed in the main plugin directory (i.e. in the same
directory as the ``setup.py`` file) as it needs to import files relative to the
current directory.

The basic command structure is::

    djangocms-helper <application> <command> [options ...]

where **<application>** is the django application name and **<command>** is one
of the available commands. Optins vary for each command.

************
Installation
************

Installing from pip::

    pip install djangocms-helper

Installing from source::

    pip install git+https://github.com/nephila/djangocms-helper#egg=djangocms-helper

Requirements
============

* django CMS 3.0 (django CMS 3.0.4 is required for pyflake command)
* docopt
* tox
* dj-database-url

*************
Documentation
*************

Documentation is available on `readthedocs <http://djangocms-helper.readthedocs.org>`_.


*******
Authors
*******

`djangocms-helper` was written by `Iacopo Spalletti <i.spalletti@nephila.it>`_ with help from
other contributors.

Thanks
======

The general logic and part of the code of the whole application is heavily taken from
`django CMS's <https://github.com/divio/django-cms`_ own `develop.py` so all the contributors
 deserve a huge thanks for their work.
