# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import os
import os.path
import shutil
import sys
from copy import copy
from distutils.version import LooseVersion

import django
from django.utils.encoding import force_text

from djangocms_helper import runner
from djangocms_helper.default_settings import get_boilerplates_settings
from djangocms_helper.main import _make_settings, core
from djangocms_helper.utils import DJANGO_1_6, DJANGO_1_7, captured_output, temp_dir, work_in

try:
    import unittest2 as unittest
except ImportError:
    import unittest


DEFAULT_ARGS = {
    'shell': False,
    'test': False,
    'cms_check': False,
    'compilemessages': False,
    'makemessages': False,
    'makemigrations': False,
    'pyflakes': False,
    'authors': False,
    'server': False,
    '--xvfb': '',
    '--runner': None,
    '--runner-options': None,
    '--nose-runner': False,
    '--simple-runner': False,
    '--cms': True,
    '--failfast': False,
    '--merge': False,
    '--boilerplate': False,
    '--dry-run': False,
    '--empty': False,
    '--native': False,
    '--bind': '',
    '--port': '',
    '<test-label>': '',
    '<extra-applications>': '',
    'options': '',
    '<command>': '',
}


class CommandTests(unittest.TestCase):
    application = None
    basedir = None
    pofile = None
    mofile = None
    migration_dir = None

    @classmethod
    def setUpClass(cls):
        os.environ.setdefault('DATABASE_URL', 'sqlite://localhost/:memory:')
        cls.basedir = os.path.abspath(os.path.join('djangocms_helper', 'test_utils'))
        cls.application = 'example1'
        cls.application_2 = 'example2'
        with work_in(cls.basedir):
            with captured_output() as (out, err):
                if LooseVersion(django.get_version()) >= LooseVersion('1.7'):
                    cls.migration_example = os.path.abspath(os.path.join(cls.application, 'data', 'django_0001_initial.py'))
                    cls.migration_partial = os.path.abspath(os.path.join(cls.application, 'data', 'django_0001_partial.py'))
                else:
                    cls.migration_example = os.path.abspath(os.path.join(cls.application, 'data', 'south_0001_initial.py'))
                    cls.migration_partial = os.path.abspath(os.path.join(cls.application, 'data', 'south_0001_partial.py'))
                cls.poexample = os.path.abspath(os.path.join(cls.application, 'data', 'django.po'))
                cls.pofile = os.path.abspath(os.path.join(cls.application, 'locale', 'en', 'LC_MESSAGES', 'django.po'))
                cls.mofile = os.path.abspath(os.path.join(cls.application, 'locale', 'en', 'LC_MESSAGES', 'django.mo'))
                cls.migration_dir = os.path.abspath(os.path.join(cls.application, 'migrations'))
                cls.migration_dir_2 = os.path.abspath(os.path.join(cls.application_2, 'migrations'))
                cls.migration_file = os.path.abspath(os.path.join(cls.application, 'migrations', '0001_initial.py'))
                cls.migration_file_2 = os.path.abspath(os.path.join(cls.application_2, 'migrations', '0001_initial.py'))
        try:
            import cms
        except ImportError:
            DEFAULT_ARGS['--cms'] = False

    def setUp(self):
        try:
            os.unlink(self.pofile)
        except (OSError, TypeError):
            pass
        try:
            os.unlink(self.mofile)
        except (OSError, TypeError):
            pass
        try:
            if self.migration_dir:
                shutil.rmtree(self.migration_dir)
        except (OSError, TypeError):
            pass
        try:
            if self.migration_dir_2:
                shutil.rmtree(self.migration_dir_2)
        except (OSError, TypeError):
            pass
        try:
            del sys.modules['example1.migrations']
        except KeyError as e:
            pass
        try:
            del sys.modules['example2.migrations']
        except KeyError as e:
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

                        args['--boilerplate'] = True
                        args['--extra-settings'] = 'cms_helper_extra.py'
                        local_settings = _make_settings(args, self.application,
                                                        settings,
                                                        STATIC_ROOT, MEDIA_ROOT)
                        # Testing that cms_helper.py in the command option is loaded
                        self.assertEqual(local_settings.TIME_ZONE, 'Europe/Paris')
                        # Existing application is kept
                        self.assertTrue('djangocms_helper.test_data' in local_settings.INSTALLED_APPS)
                        # New one is added
                        self.assertTrue('djangocms_admin_style' in local_settings.INSTALLED_APPS)

                        boilerplate_settings = get_boilerplates_settings()

                        if DJANGO_1_7:
                            # Check the loaders
                            self.assertTrue('django.template.loaders.app_directories.Loader' in local_settings.TEMPLATE_LOADERS)
                            # Existing application is kept
                            self.assertTrue('django.core.context_processors.request' in local_settings.TEMPLATE_CONTEXT_PROCESSORS)
                            # New one is added
                            self.assertTrue('django.core.context_processors.debug' in local_settings.TEMPLATE_CONTEXT_PROCESSORS)
                            # Check for aldryn boilerplates
                            for name, value in boilerplate_settings.items():
                                if type(value) in (list, tuple):
                                    self.assertTrue(set(getattr(local_settings, name)).intersection(set(value)))
                                else:
                                    self.assertTrue(value in getattr(local_settings, name))
                        else:
                            # Check the loaders
                            self.assertTrue('django.template.loaders.app_directories.Loader' in local_settings.TEMPLATES[0]['OPTIONS']['loaders'])
                            # Existing application is kept
                            self.assertTrue('django.template.context_processors.request' in local_settings.TEMPLATES[0]['OPTIONS']['context_processors'])
                            # New one is added
                            self.assertTrue('django.template.context_processors.debug' in local_settings.TEMPLATES[0]['OPTIONS']['context_processors'])
                            # Check for aldryn boilerplates
                            for name, value in boilerplate_settings.items():
                                if not name.startswith('TEMPLATE'):
                                    if type(value) in (list, tuple):
                                        self.assertTrue(set(getattr(local_settings, name)).intersection(set(value)))
                                    else:
                                        self.assertTrue(value in getattr(local_settings, name))
                                elif name == 'TEMPLATE_CONTEXT_PROCESSORS':
                                    self.assertTrue(set(local_settings.TEMPLATES[0]['OPTIONS']['context_processors']).intersection(set(value)))
                                elif name == 'TEMPLATE_LOADERS':
                                    self.assertTrue(set(local_settings.TEMPLATES[0]['OPTIONS']['loaders']).intersection(set(value)))

    def test_makemigrations(self):
        with work_in(self.basedir):
            with captured_output() as (out, err):
                args = copy(DEFAULT_ARGS)
                args['makemigrations'] = True
                args['<extra-applications>'] = ['example2']
                core(args, self.application)
            self.assertTrue(os.path.exists(self.migration_file))
            self.assertTrue(os.path.exists(self.migration_file_2))
        if DJANGO_1_6:
            self.assertTrue('Created 0001_initial.py' in err.getvalue())
            self.assertTrue('migrate example1' in err.getvalue())
            self.assertTrue('migrate example2' in err.getvalue())
        else:
            self.assertTrue('Create model ExampleModel1' in out.getvalue())
            self.assertTrue('Create model ExampleModel2' in out.getvalue())

    def skip_test_makemigrations_update(self):
        os.makedirs(self.migration_dir)
        open(os.path.join(self.migration_dir, '__init__.py'), 'w')
        shutil.copy(self.migration_partial, self.migration_file)
        with work_in(self.basedir):
            with captured_output() as (out, err):
                args = copy(DEFAULT_ARGS)
                args['makemigrations'] = True
                core(args, self.application)
        if DJANGO_1_6:
            #self.assertTrue('+ Added field test_field on example1.ExampleModel1' in err.getvalue())
            self.assertTrue('You can now apply this migration' in err.getvalue())
        else:
            self.assertTrue('Migrations for \'example1\':' in out.getvalue())

    def test_makemigrations_empty(self):
        with work_in(self.basedir):
            with captured_output() as (out, err):
                os.makedirs(self.migration_dir)
                open(os.path.join(self.migration_dir, '__init__.py'), 'w')
                shutil.copy(self.migration_example, self.migration_file)
                args = copy(DEFAULT_ARGS)
                args['makemigrations'] = True
                args['--empty'] = True
                core(args, self.application)
        if DJANGO_1_6:
            self.assertTrue('You must now edit this migration' in err.getvalue())
        else:
            self.assertTrue('Migrations for \'example1\':' in out.getvalue())

    @unittest.skipIf(LooseVersion(django.get_version()) >= LooseVersion('1.7'),
                     reason='check only for Django < 1.7')
    def test_makemigrations_existing_folder(self):
        os.makedirs(self.migration_dir)
        os.makedirs(self.migration_dir_2)
        open(os.path.join(self.migration_dir, '__init__.py'), 'w')
        open(os.path.join(self.migration_dir_2, '__init__.py'), 'w')
        with work_in(self.basedir):
            with captured_output() as (out, err):
                args = copy(DEFAULT_ARGS)
                args['makemigrations'] = True
                args['<extra-applications>'] = ['example2']
                core(args, self.application)
            self.assertTrue(os.path.exists(self.migration_file))
            self.assertTrue(os.path.exists(self.migration_file_2))
        self.assertTrue('Created 0001_initial.py' in err.getvalue())
        self.assertTrue('migrate example1' in err.getvalue())
        self.assertTrue('migrate example2' in err.getvalue())

    def test_makemigrations_merge(self):
        from django.core.exceptions import DjangoRuntimeWarning
        with work_in(self.basedir):
            with captured_output() as (out, err):
                args = copy(DEFAULT_ARGS)
                args['makemigrations'] = True
                args['--merge'] = True
                if DJANGO_1_6:
                    with self.assertRaises(DjangoRuntimeWarning) as exit:
                        core(args, self.application)
                    self.assertEqual(force_text(exit.exception), 'Option not implemented for Django 1.6 and below')
                else:
                    core(args, self.application)
                    self.assertTrue('No conflicts detected to merge' in out.getvalue())

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

    def test_cms_check(self):
        try:
            import cms
        except ImportError:
            raise unittest.SkipTest('django CMS not available, skipping test')
        with work_in(self.basedir):
            with captured_output() as (out, err):
                shutil.copy(self.poexample, self.pofile)
                args = copy(DEFAULT_ARGS)
                args['cms_check'] = True
                args['--migrate'] = False
                core(args, self.application)
            self.assertTrue('Installation okay' in out.getvalue())
            self.assertFalse('[WARNING]' in out.getvalue())
            self.assertFalse('[ERROR]' in out.getvalue())

    @unittest.skipIf(LooseVersion(django.get_version()) < LooseVersion('1.7'),
                     reason='check command available in Django 1.7+ only')
    def test_any_command_check(self):
        with work_in(self.basedir):
            with captured_output() as (out, err):
                args = copy(DEFAULT_ARGS)
                args['<command>'] = 'check'
                args['options'] = ['helper', 'check', '--extra-settings=cms_helper_extra.py']
                core(args, self.application)
        if DJANGO_1_7:
            # Django 1.7 complains about the test runner ... go figure ...
            self.assertTrue('1 issue' in err.getvalue())
        else:
            self.assertTrue('no issues' in out.getvalue())

    def test_any_command_compilemessages(self):
        with work_in(os.path.join(self.basedir, self.application)):
            with captured_output() as (out, err):
                shutil.copy(self.poexample, self.pofile)
                args = copy(DEFAULT_ARGS)
                args['<command>'] = 'compilemessages'
                args['options'] = 'helper compilemessages --cms -len --verbosity=2'.split(' ')
                core(args, self.application)
                self.assertTrue(os.path.exists(self.mofile))

    @unittest.skipIf(LooseVersion(django.get_version()) < LooseVersion('1.7'),
                     reason='makemigrations command available for Django 1.7+ only')
    def test_any_command_migrations(self):
        with work_in(self.basedir):
            with captured_output() as (out, err):
                args = copy(DEFAULT_ARGS)
                args['<command>'] = 'makemigrations'
                args['options'] = 'helper makemigrations example2 --verbosity=2'.split(' ')
                core(args, self.application)
            self.assertFalse('Create model ExampleModel1' in out.getvalue())
            self.assertFalse(os.path.exists(self.migration_file))
            self.assertTrue('Create model ExampleModel2' in out.getvalue())
            self.assertTrue(os.path.exists(self.migration_file_2))

    def test_pyflakes(self):
        try:
            import cms
        except ImportError:
            raise unittest.SkipTest('django CMS not available, skipping test')
        with work_in(self.basedir):
            with captured_output() as (out, err):
                args = copy(DEFAULT_ARGS)
                args['pyflakes'] = True
                core(args, self.application)

    @unittest.skipIf(sys.version_info < (2, 7),
                     reason='Example test non discoverable in Python 2.6')
    def test_testrun(self):
        with work_in(self.basedir):
            with captured_output() as (out, err):
                with self.assertRaises(SystemExit) as exit:
                    args = copy(DEFAULT_ARGS)
                    args['test'] = True
                    args['--runner'] = 'runners.CapturedOutputRunner'
                    core(args, self.application)
        self.assertTrue('Ran 6 tests in' in err.getvalue())
        self.assertEqual(exit.exception.code, 0)

    @unittest.skipIf(sys.version_info < (2, 7),
                     reason='Example test non discoverable in Python 2.6')
    def test_runner(self):
        try:
            import cms
        except ImportError:
            raise unittest.SkipTest('django CMS not available, skipping test')
        with work_in(self.basedir):
            with captured_output() as (out, err):
                with self.assertRaises(SystemExit) as exit:
                    args = list()
                    args.append('djangocms_helper')
                    args.append('example1')
                    args.append('test')
                    args.append('--runner=runners.CapturedOutputRunner')
                    runner.cms('example1', args)
        self.assertTrue('Ran 6 tests in' in err.getvalue())
        self.assertEqual(exit.exception.code, 0)

    @unittest.skipIf(sys.version_info < (2, 7),
                     reason='Example test non discoverable in Python 2.6')
    def test_testrun_nocms(self):
        try:
            import cms
        except ImportError:
            raise unittest.SkipTest('django CMS not available, skipping test')
        with work_in(self.basedir):
            with captured_output() as (out, err):
                with self.assertRaises(SystemExit) as exit:
                    args = copy(DEFAULT_ARGS)
                    args['test'] = True
                    args['--cms'] = False
                    args['--runner'] = 'runners.CapturedOutputRunner'
                    core(args, self.application)
        self.assertTrue('Ran 6 tests in' in err.getvalue())
        self.assertEqual(exit.exception.code, 0)

    @unittest.skipIf(sys.version_info < (2, 7),
                     reason='Example test non discoverable in Python 2.6')
    def test_runner_nocms(self):
        with work_in(self.basedir):
            with captured_output() as (out, err):
                with self.assertRaises(SystemExit) as exit:
                    args = list()
                    args.append('djangocms_helper')
                    args.append('example1')
                    args.append('test')
                    args.append('--runner=runners.CapturedOutputRunner')
                    runner.run('example1', args)
        self.assertTrue('Ran 6 tests in' in err.getvalue())
        self.assertEqual(exit.exception.code, 0)

    @unittest.skipIf(sys.version_info < (2, 7),
                     reason='Example test non discoverable in Python 2.6')
    def test_testrun_native(self):
        try:
            import cms
        except ImportError:
            raise unittest.SkipTest('django CMS not available, skipping test')
        with work_in(self.basedir):
            with captured_output() as (out, err):
                args = copy(DEFAULT_ARGS)
                args['<command>'] = 'test'
                args['--cms'] = False
                args['--native'] = True
                args['--extra-settings'] = 'cms_helper_extra_runner.py'
                core(args, self.application)
        self.assertTrue('Ran 6 tests in' in err.getvalue())

    def test_authors(self):
        with work_in(self.basedir):
            with captured_output() as (out, err):
                args = copy(DEFAULT_ARGS)
                args['authors'] = True
                core(args, self.application)
        self.assertTrue('Generating AUTHORS' in out.getvalue())
        self.assertTrue('* Iacopo Spalletti' in out.getvalue())
        self.assertTrue('Authors (' in out.getvalue())

    def test_urls(self):
        try:
            import cms
        except ImportError:
            raise unittest.SkipTest('django CMS not available, skipping test')
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
