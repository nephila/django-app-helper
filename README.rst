================
djangocms-helper
================

.. image:: https://img.shields.io/pypi/v/djangocms-helper.svg?style=flat-square
    :target: https://pypi.python.org/pypi/djangocms-helper
    :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/dm/djangocms-helper.svg?style=flat-square
    :target: https://pypi.python.org/pypi/djangocms-helper
    :alt: Monthly downloads

.. image:: https://img.shields.io/pypi/pyversions/djangocms-helper.svg?style=flat-square
    :target: https://pypi.python.org/pypi/djangocms-helper
    :alt: Python versions

.. image:: https://img.shields.io/travis/nephila/djangocms-helper.svg?style=flat-square
    :target: https://travis-ci.org/nephila/djangocms-helper
    :alt: Latest Travis CI build status

.. image:: https://img.shields.io/coveralls/nephila/djangocms-helper/master.svg?style=flat-square
    :target: https://coveralls.io/r/nephila/djangocms-helper?branch=master
    :alt: Test coverage

.. image:: https://img.shields.io/codecov/c/github/nephila/djangocms-helper/master.svg?style=flat-square
    :target: https://codecov.io/github/nephila/djangocms-helper
    :alt: Test coverage

.. image:: https://codeclimate.com/github/nephila/djangocms-helper/badges/gpa.svg?style=flat-square
   :target: https://codeclimate.com/github/nephila/djangocms-helper
   :alt: Code Climate

****************************************
Helper for django CMS plugin development
****************************************

djangocms-helper is a set of commands to handle django CMS plugins development
process.

It's a modified version of django CMS's own ``develop.py`` script, modified
to handle generic plugins development process.

Supported versions
==================

Python: 2.6, 2.7, 3.3, 3.4, 3.5

Django: 1.6 to 1.9

django CMS: 3.0 to 3.2

.. warning:: Starting from version 1.0, compatibily with Python 2.6, Python 3.3, Django<=1.7 and
             django CMS<=3.1 will be dropped. Pin your test requirements accordingly
             (``djangocms-helper<1.0``).

Common options
==============

* ``--cms``: Loads configuration to properly run a django CMS-based application;
* ``--extra-settings``: Path to a helper file to set extra settings; see
  `Settings section <http://djangocms-helper.readthedocs.org/en/develop/settings.html>`_
  for details;

*****
Usage
*****

The command **must** be executed in the main plugin directory (i.e. in the same
directory as the ``setup.py`` file) as it needs to import files relative to the
current directory.

The basic command structure is::

    djangocms-helper <application> <command> [options ...]

where **<application>** is the django application name and **<command>** is one
of the available commands. Options vary for each command.

*************
Bootstrapping
*************

To bootstrap a project using ``djangocms-helper`` you may want to have a look at `cookiecutter-djangopackage-helper <https://github.com/nephila/cookiecutter-djangopackage-helper>`_, a `cookiecutter <https://github.com/audreyr/cookiecutter>`_ template for ``djangocms-helper``.

To use it follows `usage instructions <https://github.com/nephila/cookiecutter-djangopackage-helper#usage>`_

******
Runner
******

By using the integrated runned in the settings file you'll be able to run
the commands without invoking ``djangocms-helper``: see
`Integrate runner <http://djangocms-helper.readthedocs.org/en/develop/runner.html>`_
for reference.

************
Installation
************

Installing from pip::

    pip install djangocms-helper

Installing from source::

    pip install git+https://github.com/nephila/djangocms-helper#egg=djangocms-helper

Requirements
============

* django CMS 3.0 (django CMS 3.0.4 is required for pyflake command), optional; required only
  to work with ``--cms`` option
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
`django CMS's <https://github.com/divio/django-cms>`_ own `develop.py` so all the contributors
deserve a huge thanks for their work.

