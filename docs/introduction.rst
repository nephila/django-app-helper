############################
How to use Django App Helper
############################

We'll assume that you have an application for django CMS that you're working on.

Once you have django CMS installed, it'll be available using ``django-app-helper`` command.

``cd`` into the root directory of your application (that is, the outer directory containing its
``setup.py``). You need to be here to run the ``django-app-helper`` command.


*********************************
Running Django App Helper command
*********************************

Try it::

    django-app-helper <myapp> test --cms  # change <myapp> to your application's actual name

It'll spawn its virtual project and run your tests in it. You should see some output along these
lines (there may well be some other output before it gets to this stage)::

    Creating test database for alias 'default'...
    F
    ======================================================================
    FAIL: test_bad_maths (djangocms_maths.tests.SmokeTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "./djangocms_maths/tests.py", line 6, in test_bad_maths
        self.assertEqual(1 + 1, 3)
    AssertionError: 2 != 3

    ----------------------------------------------------------------------
    Ran 1 test in 0.000s

    FAILED (failures=1)

All commands take a form similar to the one you've just run, sharing the basic command structure::

    django-app-helper <application> <command> [options ...]

where **<application>** is the Django application name and **<command>** is one
of the available commands. Options vary for each command.

************************************
But I haven't written any tests yet!
************************************

It helps if you actually have some tests of course - if you don't, simply create a ``tests.py``
file in your application (not in this directory, but in the package directory, alongside its
models and views and so on)::

    from django.test import TestCase

    class SmokeTest(TestCase):

        # a deliberately-failing test
        def test_bad_maths(self):
            self.assertEqual(1 + 1, 3)

*********************************
The --cms option
*********************************

You'll need the ``--cms`` option most of the time. It sets up the virtual project appropriately
for django CMS, providing the required configuration (see :ref:`cms-option` for details).

*********************************
Other commands
*********************************

Try a couple of the other commands; they're mostly self-explanatory::

    django-app-helper <myapp> shell --cms  # start a Django shell for the virtual project

    django-app-helper <myapp> check --cms  # runs the Django check command

    django-app-helper <myapp> cms_check  # runs the django CMS check command

Note that the last of these doesn't require the ``--cms`` option, because of course that is implied
anyway by ``cms_check``.



*********************************
Integrated runner
*********************************

In some contexts running commands by using the complete syntax can be clunky or unfeasible.

Django App Helper contains function that allows to run the commands with a much shorter syntax::

    python helper.py

to run tests

Or::

    python helper.py server

to invoke a server.

See :doc:`runner` for details.


*********************************
Sphinx integration
*********************************

When documenting a project using Sphinx autodoc, you mostly need a proper project setup, because
the imports in your application's modules will trigger Django setup code anyway.

Using the :ref:`naked_runner` it's easy to let helper setup an environment for you:

* setup the :ref:`naked_runner`
* add the following code to sphinx ``conf.py``::

    sys.path.insert(0, os.path.abspath('..'))
    import app_helper
    app_helper.setup()

