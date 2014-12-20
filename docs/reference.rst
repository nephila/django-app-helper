###########################
django CMS Helper reference
###########################

========
Commands
========

Commands take the general form::

    djangocms-helper <application> <command> [options ...]

where **<application>** is the Django application name and **<command>** is one
of the available commands. Options vary for each command.

test
====

::

    djangocms-helper <application> test [--failfast] [--migrate] [<test-label>...] [--xvfb] [--runner=<test.runner.class>] [--extra-settings=</path/to/settings.py>] [--cms] [--nose-runner] [--simple-runner] [--runner-options=<option1>,<option2>]

Example: ``djangocms-helper some_application test --cms``

Runs the application's test suite in django CMS Helper's virtual environment.

Arguments
---------

* ``<test-label>``: a space-separated list of tests to run;

Options
-------

* ``--runner``: custom test runner to use in dotted path notation;
* ``--runner-options=<option1>,<option2>``: comma separated list of command
  line options for the test runner: e.g. ``--runner-options=--with-coverage,--cover-package=my_package``
* ``--failfast``: whether to stop at first test failure;
* ``--migrate``: whether to apply south migrations when running tests;
* ``--xvfb``: whether to configure ``xvfb`` (for frontend tests);
* ``--nose-runner``: use django nose test suite
* ``--simple-runner`` use Django DjangoTestSuiteRunner

Test structure
--------------

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

Currently supported test runners are:

* Django's DiscoverRunner (default)
* Django's DjangoTestSuiteRunner (option ``--simple-runner``)
* Nose's NoseTestSuiteRunner (option ``--nose-runner``)

You can also specify your own custom runner with the ``--runner`` option.


shell
=====

::

    djangocms-helper <application> shell [--extra-settings=</path/to/settings.py>] [--cms]

Example: ``djangocms-helper some_application shell --cms``

Starts a django shell for the test project.

check
=====

::

    djangocms-helper <application> check [--extra-settings=</path/to/settings.py>] [--cms]

Runs the Django ``check`` command.

Example: ``djangocms-helper some_application check --cms``

cms_check
=========

::

    djangocms-helper <application> cms_check [--extra-settings=</path/to/settings.py>] [--migrate]

Runs the django CMS ``cms check`` command.

Example: ``djangocms-helper some_application cms_check``

compilemessages and update messages
===================================

::

    djangocms-helper <application> compilemessages [--extra-settings=</path/to/settings.py>] [--cms]
    djangocms-helper <application> makemessages [--extra-settings=</path/to/settings.py>] [--cms]

Examples::

    djangocms-helper some_application compilemessages --cms
    djangocms-helper some_application makemessages --cms

These two commands compiles and update the locale messages.

makemigrations
==============

::

    djangocms-helper <application> makemigrations [--extra-settings=</path/to/settings.py>] [--cms] [--merge] [<extra-applications>...]

Updates the application migrations (south migrations or Django migrations
according to the current installed Django version). For South, it automatically
handles `initial` and `auto` options.

Options
-------

* ``--merge``: Enable fixing of migration conflicts (for Django 1.7+ only)

Arguments
---------

* ``<extra-applications>``: Spaces separated list of applications to migrate

squashmigrations
================

::

    djangocms-helper <application> squashmigrations <migration-name>


Runs the ``squashmigrations`` command. It operates on the current application.

Arguments
---------

* ``<migration-name>``: Squash migrations until this migration

pyflakes
========

::

    djangocms-helper <application> pyflakes [--extra-settings=</path/to/settings.py>] [--cms]

Performs static analysis using pyflakes, with the same configuration as django CMS.

authors
=======

::

    djangocms-helper <application> authors [--extra-settings=</path/to/settings.py>] [--cms]

Generates an authors list from the git log, in a form suitable for the **AUTHORS** file.

server
======

::

    djangocms-helper <application> server [--port=<port>] [--bind=<bind>] [--extra-settings=</path/to/settings.py>] [--cms]

Starts a runserver instance.
