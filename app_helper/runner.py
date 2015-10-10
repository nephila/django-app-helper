# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import inspect
import os.path
import sys


def run(app, argv=sys.argv, extra_args=None):
    """
    Run commands in a plain django environment

    :param app: application
    :param argv: arguments (default to sys.argv)
    :param extra_args: list of extra arguments
    """
    if app not in argv[:2]:
        # app is automatically added if not present
        argv.insert(1, app)
    if len(argv) < 3 and 'test' not in argv[:2]:
        # test argument is given if not argument is passed
        argv.insert(2, 'test')
    if extra_args:
        argv.extend(extra_args)
    return runner(argv)


def cms(app, argv=sys.argv, extra_args=None):
    """
    Run commands in a django cMS environment

    :param app: application
    :param argv: arguments (default to sys.argv)
    :param extra_args: list of extra arguments
    """
    try:
        import cms  # NOQA  # nopyflakes
    except ImportError:
        print('runner.cms is available only if django CMS is installed')
        raise
    if app not in argv[:2]:
        # app is automatically added if not present
        argv.insert(1, app)
    if len(argv) < 3 and 'test' not in argv[:2]:
        # test argument is given if not argument is passed
        argv.insert(2, 'test')
    if '--cms' not in argv:
        # this is the cms runner, just add the cms argument
        argv.append('--cms')
    if extra_args:
        argv.extend(extra_args)
    return runner(argv)


def setup(app, helper_module, extra_args=None, use_cms=False):
    """
    Setup the Django / django CMS environment and return the environment settings.

    :param app: application
    :param helper_module: helper module
    :param extra_args: list of extra arguments
    :param use_cms: setup a django CMS environemtn
    :return: Django settings module
    """
    helper = helper_module.__file__
    argv = [os.path.basename(helper), app, 'setup', '--extra-settings={0}'.format(helper)]
    if use_cms:
        argv.append('--cms')
    if extra_args:
        argv.extend(extra_args)
    return runner(argv)


def runner(argv):
    from . import HELPER_FILE
    from .main import main

    # This is a hackish way to get the caller file which is the file
    # which contains the HELPER_SETTINGS
    helper = os.path.abspath(inspect.getframeinfo(inspect.stack()[2][0]).filename)
    # check if extra settings has been passed
    # if not, user the helper file
    extra_settings = any(map(lambda x: x.startswith('--extra-settings='), argv))
    if os.path.basename(helper) != HELPER_FILE and not extra_settings:
        argv.append('--extra-settings=%s' % helper)
    return main(argv)
