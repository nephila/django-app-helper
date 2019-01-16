================
djangocms-helper
================

|Gitter| |PyPiVersion| |PyVersion| |Status| |TestCoverage| |CodeClimate| |License|

******************************************
Helper for django applications development
******************************************

djangocms-helper is a set of commands and helper methods
to make developing and testing reusable Django applications easier.

Being born in the django CMS ecosystem, it provides a lot of utility
functions to develop, run and test django CMS applications.

It's a modified version of django CMS's own ``develop.py`` script, modified
to handle generic application development process.

Supported versions
==================

Python: 2.7, 3.5, 3.6, 3.7

Django: 1.11, 2.0, 2.1

django CMS: 3.4, 3.5, 3.6

Newer versions might work but are not tested yet.

.. warning:: Starting from version 1.2, compatibility with Python 3.4, Django<=1.11 and
             django CMS<=3.4 has been dropped. Pin your test requirements accordingly
             (``djangocms-helper<1.2``).

.. warning:: Starting from version 1.1, nose test runner has been dropped.
             Pin your test requirements accordingly (``djangocms-helper<1.0``).

Common options
==============

* ``--cms``: Loads configuration to properly run a django CMS-based application;
* ``--extra-settings``: Path to a helper file to set extra settings; see
  `Settings section <https://djangocms-helper.readthedocs.io/en/develop/settings.html>`_
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

Base test class
===============

A base test class is available to provide helpers and methods that
implements repetitive tasks during development or compatibility shims
(especially for django CMS).

.. warning:: Changes in version 1.2 **might** reduce the number of queries executed in tests
             rendering plugins.

             If you are using ``assertNumQueries`` (or similar), this may
             yield unexpected failures.

             Please check your code before upgrading djangocms-helper.

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
`Integrate runner <https://djangocms-helper.readthedocs.io/en/develop/runner.html>`_
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

* django CMS optional; required only to work with ``--cms`` option
* docopt
* tox
* dj-database-url

*************
Documentation
*************

Documentation is available on `readthedocs <https://djangocms-helper.readthedocs.io>`_.


*******
Authors
*******

``djangocms-helper`` was written by `Iacopo Spalletti <i.spalletti@nephila.it>`_ with help from
other contributors.

Thanks
======

The general logic and part of the code of the whole application is heavily taken from
`django CMS's <https://github.com/divio/django-cms>`_ own ``develop.py`` so all the contributors
deserve a huge thanks for their work.



.. |Gitter| image:: https://img.shields.io/badge/GITTER-join%20chat-brightgreen.svg?style=flat-square
    :target: https://gitter.im/nephila/applications
    :alt: Join the Gitter chat

.. |PyPiVersion| image:: https://img.shields.io/pypi/v/djangocms-helper.svg?style=flat-square
    :target: https://pypi.python.org/pypi/djangocms-helper
    :alt: Latest PyPI version

.. |PyVersion| image:: https://img.shields.io/pypi/pyversions/djangocms-helper.svg?style=flat-square
    :target: https://pypi.python.org/pypi/djangocms-helper
    :alt: Python versions

.. |Status| image:: https://img.shields.io/travis/nephila/djangocms-helper.svg?style=flat-square
    :target: https://travis-ci.org/nephila/djangocms-helper
    :alt: Latest Travis CI build status

.. |TestCoverage| image:: https://img.shields.io/coveralls/nephila/djangocms-helper/master.svg?style=flat-square
    :target: https://coveralls.io/r/nephila/djangocms-helper?branch=master
    :alt: Test coverage

.. |License| image:: https://img.shields.io/github/license/nephila/djangocms-helper.svg?style=flat-square
   :target: https://pypi.python.org/pypi/djangocms-helper/
    :alt: License

.. |CodeClimate| image:: https://codeclimate.com/github/nephila/djangocms-helper/badges/gpa.svg?style=flat-square
   :target: https://codeclimate.com/github/nephila/djangocms-helper
   :alt: Code Climate
