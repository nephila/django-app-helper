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

.. _pytest-django: https://pytest-django.readthedocs.io/en/latest/faq.html#how-can-i-use-manage-py-test-with-pytest-django
