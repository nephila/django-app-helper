##############
pytest support
##############

While its :py:class:`BaseTestCaseMixin` is built on Django ``TestCase``,
``django-app-helper`` can be used with pytest-based tests by using the provided
compatible runner as documented on `pytest-django`_ documentation.

To enable pytest compatible runner:

* Add to project ``helper.py`` file:

    .. code-block:: python

        HELPER_SETTINGS = {
            ...
            "TEST_RUNNER": "app_helper.pytest_runner.PytestTestRunner",
            ...
        }

* Run tests as usual::

    $ python helper.py <app-name> test

You can also mix pytest tests and Django ``TestCase`` ones, the runner will take care
of discovering and running both.

pytest options
==============

The runner support translates the following Django test runner options to pytest ones:

* ``verbosity == 0``: ``--quiet``
* ``verbosity == 2``: ``--verbose``
* ``verbosity == 3``: ``-vv``
* ``failfast``: ``--exitfirst``
* ``keepdb``: ``--reuse-db``

All the other pytest and pytest plugins are supported via ``PYTEST_ARGS`` enviroment variable::

    PYTEST_ARGS='-s -k my_test' python app_helper.py

.. _pytest-django: https://pytest-django.readthedocs.io/en/latest/faq.html#how-can-i-use-manage-py-test-with-pytest-django
