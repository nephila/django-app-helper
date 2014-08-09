# -*- coding: utf-8 -*-
import contextlib
import os
import sys
from django.utils.six import StringIO


def load_from_file(module_path):
    """
    Load a python module from its absolute filesystem path

    Borrowed from django-cms
    """
    from imp import load_module, PY_SOURCE

    imported = None
    if module_path:
        with open(module_path, 'r') as openfile:
            imported = load_module("mod", openfile, module_path,
                                   ('imported', 'r', PY_SOURCE))
    return imported


@contextlib.contextmanager
def work_in(dirname=None):
    """
    Context manager version of os.chdir. When exited, returns to the working
    directory prior to entering.

    Grabbed from cookiecutter, thanks audreyr!
    """
    curdir = os.getcwd()
    try:
        if dirname is not None:
            if dirname not in sys.path:
                sys.path.insert(0, dirname)
            os.chdir(dirname)
        yield
    finally:
        os.chdir(curdir)


@contextlib.contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err