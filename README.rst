=================
Django App helper
=================

|Gitter| |PyPiVersion| |PyVersion| |GAStatus| |TestCoverage| |CodeClimate| |License|

.. warning::
    Starting from 3.3 django-app-helper only supports Django 3.2+ and django CMS 3.11. If you need support for older (unsupported) versions, use django-app-helper<3.3

    Starting from 3 django-app-helper only supports Django 2.2+ and django CMS 3.7+. If you need support for older (unsupported) versions, use django-app-helper 2.

    Django 5.0 support exclude django CMS 3.11 support, as django CMS 3.11 doesn't yet support Django 5.0.

******************************************
Helper for django applications development
******************************************

django-app-helper is a set of commands and helper methods
to make developing and testing reusable Django applications easier.

Being born in the django CMS ecosystem, it provides a lot of utility
functions to develop, run and test django CMS applications.

It's a modified version of django CMS's own ``develop.py`` script, modified
to handle generic application development process.

It supports both tests writted using Django ``TestCase`` and pytest ones
(see `pytest support`_).

Supported versions
==================

Python: 3.8, 3.9, 3.10, 3.11, 3.12

Django: 3.2, 4.0, 4.1, 4.2, 5.0

django CMS: 3.11

Newer versions might work but are not tested yet.

Common options
==============

* ``--cms``: Loads configuration to properly run a django CMS-based application;
* ``--extra-settings``: Path to a helper file to set extra settings; see
  `Project settings with Django App Helper`_ for details;

*****
Usage
*****

The command **must** be executed in the main plugin directory (i.e. in the same
directory as the ``setup.py`` file) as it needs to import files relative to the
current directory.

The basic command structure is::

    django-app-helper <application> <command> [options ...]

where **<application>** is the django application name and **<command>** is one
of the available commands. Options vary for each command.

Base test class
===============

A base test class is available to provide helpers and methods that
implements repetitive tasks during development or compatibility shims
(especially for django CMS).

*************
Bootstrapping
*************

To bootstrap a project using ``django-app-helper`` you may want to have a look at `cookiecutter-djangopackage-helper`_, a `cookiecutter`_ template for ``django-app-helper``.

To use it follows `usage`_

******
Runner
******

By using the integrated runned in the settings file you'll be able to run
the commands without invoking ``django-app-helper``: see `Integrated runner`_
for reference.

***************
ASGI / Channels
***************

ASGI / Channels are supported by installing the project with ``django-app-helper[async]``.

With Daphne / Channels installed you can run ``django-app-helper server --use-daphne|--use-channels`` to run the
project on ASGI.

See `ASGI / Channels support`_

Pure ASGI support is available only for Django 3.0+.

************
Installation
************

Installing from pip::

    pip install django-app-helper

Installing from source::

    pip install git+https://github.com/nephila/django-app-helper#egg=django-app-helper

Requirements
============

* django CMS optional; required only to work with ``--cms`` option
* docopt
* tox
* dj-database-url

*************
Documentation
*************

Documentation is available on `readthedocs`_.


*******
Authors
*******

``django-app-helper`` was written by `Iacopo Spalletti <i.spalletti@nephila.digital>`_ with help from
other contributors.

Thanks
======

The general logic and part of the code of the whole application is heavily taken from
`django CMS's`_ own ``develop.py`` so all the contributors
deserve a huge thanks for their work.



.. |Gitter| image:: https://img.shields.io/badge/GITTER-join%20chat-brightgreen.svg?style=flat-square
    :target: https://gitter.im/nephila/applications
    :alt: Join the Gitter chat

.. |PyPiVersion| image:: https://img.shields.io/pypi/v/django-app-helper.svg?style=flat-square
    :target: https://pypi.python.org/pypi/django-app-helper
    :alt: Latest PyPI version

.. |PyVersion| image:: https://img.shields.io/pypi/pyversions/django-app-helper.svg?style=flat-square
    :target: https://pypi.python.org/pypi/django-app-helper
    :alt: Python versions

.. |GAStatus| image:: https://github.com/nephila/django-app-helper/workflows/Tox%20tests/badge.svg
    :target: https://github.com/nephila/django-app-helper
    :alt: Latest CI build status

.. |TestCoverage| image:: https://img.shields.io/coveralls/nephila/django-app-helper/master.svg?style=flat-square
    :target: https://coveralls.io/r/nephila/django-app-helper?branch=master
    :alt: Test coverage

.. |License| image:: https://img.shields.io/github/license/nephila/django-app-helper.svg?style=flat-square
   :target: https://pypi.python.org/pypi/django-app-helper/
    :alt: License

.. |CodeClimate| image:: https://codeclimate.com/github/nephila/django-app-helper/badges/gpa.svg?style=flat-square
   :target: https://codeclimate.com/github/nephila/django-app-helper
   :alt: Code Climate

.. _Migrating from djangocms-helper to django-app-helper: https://django-app-helper.readthedocs.io/en/latest/migrating.html
.. _Project settings with Django App Helper: https://django-app-helper.readthedocs.io/en/latest/settings.html
.. _Integrated runner: https://django-app-helper.readthedocs.io/en/latest/runner.html
.. _cookiecutter: https://github.com/audreyr/cookiecutter
.. _cookiecutter-djangopackage-helper: https://github.com/nephila/cookiecutter-djangopackage-helper
.. _readthedocs: https://django-app-helper.readthedocs.io
.. _django CMS's: https://github.com/divio/django-cms:
.. _usage: https://github.com/nephila/cookiecutter-djangopackage-helper#usage
.. _pytest support: https://django-app-helper.readthedocs.io/en/latest/pytest.html
.. _ASGI / Channels support: https://django-app-helper.readthedocs.io/en/latest/asgi.html
