# -*- coding: utf-8 -*-
import sys


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
    main()
