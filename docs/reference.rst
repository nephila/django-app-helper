###########################
django CMS Helper reference
###########################

========
Commands
========

Commands take the general form::

    djangocms-helper <application> <command> [options ...]

where **<application>** is the Django application name and **<command>** is a Django supported
command, *or* one of the djangocms-helper commands detailed below. Options vary for each command.


Common options
==============

* ``--extra-settings=path``: loads the extra settings from the provided file instead of the
  default ``cms_helper.py``
* ``cms``: loads django CMS specific options (see :ref:`cms-option` for details)


Django commands
===============

django CMS Helper supports any Django command available according to the project setup; the
general syntax is::

    djangocms-helper <application> <command> [options] [--extra-settings=</path/to/settings.py>] [--cms]

Example: ``djangocms-helper some_application shell --cms``

Arguments
---------

* ``<command>`` is any available Django command
* ``[options]`` is any option/argument accepted by the above command



test
====

::

    djangocms-helper <application> test [--failfast] [--migrate] [<test-label>...] [--xvfb] [--runner=<test.runner.class>] [--extra-settings=</path/to/settings.py>] [--cms] [--nose-runner] [--simple-runner] [--runner-options=<option1>,<option2>]

Example: ``djangocms-helper some_application test --cms``

Runs the application's test suite in django CMS Helper's virtual environment.

Arguments
---------

* ``<test-label>``: a space-separated list of tests to run; test labels depends on the runner
  test suite building protocol, please, refer to the runner documentation to know the
  test label format;

Options
-------

* ``--runner``: custom test runner to use in dotted path notation;
* ``--runner-options=<option1>,<option2>``: comma separated list of command
  line options for the test runner: e.g. ``--runner-options=--with-coverage,--cover-package=my_package``
* ``--failfast``: whether to stop at first test failure;
* ``--migrate``: use migrations (default);
* ``--persistent``: use persistent storage for media and static; if given without arguments the
                    storage is created in ``data`` directory in the root of the application; if
                    argument is provided, it's used as parent path (either absolute or relative)
                    for ``media`` and ``static``;
* ``--no-migrate``: skip migrations;
* ``--boilerplate``: adds ``aldryn-boilerplates`` configuration to settings;
* ``--xvfb``: whether to configure ``xvfb`` (for frontend tests);
* ``--nose-runner``: use django nose test suite
* ``--simple-runner`` use Django DjangoTestSuiteRunner
* ``--native`` use the native Django command: the use of this option is **incompatible** with
  the options above.

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

Depending on the used test runner you may need to setup your tests accordingly.

Currently supported test runners are:

* Django's DiscoverRunner (default on Django 1.6+)
* Nose's NoseTestSuiteRunner (option ``--nose-runner``)

You can also specify your own custom runner with the ``--runner`` option.


cms_check
=========

::

    djangocms-helper <application> cms_check [--extra-settings=</path/to/settings.py>] [--migrate]

Runs the django CMS ``cms check`` command.

Example: ``djangocms-helper some_application cms_check``

update and compile locales
==========================

::

    djangocms-helper <application> makemessages [--extra-settings=</path/to/settings.py>] [--cms] [--locale=locale]
    djangocms-helper <application> compilemessages [--extra-settings=</path/to/settings.py>] [--cms]

Examples::

    djangocms-helper some_application makemessages --cms
    djangocms-helper some_application compilemessages --cms

These two commands compiles and update the locale messages.

Options
-------

* ``--locale=locale``: ``makemessages`` allows a single option to choose the locale to update.
                       If not provided **en** is used.

makemigrations
==============

::

    djangocms-helper <application> makemigrations [--extra-settings=</path/to/settings.py>] [--cms] [--merge] [--dry-run] [--empty] [<extra-applications>...]

Updates the application migrations (south migrations or Django migrations
according to the current installed Django version). For South, it automatically
handles `initial` and `auto` options.

Options
-------

* ``--merge``: Enable fixing of migration conflicts (for Django 1.7+ only)
* ``--empty``: It generates an empty migration for customisations
* ``--dry-run``: Does not create migrations file (for Django 1.7+ only)

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
