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
    from .main import main
    if len(argv) == 1:
        argv.append('test')
    if app not in argv:
        argv.insert(1, app)
    # This is a hackish to get the caller file which is the file
    # which contains the HELPER_SETTINGS
    helper = os.path.abspath(inspect.getframeinfo(inspect.stack()[1][0]).filename)
    if os.path.basename(helper) != HELPER_FILE and '--extra-settings=%s' % helper not in argv:
        argv.append('--extra-settings=%s' % helper)
    main()


def cms(app, argv=sys.argv):
    """
    Function to invoke to run commands in a django CMS environment

    :param app: application
    """
    try:
        import cms
    except ImportError:
        print(u"runner.cms is available only if django CMS is installed")
    from .main import main
    if len(argv) == 1:
        argv.append('test')
    if app not in argv:
        argv.insert(1, app)
    if '--cms' not in argv:
        argv.insert(2, '--cms')
    # This is a hackish to get the caller file which is the file
    # which contains the HELPER_SETTINGS
    helper = os.path.abspath(inspect.getframeinfo(inspect.stack()[1][0]).filename)
    if os.path.basename(helper) != HELPER_FILE and '--extra-settings=%s' % helper not in argv:
        argv.append('--extra-settings=%s' % helper)
    main()
