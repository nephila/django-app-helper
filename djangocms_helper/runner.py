# -*- coding: utf-8 -*-
import sys


def run(app):
    from .main import main
    if len(sys.argv) == 1:
        sys.argv.append('test')
    if app not in sys.argv:
        sys.argv.insert(1, app)
    main()


def cms(app):
    from .main import main
    if len(sys.argv) == 1:
        sys.argv.append('test')
    if app not in sys.argv:
        sys.argv.insert(1, app)
    if '--cms' not in sys.argv:
        sys.argv.insert(2, '--cms')
    main()
