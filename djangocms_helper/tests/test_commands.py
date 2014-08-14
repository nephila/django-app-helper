# -*- coding: utf-8 -*-
from __future__ import print_function, with_statement
from copy import copy
import os.path
import shutil
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from cms.test_utils.tmpdir import temp_dir

from ..main import core, _make_settings
from ..utils import work_in, captured_output

DEFAULT_ARGS = {
    'shell': False,
    'test': False,
    'compilemessages': False,
    'makemessages': False,
    'makemigrations': False,
    'pyflakes': False,
    'authors': False,
    'server': False,
    '--xvfb': '',
    '--nose-runner': False,
    '--simple-runner': False,
    '--cms': True,
    '--failfast': False,
    '<test-label>': ''
}


class CommandTests(unittest.TestCase):
    application = None
    basedir = None
    pofile = None
    mofile = None

    @classmethod
    def setUpClass(cls):
        cls.basedir = os.path.abspath(os.path.join('djangocms_helper', 'test_utils'))
        cls.application = 'example'
        with work_in(cls.basedir):
            with captured_output() as (out, err):
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

    def tearDown(self):
        self.setUp()

    def test_extra_settings(self):
        from django.conf import settings

        with work_in(self.basedir):
            with captured_output() as (out, err):
                args = copy(DEFAULT_ARGS)
                with temp_dir() as STATIC_ROOT:
                    with temp_dir() as MEDIA_ROOT:
                        local_settings = _make_settings(args, self.application,
                                                        settings,
                                                        STATIC_ROOT, MEDIA_ROOT)
                        # Testing that cms_helper.py in custom project is loaded
                        self.assertEqual(local_settings.TIME_ZONE, 'Europe/Rome')

                        args['--extra-settings'] = 'cms_helper_extra.py'
                        local_settings = _make_settings(args, self.application,
                                                        settings,
                                                        STATIC_ROOT, MEDIA_ROOT)
                        # Testing that cms_helper.py in the command option is loaded
                        self.assertEqual(local_settings.TIME_ZONE, 'Europe/Paris')
                        # Existing application is kept
                        self.assertTrue('mptt' in local_settings.INSTALLED_APPS)
                        # New one is added
                        self.assertTrue('djangocms_admin_style' in local_settings.INSTALLED_APPS)
                        # Existing application is kept
                        self.assertTrue('django.core.context_processors.request' in local_settings.TEMPLATE_CONTEXT_PROCESSORS)
                        # New one is added
                        self.assertTrue('django.core.context_processors.debug' in local_settings.TEMPLATE_CONTEXT_PROCESSORS)

    def test_makemigrations(self):
        with work_in(self.basedir):
            with captured_output() as (out, err):
                args = copy(DEFAULT_ARGS)
                args['makemigrations'] = True
                core(args, self.application)
                self.assertTrue(os.path.exists(self.migration_file))
        self.assertTrue('Created 0001_initial.py' in err.getvalue())

    def test_makemessages(self):
        with work_in(self.basedir):
            with captured_output() as (out, err):
                args = copy(DEFAULT_ARGS)
                args['makemessages'] = True
                core(args, self.application)
                self.assertTrue(os.path.exists(self.pofile))

    def test_compilemessages(self):
        with work_in(self.basedir):
            with captured_output() as (out, err):
                shutil.copy(self.poexample, self.pofile)
                args = copy(DEFAULT_ARGS)
                args['compilemessages'] = True
                core(args, self.application)
                self.assertTrue(os.path.exists(self.mofile))

    def test_pyflakes(self):
        with work_in(self.basedir):
            with captured_output() as (out, err):
                args = copy(DEFAULT_ARGS)
                args['pyflakes'] = True
                core(args, self.application)

    def test_testrun(self):
        with work_in(self.basedir):
            with captured_output() as (out, err):
                with self.assertRaises(SystemExit) as exit:
                    args = copy(DEFAULT_ARGS)
                    args['test'] = True
                    args['--runner'] = 'runners.CapturedOutputRunner'
                    core(args, self.application)
        self.assertTrue('Ran 1 test in 0.000s' in err.getvalue())
        self.assertEqual(exit.exception.code, 0)

    def test_testrun_nocms(self):
        with work_in(self.basedir):
            with captured_output() as (out, err):
                with self.assertRaises(SystemExit) as exit:
                    args = copy(DEFAULT_ARGS)
                    args['test'] = True
                    args['--cms'] = False
                    args['--runner'] = 'runners.CapturedOutputRunner'
                    core(args, self.application)
        self.assertTrue('Ran 1 test in 0.000s' in err.getvalue())
        self.assertEqual(exit.exception.code, 0)

    def test_authors(self):
        with work_in(self.basedir):
            with captured_output() as (out, err):
                args = copy(DEFAULT_ARGS)
                args['authors'] = True
                core(args, self.application)
        self.assertTrue('Generating AUTHORS' in out.getvalue())
        self.assertTrue('* Iacopo Spalletti' in out.getvalue())
        self.assertTrue('Authors (2):' in out.getvalue())

    def test_urls(self):
        from django.core.urlresolvers import reverse
        with work_in(self.basedir):
            with captured_output() as (out, err):
                shutil.copy(self.poexample, self.pofile)
                args = copy(DEFAULT_ARGS)
                args['makemessages'] = True
                core(args, self.application)
                self.assertTrue(reverse('pages-root'))

    def test_urls_nocms(self):
        from django.core.urlresolvers import reverse, NoReverseMatch
        with work_in(self.basedir):
            with captured_output() as (out, err):
                shutil.copy(self.poexample, self.pofile)
                args = copy(DEFAULT_ARGS)
                args['makemessages'] = True
                args['--cms'] = False
                core(args, self.application)
                with self.assertRaises(NoReverseMatch):
                    reverse('pages-root')
