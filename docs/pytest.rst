##############
pytest support
##############

While django-app-helper was born with Django ``TestCase`` in mind, it can be used with ``pytest`` with some configuration
together with ``pytest-django``.

************************
django-app-helper runner
************************

You can run pytest tests by using a custom runner (based on `pytest-django`_ documentation); to enable it,
add the following to project ``helper.py`` file:

  .. code-block:: python

      HELPER_SETTINGS = {
          ...
          "TEST_RUNNER": "app_helper.pytest_runner.PytestTestRunner",
          ...
      }

Using this approach you can mix pytest tests and Django ``TestCase`` ones, the runner will take care
of discovering and running both.

Running tests
==============

Invoke ``app_helper`` as usual::

    $ python helper.py <app-name> test

pytest options
==============

The runner support translates the following Django test runner options to pytest ones:

* ``verbosity == 0``: ``--quiet``
* ``verbosity == 2``: ``--verbose``
* ``verbosity == 3``: ``-vv``
* ``failfast``: ``--exitfirst``
* ``keepdb``: ``--reuse-db``

All the other pytest and pytest plugins are supported either via ``PYTEST_ARGS`` enviroment variable or
``--runner-options`` cmdline argument.

Environment variable example::

    PYTEST_ARGS='-s -k my_test' python helper.py test

argument variable example::

    python helper.py test --runner-options="-k my_test"

In case arguments are passed via both channels they are merged together, with runner-options arguments having priority
over environment variables in case of overlapping options.

.. _pytest-django: https://pytest-django.readthedocs.io/en/latest/faq.html#how-can-i-use-manage-py-test-with-pytest-django

***************
standard pytest
***************

Running tests
==============

Invoke ``pytest`` as usual::

    $ python -mpytest <args>

or::

    $ pytest <args>

In this case you don't need any special syntax to pass commands as the
django-app-helper pytest runner is not executed and pytest is full in control.

.. warning: the ``pytest`` invocation will only works if you add the current directory in the ``PYTHONPATH``, thus the
            ``python -mpytest`` version is preferred.

Using BaseTestCaseMixin
=======================

While its :py:class:`~app_helper.base_test.BaseTestCaseMixin` is built on Django ``TestCase``, it can be used in pytest classes:

Fixtures, markers and decorators can be used as usual on test methods as in classic pytest classes.

.. code-block:: python

    class TestTags(BaseTestCaseMixin):
        ...
        def test_foo(self):
            ...
