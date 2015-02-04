# -*- coding: utf-8 -*-
import inspect
import os.path
import sys

from . import HELPER_FILE


def run(app, argv=sys.argv):
    """
    Function to invoke to run commands in a plain django environment

    :param app: application
    """
    if len(argv) == 1:
        # test argument is given if not argument is passed
        argv.append('test')
    if app not in argv:
        # app is automatically added if not present
        argv.insert(1, app)
    runner(argv)


def cms(app, argv=sys.argv):
    """
    Function to invoke to run commands in a django CMS environment

    :param app: application
    """
    try:
        import cms  # NOQA
    except ImportError:
        print(u"runner.cms is available only if django CMS is installed")
    if len(argv) == 1:
        # test argument is given if not argument is passed
        argv.append('test')
    if app not in argv:
        # app is automatically added if not present
        argv.insert(1, app)
    if '--cms' not in argv:
        # this is the cms runner, just add the cms argument
        argv.insert(2, '--cms')
    runner(argv)


def runner(argv):
    from .main import main

    # This is a hackish way to get the caller file which is the file
    # which contains the HELPER_SETTINGS
    helper = os.path.abspath(inspect.getframeinfo(inspect.stack()[2][0]).filename)
    # check if extra settings has been passed
    # if not, user the helper file
    extra_settings = any(map(lambda x: x.startswith('--extra-settings='), argv))
    if os.path.basename(helper) != HELPER_FILE and not extra_settings:
        argv.append('--extra-settings=%s' % helper)
    main(argv)
