# -*- coding: utf-8 -*-
from __future__ import print_function, with_statement
from copy import copy
import os.path
import shutil
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from ..main import (core, makemessages, makemigrations, compilemessages, shell,
                    generate_authors, static_analisys, test)
from ..utils import work_in, captured_output

DEFAULT_ARGS = {
    'shell': False,
    'test': False,
    'compilemessages': False,
    'makemessages': False,
    'makemigrations': False,
    'pyflakes': False,
    'authors': False,
}


class CommandTests(unittest.TestCase):
    application = None
    basedir = None
    pofile = None
    mofile = None

    @classmethod
    def setUpClass(cls):
        args = copy(DEFAULT_ARGS)
        args['authors'] = True
        cls.basedir = os.path.abspath(os.path.join('djangocms_helper', 'test_utils'))
        cls.application = 'example'
        with work_in(cls.basedir):
            with captured_output() as (out, err):
                core(args, cls.application)
                cls.poexample = os.path.abspath(os.path.join(cls.application, 'data', 'django.po'))
                cls.pofile = os.path.abspath(os.path.join(cls.application, 'locale', 'en', 'LC_MESSAGES', 'django.po'))
                cls.mofile = os.path.abspath(os.path.join(cls.application, 'locale', 'en', 'LC_MESSAGES', 'django.mo'))
                cls.migration_dir = os.path.abspath(os.path.join(cls.application, 'migrations'))
                cls.migration_file = os.path.abspath(os.path.join(cls.application, 'migrations', '0001_initial.py'))

    def setUp(self):
        try:
            os.unlink(self.pofile)
        except OSError:
            pass
        try:
            os.unlink(self.mofile)
        except OSError:
            pass
        try:
            shutil.rmtree(self.migration_dir)
        except OSError:
            pass

    def test_makemigrations(self):
        with work_in(self.basedir):
            with captured_output() as (out, err):
                makemigrations(self.application)
                self.assertTrue(os.path.exists(self.migration_file))
        self.assertTrue('Created 0001_initial.py' in err.getvalue())

    def test_makemessages(self):
        with work_in(self.basedir):
            with captured_output() as (out, err):
                makemessages(self.application)
                self.assertTrue(os.path.exists(self.pofile))

    def test_compilemessages(self):
        with work_in(self.basedir):
            with captured_output() as (out, err):
                shutil.copy(self.poexample, self.pofile)
                compilemessages(self.application)
                self.assertTrue(os.path.exists(self.mofile))

    def test_pyflakes(self):
        with work_in(self.basedir):
            with captured_output() as (out, err):
                static_analisys(self.application)

    def test_testrun(self):
        with work_in(self.basedir):
            with captured_output() as (out, err):
                test((self.application,), self.application, False, 'runners.CapturedOutputRunner')
        self.assertTrue('Ran 1 test in 0.000s' in err.getvalue())

    def test_authors(self):
        with work_in(self.basedir):
            with captured_output() as (out, err):
                generate_authors()
        self.assertTrue('Generating AUTHORS' in out.getvalue())
        self.assertTrue('* Iacopo Spalletti' in out.getvalue())
        self.assertTrue('Authors (2):' in out.getvalue())