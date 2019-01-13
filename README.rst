=================
django-app-helper
=================

|Gitter| |PyPiVersion| |PyVersion| |Status| |TestCoverage| |CodeClimate| |License|

******************************************
Helper for django applications development
******************************************

django-app-helper is a set of commands and helper methods
to make developing and testing reusable Django applications easier.

Being born in the django CMS ecosystem, it provides a lot of utility
functions to develop, run and test django CMS applications.

It's a modified version of django CMS's own ``develop.py`` script, modified
to handle generic application development process.

Supported versions
==================

Python: 2.7, 3.5, 3.6, 3.7

Django: 1.11 to 2.1

django CMS: 3.4, 3.5, 3.6

.. warning:: Starting from version 1.1, compatibily nose test runner has been dropped.
             Pin your test requirements accordingly (``djangocms-helper<1.0``).

.. warning:: Starting from version 1.2, compatibily with Python 3.4, Django<=1.11 and
             django CMS<=3.4 has been dropped. Pin your test requirements accordingly
             (``djangocms-helper<1.2``).

Common options
==============

* ``--cms``: Loads configuration to properly run a django CMS-based application;
* ``--extra-settings``: Path to a helper file to set extra settings; see
  `Settings section <https://django-app-helper.readthedocs.io/en/develop/settings.html>`_
  for details;

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

*************
Bootstrapping
*************

To bootstrap a project using ``django-app-helper`` you may want to have a look at `cookiecutter-djangopackage-helper <https://github.com/nephila/cookiecutter-djangopackage-helper>`_, a `cookiecutter <https://github.com/audreyr/cookiecutter>`_ template for ``django-app-helper``.

To use it follows `usage instructions <https://github.com/nephila/cookiecutter-djangopackage-helper#usage>`_

******
Runner
******

By using the integrated runned in the settings file you'll be able to run
the commands without invoking ``django-app-helper``: see
`Integrate runner <https://django-app-helper.readthedocs.io/en/develop/runner.html>`_
for reference.

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

Documentation is available on `readthedocs <https://django-app-helper.readthedocs.io>`_.


*******
Authors
*******

<<<<<<< HEAD
``djangocms-helper`` was written by `Iacopo Spalletti <i.spalletti@nephila.it>`_ with help from
=======
`django-app-helper` was written by `Iacopo Spalletti <i.spalletti@nephila.it>`_ with help from
>>>>>>> Rename app to django app helper
other contributors.

Thanks
======

The general logic and part of the code of the whole application is heavily taken from
`django CMS's <https://github.com/divio/django-cms>`_ own ``develop.py`` so all the contributors
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

.. |Status| image:: https://img.shields.io/travis/nephila/django-app-helper.svg?style=flat-square
    :target: https://travis-ci.org/nephila/django-app-helper
    :alt: Latest Travis CI build status

.. |TestCoverage| image:: https://img.shields.io/coveralls/nephila/django-app-helper/master.svg?style=flat-square
    :target: https://coveralls.io/r/nephila/django-app-helper?branch=master
    :alt: Test coverage

.. |License| image:: https://img.shields.io/github/license/nephila/django-app-helper.svg?style=flat-square
   :target: https://pypi.python.org/pypi/django-app-helper/
    :alt: License

.. |CodeClimate| image:: https://codeclimate.com/github/nephila/django-app-helper/badges/gpa.svg?style=flat-square
   :target: https://codeclimate.com/github/nephila/django-app-helper
   :alt: Code Climate
