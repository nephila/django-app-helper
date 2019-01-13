#################
Integrated runner
#################

Django App Helper provide a runner to invoke the commands without requiring the
``django-app-helper`` file; this can be useful to invoke tests with coverage or to
have a simpler syntax to remember.

Typically you'd setup the runner function in the :ref:`extra settings file <extra-settings>`::


    HELPER_SETTINGS={
        'INSTALLED_APPS': [
            'any_django_app',
        ],
        'ANY_SETTING: False,
        ...
    }


    def run():
        from app_helper import runner
        runner.cms('my_app')

    if __name__ == "__main__":
        run()


with the above code in place you can run any Django App Helper command as::

    python helper.py <command>

and adding the ``test_suite`` argument to ``setup.py``::

    setup(
        ...
        test_suite='app_helper.run',
        ...
    )

you can invoke the tests with::

    python setup.py test


******************
Django environment
******************

If you don't need django CMS, you can use a runner function with no CMS attached::


    def run():
        from app_helper import runner
        runner.run('my_app')

    if __name__ == "__main__":
        run()


.. warning:: The runner **must** be invoked from the **settings** file.
             The runner takes care of setting up the file in which is
             invoked as the ``extra_settings`` file.

.. _naked_runner:

******************
Naked setup
******************

Sometimes you just want to properly setup a Django environment without running any commands
(e.g: when building Sphinx docs using autodoc). Naked setup allows to do so::


    def setup():
        import sys
        from app_helper import runner
        runner.setup('my_app', sys.modules[__name__], use_cms=True)

    if __name__ == "cms_helper":
        setup()

the last lines allows to auto-load naked setup when runner file is imported. This is
useful when running tests in a PyCharm environment.
In case you customized the runner filename, replace ``"cms_helper"`` with the
custom name.

.. warning:: The runner **must** be invoked from the **settings** file.
             The runner takes care of setting up the file in which is
             invoked as the ``extra_settings`` file.
