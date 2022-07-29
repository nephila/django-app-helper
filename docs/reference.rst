###########################
Django App Helper reference
###########################

*********************************
Commands
*********************************

Commands take the general form::

    django-app-helper <application> <command> [options ...]

where **<application>** is the Django application name and **<command>** is a Django supported
command, *or* one of the django-app-helper commands detailed below. Options vary for each command.

.. note:: while all examples here use the ``django-app-helper`` CLI, a more idiomatic way to run commands is by using
          :ref:`runner`.


Common options
==============

* ``--extra-settings=path``: loads the extra settings from the provided file instead of the
  default ``helper.py``
* ``cms``: loads django CMS specific options (see :ref:`cms-option` for details)


Django commands
===============

Django App Helper supports any Django command available according to the project setup; the
general syntax is::

    django-app-helper <application> <command> [options] [--extra-settings=</path/to/settings.py>] [--cms]

Example: ``django-app-helper some_application shell --cms``

Arguments
---------

* ``<command>`` is any available Django command
* ``[options]`` is any option/argument accepted by the above command



test
====

::

    django-app-helper <application> test [--failfast] [--migrate] [<test-label>...] [--xvfb] [--runner=<test.runner.class>] [--extra-settings=</path/to/settings.py>] [--cms] [--simple-runner] [--runner-options=<option1>,<option2>]

Example: ``django-app-helper some_application test --cms``

Runs the application's test suite in Django App Helper's virtual environment.

Arguments
---------

* ``<test-label>``: a space-separated list of tests to run; test labels depends on the runner
  test suite building protocol, please, refer to the runner documentation to know the
  test label format;

Options
-------

* ``--runner``: custom test runner to use in dotted path notation;
* ``--runner-options=<option1>,<option2>``: comma separated list of command
  line options for the test runner: e.g. ``--runner-options="--with-coverage,--cover-package=my_package"``
* ``--failfast``: whether to stop at first test failure;
* ``--migrate``: use migrations (default);
* ``--persistent``: use persistent storage for media and static; by default  storage is created
  in ``data`` directory in the root of the application; if a different
  directory is needed, use ``--persistent-path`` to provide the path;
* ``--persistent-path``: persistent storage path, instead of ``data``
* ``--no-migrate``: skip migrations;
* ``--xvfb``: whether to configure ``xvfb`` (for frontend tests);
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

The default runner is the Django one, but it's possible to specify your own custom runner with the ``--runner`` option.


cms_check
=========

::

    django-app-helper <application> cms_check [--extra-settings=</path/to/settings.py>] [--migrate]

Runs the django CMS ``cms check`` command.

Example: ``django-app-helper some_application cms_check``

update and compile locales
==========================

::

    django-app-helper <application> makemessages [--extra-settings=</path/to/settings.py>] [--cms] [--locale=locale]
    django-app-helper <application> compilemessages [--extra-settings=</path/to/settings.py>] [--cms]

Examples::

    django-app-helper some_application makemessages --cms
    django-app-helper some_application compilemessages --cms

These two commands compiles and update the locale messages.

Options
-------

* ``--locale=locale``: ``makemessages`` allows a single option to choose the locale to update.
  If not provided **en** is used.

makemigrations
==============

::

    django-app-helper <application> makemigrations [--extra-settings=</path/to/settings.py>] [--cms] [--merge] [--dry-run] [--empty] [<extra-applications>...]

Updates the application migrations (south migrations or Django migrations
according to the current installed Django version). For South, it automatically
handles ``initial`` and ``auto`` options.

Options
-------

* ``--merge``: Enable fixing of migration conflicts
* ``--empty``: It generates an empty migration for customisations
* ``--dry-run``: Does not create migrations file

Arguments
---------

* ``<extra-applications>``: Spaces separated list of applications to migrate

squashmigrations
================

::

    django-app-helper <application> squashmigrations <migration-name>


Runs the ``squashmigrations`` command. It operates on the current application.

Arguments
---------

* ``<migration-name>``: Squash migrations until this migration

authors
=======

::

    django-app-helper <application> authors [--extra-settings=</path/to/settings.py>] [--cms]

Generates an authors list from the git log, in a form suitable for the **AUTHORS** file.

server
======

::

    django-app-helper <application> server [--port=<port>] [--bind=<bind>] [--extra-settings=</path/to/settings.py>] [--cms] [--migrate] [--no-migrate] [--persistent | --persistent-path=<path>] [--verbose=<level>] [--use-daphne] [--use-channels]

Starts a runserver instance.

* ``--port=<port>``: port to bind the server on;
* ``--bind=<bind>``: address to bind the server on;
* ``--extra-settings=</path/to/settings.py>``: path to extra settings file;
* ``--cms``: enable django CMS settings;
* ``--migrate``: run migrations on server start (default);
* ``--no-migrate``: do not run migrations on server start;
* ``--persistent | --persistent-path=<path>``: persist generated media directory; optionally you can provide a fixed path;
* ``--verbose=<level>``: verbosity level;
* ``--use-daphne``: use daphne server;
* ``--use-channels]``: use channels server;
