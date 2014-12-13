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

Available commands
==================

test
####

Test command allows to run the application test suite using test environemnt similar to
the django CMS testsuite.

Test structure
^^^^^^^^^^^^^^
Currently two different tests layouts are supported:

* tests outside the application module::

    setup.py
    tests
        __init__.py
        test_module1.py
        ....

* tests inside the application::

    setup.py
    application
        tests
            __init__.py
            test_module1.py
            ...

Depending on the used test runner you may need to setup your tests accordingly.

Currently supported test runners are:

* Django's DiscoverRunner (default)
* Django's DjangoTestSuiteRunner (option ``--simple-runner``)
* Nose's NoseTestSuiteRunner (option ``--nose-runner``)

You can also write your own runner an use it with ``--runner`` option.

Arguments
^^^^^^^^^

* ``<test-label>``: a space-separated list of tests to run;

Options
^^^^^^^

* ``--runner``: custom test runner to use in dotted path notation;
* ``--runner-options=<option1>,<option2>``: comma separated list of command
  line options for the test runner: e.g. ``--runner-options=--with-coverage,--cover-package=my_package``
* ``--failfast``: whether to stop at first test failure;
* ``--migrate``: whether to apply south migrations when running tests;
* ``--xvfb``: whether to configure ``xvfb`` (for frontend tests);
* ``--nose-runner``: use django nose test suite
* ``--simple-runner`` use Django DjangoTestSuiteRunner


shell
#####

Starts a django shell for the test project.

check
#####

Runs the Django ``check`` command

cms_check
#########

Runs the django CMS ``cms check`` command

compilemessages
###############

Compiles the locale messages.

makemessages
############

Updates the locale messages for the current application.

makemigrations
##############

Updates the application migrations (south migrations or Django migrations
according to the current installed Django version). For South, it automatically
handles **initial** / **auto** options.

Options
^^^^^^^

* ``--merge``: Enable fixing of migration conflicts (for Django 1.7+ only)

Arguments
^^^^^^^^^

* ``<extra-applications>``: Spaces separated list of applications to migrate

squashmigrations
################

Runs the ``squasmigrations`` command. It operates on the current application.

Arguments
^^^^^^^^^

* ``<migration-name>``: Squash migrations until this migration

pyflakes
########

Performs static analysis using pyflakes with the same configuration as django CMS.

authors
#######

Generates the authors list from the git log suitable for the **AUTHORS** file.


Customizing settings
^^^^^^^^^^^^^^^^^^^^

For non trivial applications, you'd probably want to customize the base django
settings provided by ``djangocms-helper``.

This can be achieved by either putting a ``cms_helper.py`` file in the application
main directory or by passing the path to the file using ``--extra-settings``
option (use full path complete with `.py` extension).

The file must contain a ``HELPER_SETTINGS`` dictionary containing the desired
settings::

    HELPER_SETTINGS = {
        'TIME_ZONE': 'Europe/Rome',
        'INSTALLED_APPS': [
            'another_application',
        ]
    }

All the parameter in settings will override the default ones, except
``INSTALLED_APPS`` and ``TEMPLATE_CONTEXT_PROCESSORS`` that will be appended to
the existing ones.

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

*******
Authors
*******

`djangocms-helper` was written by `Iacopo Spalletti <i.spalletti@nephila.it>`_.
