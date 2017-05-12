# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import os
import os.path
import shutil
import sys
from copy import copy
from distutils.version import LooseVersion
from tempfile import mkdtemp

import django
from django.utils.encoding import force_text

from djangocms_helper import runner
from djangocms_helper.default_settings import get_boilerplates_settings
from djangocms_helper.main import _make_settings, core
from djangocms_helper.utils import (
    DJANGO_1_6, DJANGO_1_7, DJANGO_1_8, DJANGO_1_9, captured_output, temp_dir, work_in,
)

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch


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
    '--locale': '',
    '--boilerplate': False,
    '--dry-run': False,
    '--empty': False,
    '--native': False,
    '--persistent': False,
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
            with captured_output():
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
            #with captured_output() as (out, err):
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
                        # New ones are added both on top and in random positions
                        self.assertEqual('djangocms_admin_style', local_settings.INSTALLED_APPS[0])
                        self.assertTrue('some_app' in local_settings.INSTALLED_APPS)

                        # Ditto for middlewares
                        if DJANGO_1_9:
                            self.assertEqual('top_middleware', local_settings.MIDDLEWARE_CLASSES[0])
                            self.assertTrue('some_middleware' in local_settings.MIDDLEWARE_CLASSES)
                            self.assertTrue('django.contrib.sessions.middleware.SessionMiddleware' in local_settings.MIDDLEWARE_CLASSES)
                        else:
                            self.assertTrue('django.contrib.sessions.middleware.SessionMiddleware' in local_settings.MIDDLEWARE)
                            self.assertEqual('top_middleware', local_settings.MIDDLEWARE[0])
                            self.assertTrue('some_middleware' in local_settings.MIDDLEWARE)

                        boilerplate_settings = get_boilerplates_settings()

                        if DJANGO_1_7:
                            # Check the loaders
                            self.assertTrue('django.template.loaders.app_directories.Loader' in local_settings.TEMPLATE_LOADERS)
                            # Loaders declared in settings
                            self.assertTrue('admin_tools.template_loaders.Loader' in local_settings.TEMPLATE_LOADERS)
                            # Existing application is kept
                            self.assertTrue('django.core.context_processors.request' in local_settings.TEMPLATE_CONTEXT_PROCESSORS)
                            # New one is added
                            self.assertTrue('django.core.context_processors.debug' in local_settings.TEMPLATE_CONTEXT_PROCESSORS)
                            # Check template dirs
                            self.assertTrue('some/dir' in local_settings.TEMPLATE_DIRS)
                            # Check for aldryn boilerplates
                            for name, value in boilerplate_settings.items():
                                if type(value) in (list, tuple):
                                    self.assertTrue(set(getattr(local_settings, name)).intersection(set(value)))
                                elif name == 'ALDRYN_BOILERPLATE_NAME':
                                    self.assertEqual(getattr(local_settings, name), 'legacy')
                                else:
                                    self.assertTrue(value in getattr(local_settings, name))
                        else:
                            # Check the loaders
                            self.assertTrue('django.template.loaders.app_directories.Loader' in local_settings.TEMPLATES[0]['OPTIONS']['loaders'])
                            # Loaders declared in settings
                            self.assertTrue('admin_tools.template_loaders.Loader' in local_settings.TEMPLATES[0]['OPTIONS']['loaders'])
                            # Existing application is kept
                            self.assertTrue('django.template.context_processors.request' in local_settings.TEMPLATES[0]['OPTIONS']['context_processors'])
                            # New one is added
                            self.assertTrue('django.template.context_processors.debug' in local_settings.TEMPLATES[0]['OPTIONS']['context_processors'])
                            # Check template dirs
                            self.assertTrue('some/dir' in local_settings.TEMPLATES[0]['DIRS'])
                            # Check for aldryn boilerplates
                            for name, value in boilerplate_settings.items():
                                if not name.startswith('TEMPLATE'):
                                    if type(value) in (list, tuple):
                                        self.assertTrue(set(getattr(local_settings, name)).intersection(set(value)))
                                    elif name == 'ALDRYN_BOILERPLATE_NAME':
                                        self.assertEqual(getattr(local_settings, name), 'legacy')
                                    else:
                                        self.assertTrue(value in getattr(local_settings, name))
                                elif name == 'TEMPLATE_CONTEXT_PROCESSORS':
                                    self.assertTrue(set(local_settings.TEMPLATES[0]['OPTIONS']['context_processors']).intersection(set(value)))
                                elif name == 'TEMPLATE_LOADERS':

                                    self.assertTrue(set(local_settings.TEMPLATES[0]['OPTIONS']['loaders']).intersection(set(value)))

    @patch('djangocms_helper.main.autoreload')
    def test_server(self, mocked_command):
        with work_in(self.basedir):
            with captured_output() as (out, err):
                args = copy(DEFAULT_ARGS)
                args['server'] = True
                core(args, self.application)
            self.assertTrue(
                'A admin user (username: admin, password: admin) has been created.' in
                out.getvalue()
            )

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
                args['--extra-settings'] = 'cms_helper.py'
                args['--migrate'] = False
                core(args, self.application)
            self.assertTrue('Installation okay' in out.getvalue())
            self.assertFalse('[WARNING]' in out.getvalue())
            self.assertFalse('[ERROR]' in out.getvalue())

    @unittest.skipIf(LooseVersion(django.get_version()) > LooseVersion('1.8'),
                     reason='Test for Django up until 1.8')
    def test_cms_check_nocms(self):
        try:
            import cms
            raise unittest.SkipTest('django CMS available, skipping test')
        except ImportError:
            pass
        with work_in(self.basedir):
            with captured_output() as (out, err):
                shutil.copy(self.poexample, self.pofile)
                args = copy(DEFAULT_ARGS)
                args['cms_check'] = True
                args['--extra-settings'] = 'cms_helper.py'
                args['--migrate'] = False
                core(args, self.application)
            self.assertTrue('cms_check available only if django CMS is installed' in out.getvalue())

    @unittest.skipIf(LooseVersion(django.get_version()) < LooseVersion('1.9'),
                     reason='Test for Django 1.9+')
    def test_cms_check_nocms_19(self):
        try:
            import cms
            raise unittest.SkipTest('django CMS available, skipping test')
        except ImportError:
            pass
        with work_in(self.basedir):
            with self.assertRaises(ImportError):
                shutil.copy(self.poexample, self.pofile)
                args = copy(DEFAULT_ARGS)
                args['cms_check'] = True
                args['--extra-settings'] = 'cms_helper.py'
                args['--migrate'] = False
                core(args, self.application)

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
        self.assertFalse(os.path.exists(args['STATIC_ROOT']))
        self.assertFalse(os.path.exists(args['MEDIA_ROOT']))

    def test_pyflakes_nocms(self):
        try:
            import cms
            raise unittest.SkipTest('django CMS available, skipping test')
        except ImportError:
            pass
        with work_in(self.basedir):
            with captured_output() as (out, err):
                args = copy(DEFAULT_ARGS)
                args['pyflakes'] = True
                core(args, self.application)
            self.assertTrue('Static analisys available only if django CMS is installed' in out.getvalue())
        self.assertFalse(os.path.exists(args['STATIC_ROOT']))
        self.assertFalse(os.path.exists(args['MEDIA_ROOT']))

    @unittest.skipIf(sys.version_info < (2, 7),
                     reason='Example test non discoverable in Python 2.6')
    def test_testrun(self):
        try:
            import cms
        except ImportError:
            raise unittest.SkipTest('django CMS not available, skipping test')
        with work_in(self.basedir):
            with captured_output() as (out, err):
                with self.assertRaises(SystemExit) as exit:
                    try:
                        from django.test.utils import _TestState
                        del _TestState.saved_data
                    except (ImportError, AttributeError):
                        pass
                    args = copy(DEFAULT_ARGS)
                    args['test'] = True
                    args['--persistent'] = mkdtemp()
                    args['--runner'] = 'runners.CapturedOutputRunner'
                    core(args, self.application)
        self.assertTrue('Ran 12 tests in' in err.getvalue())
        self.assertEqual(exit.exception.code, 0)
        self.assertTrue(os.path.exists(args['STATIC_ROOT']))
        self.assertTrue(os.path.exists(args['MEDIA_ROOT']))

    @unittest.skipIf(sys.version_info < (2, 7),
                     reason='Example test non discoverable in Python 2.6')
    def test_runner_wrong(self):
        try:
            import cms
        except ImportError:
            raise unittest.SkipTest('django CMS not available, skipping test')
        with work_in(self.basedir):
            with captured_output():
                if sys.version_info < (3, 5):
                    exception = ImportError
                else:
                    exception = SystemExit
                with self.assertRaises(exception) as exit:
                    args = list()
                    args.append('djangocms_helper')
                    args.append('test')
                    args.append('example1')
                    args.append('--runner=runners.CapturedOutputRunner')
                    args.append('whatever')
                    runner.cms('example1', args)
        if sys.version_info >= (3, 5):
            self.assertEqual(exit.exception.code, 1)

    @unittest.skipIf(sys.version_info < (2, 7),
                     reason='Example test non discoverable in Python 2.6')
    def test_runner(self):
        try:
            import cms
        except ImportError:
            raise unittest.SkipTest('django CMS not available, skipping test')
        from djangocms_helper.test_utils.runners import CapturedOutputRunner
        with patch('django.test.runner.DiscoverRunner', CapturedOutputRunner):
            with work_in(self.basedir):
                with captured_output() as (out, err):
                    with self.assertRaises(SystemExit) as exit:
                        args = list()
                        args.append('djangocms_helper')
                        args.append('test')
                        args.append('example1')
                        runner.cms('example1', args)
        self.assertTrue('visible string' in out.getvalue())
        self.assertFalse('hidden string' in out.getvalue())
        self.assertFalse('hidden string' in err.getvalue())
        self.assertTrue('Ran 12 tests in' in err.getvalue())
        self.assertEqual(exit.exception.code, 0)

    @unittest.skipIf(sys.version_info < (2, 7),
                     reason='Example test non discoverable in Python 2.6')
    def test_runner_cms_exception(self):
        try:
            import cms
            raise unittest.SkipTest('django CMS available, skipping test')
        except ImportError:
            pass
        from djangocms_helper.test_utils.runners import CapturedOutputRunner
        with patch('django.test.runner.DiscoverRunner', CapturedOutputRunner):
            with work_in(self.basedir):
                with captured_output() as (out, err):
                    with self.assertRaises(ImportError) as exit:
                        args = list()
                        args.append('djangocms_helper')
                        runner.cms('example1', args)

    @unittest.skipIf(sys.version_info < (2, 7),
                     reason='Example test non discoverable in Python 2.6')
    def test_runner_cms_exception(self):
        try:
            import cms
            raise unittest.SkipTest('django CMS available, skipping test')
        except ImportError:
            pass
        from djangocms_helper.test_utils.runners import CapturedOutputRunner
        with patch('django.test.runner.DiscoverRunner', CapturedOutputRunner):
            with work_in(self.basedir):
                with captured_output() as (out, err):
                    with self.assertRaises(ImportError) as exit:
                        args = list()
                        args.append('djangocms_helper')
                        runner.cms('example1', args)

    def test_runner_cms_argv(self):
        try:
            import cms
        except ImportError:
            raise unittest.SkipTest('django CMS not available, skipping test')

        def fake_runner(argv):
            return argv

        from djangocms_helper.test_utils.runners import CapturedOutputRunner
        with patch('django.test.runner.DiscoverRunner', CapturedOutputRunner):
            with work_in(self.basedir):
                with captured_output() as (out, err):
                    args = list()
                    args.append('djangocms_helper')
                    with patch('djangocms_helper.runner.runner', fake_runner):
                        data = runner.cms('example1', args)
                    self.assertEqual(data, ['djangocms_helper', 'example1', 'test', '--cms'])

    def test_runner_argv(self):
        def fake_runner(argv):
            return argv

        from djangocms_helper.test_utils.runners import CapturedOutputRunner
        with patch('django.test.runner.DiscoverRunner', CapturedOutputRunner):
            with work_in(self.basedir):
                with captured_output() as (out, err):
                    args = list()
                    args.append('djangocms_helper')
                    with patch('djangocms_helper.runner.runner', fake_runner):
                        data = runner.run('example1', args)
                    self.assertEqual(data, [u'djangocms_helper', u'example1', u'test'])

    def test_setup_cms(self):
        try:
            import cms
        except ImportError:
            raise unittest.SkipTest('django CMS not available, skipping test')
        with work_in(self.basedir):
            with captured_output() as (out, err):
                from djangocms_helper.test_utils import cms_helper
                settings = runner.setup(
                    'example1', cms_helper, use_cms=True, extra_args=['--boilerplate']
                )
        self.assertTrue('example2' in settings.INSTALLED_APPS)
        self.assertTrue('aldryn_boilerplates' in settings.INSTALLED_APPS)
        self.assertTrue('cms' in settings.INSTALLED_APPS)

    def test_setup_nocms(self):
        with work_in(self.basedir):
            with captured_output() as (out, err):
                from djangocms_helper.test_utils import cms_helper
                settings = runner.setup('example1', cms_helper, extra_args=[])
        self.assertTrue('example2' in settings.INSTALLED_APPS)
        self.assertFalse('aldryn_boilerplates' in settings.INSTALLED_APPS)
        self.assertFalse('cms' in settings.INSTALLED_APPS)

    @unittest.skipIf(sys.version_info < (2, 7),
                     reason='Example test non discoverable in Python 2.6')
    @unittest.skipIf(LooseVersion(django.get_version()) >= LooseVersion('1.8'),
                     reason='Simple runner not available in Django > 1.8')
    def test_runner_simple(self):
        try:
            import cms
        except ImportError:
            raise unittest.SkipTest('django CMS not available, skipping test')
        from djangocms_helper.test_utils.runners import CapturedOutputSimpleRunner
        with patch('django.test.simple.DjangoTestSuiteRunner', CapturedOutputSimpleRunner):
            with work_in(self.basedir):
                with captured_output() as (out, err):
                    with self.assertRaises(SystemExit) as exit:
                        args = list()
                        args.append('djangocms_helper')
                        args.append('test')
                        args.append('example1')
                        args.append('--simple-runner')
                        args.append('example1.FakeTests')
                        runner.cms('example1', args)
        self.assertTrue('Ran 12 tests in' in err.getvalue())
        self.assertEqual(exit.exception.code, 0)

    @unittest.skipIf(sys.version_info < (2, 7),
                     reason='Example test non discoverable in Python 2.6')
    def test_runner_nose(self):
        try:
            import cms
        except ImportError:
            raise unittest.SkipTest('django CMS not available, skipping test')
        with work_in(self.basedir):
            with captured_output() as (out, err):
                with self.assertRaises(SystemExit) as exit:
                    args = list()
                    args.append('djangocms_helper')
                    args.append('test')
                    args.append('example1')
                    args.append('--nose-runner')
                    args.append('example1.tests')
                    runner.cms('example1', args)
        self.assertTrue('Ran 24 tests in' in err.getvalue())
        self.assertEqual(exit.exception.code, 0)

    @unittest.skipIf(sys.version_info < (2, 7),
                     reason='Example test non discoverable in Python 2.6')
    def test_testrun_nocms(self):
        with work_in(self.basedir):
            with captured_output() as (out, err):
                with self.assertRaises(SystemExit) as exit:
                    try:
                        from django.test.utils import _TestState
                        del _TestState.saved_data
                    except (ImportError, AttributeError):
                        pass
                    args = copy(DEFAULT_ARGS)
                    args['test'] = True
                    args['--cms'] = False
                    args['--runner'] = 'runners.CapturedOutputRunner'
                    core(args, self.application)
        self.assertTrue('Ran 12 tests in' in err.getvalue())
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
                    args.append('--extra-settings=cms_helper.py')
                    args.append('--runner=runners.CapturedOutputRunner')
                    runner.run('example1', args)
        self.assertTrue('Ran 12 tests in' in err.getvalue())
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
                try:
                    from django.test.utils import _TestState
                    del _TestState.saved_data
                except (ImportError, AttributeError):
                    pass
                args = copy(DEFAULT_ARGS)
                args['<command>'] = 'test'
                args['--cms'] = False
                args['--native'] = True
                args['--extra-settings'] = 'cms_helper_extra_runner.py'
                core(args, self.application)
        self.assertTrue('Ran 12 tests in' in err.getvalue())

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
