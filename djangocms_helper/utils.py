# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import contextlib
import os
import shutil
import sys
from distutils.version import LooseVersion
from tempfile import mkdtemp

import django
from django.core.management import call_command
from django.core.urlresolvers import clear_url_caches
from django.utils import six
from django.utils.functional import empty
from django.utils.six import StringIO
from django.utils.six.moves import reload_module
from mock import patch

from . import HELPER_FILE

try:
    from collections import OrderedDict
except ImportError:
    from django.utils.datastructures import SortedDict as OrderedDict

try:
    import cms  # NOQA
    CMS = True
    CMS_32 = LooseVersion('3.2') <= LooseVersion(cms.__version__) < LooseVersion('3.3')
    CMS_31 = LooseVersion('3.1') <= LooseVersion(cms.__version__) < LooseVersion('3.2')
    CMS_30 = LooseVersion('3.0') <= LooseVersion(cms.__version__) < LooseVersion('3.1')
except ImportError:  # pragma: no cover
    CMS = False
    CMS_32 = False
    CMS_31 = False
    CMS_30 = False

DJANGO_1_4 = LooseVersion(django.get_version()) < LooseVersion('1.5')
DJANGO_1_5 = LooseVersion(django.get_version()) < LooseVersion('1.6')
DJANGO_1_6 = LooseVersion(django.get_version()) < LooseVersion('1.7')
DJANGO_1_7 = LooseVersion(django.get_version()) < LooseVersion('1.8')
DJANGO_1_8 = LooseVersion(django.get_version()) < LooseVersion('1.9')
DJANGO_1_9 = LooseVersion(django.get_version()) < LooseVersion('1.10')


def load_from_file(module_path):
    """
    Load a python module from its absolute filesystem path

    Borrowed from django-cms
    """
    from imp import load_module, PY_SOURCE

    imported = None
    if module_path:
        with open(module_path, 'r') as openfile:
            imported = load_module('mod', openfile, module_path, ('imported', 'r', PY_SOURCE))
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
    with patch('sys.stdout', new_callable=StringIO) as out:
        with patch('sys.stderr', new_callable=StringIO) as err:
            yield out, err


# Borrowed from django CMS codebase
@contextlib.contextmanager
def temp_dir(suffix='', container='/dev/shm/'):
    name = make_temp_dir(suffix, container)
    yield name
    shutil.rmtree(name)


def make_temp_dir(suffix='', container='/dev/shm/'):
    if os.path.exists(container):
        return mkdtemp(suffix=suffix, dir=container)
    return mkdtemp(suffix=suffix)


@contextlib.contextmanager
def persistent_dir(suffix, container='data'):
    name = os.path.abspath(os.path.join(container, suffix))
    if not os.path.exists(name):
        os.makedirs(name)
    yield name


class DisableMigrations(object):

    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return 'notmigrations'


def _reset_django(settings):
    """
    Hackish way to reset the django instance settings and AppConfig
    :param settings: django settings module
    """
    if settings._wrapped != empty:
        clear_url_caches()
        if DJANGO_1_6:
            from django.db.models.loading import cache as apps
            apps.app_store = OrderedDict()
            apps.loaded = False
            apps.handled = set()
            apps.postponed = []
            apps.nesting_level = 0
            apps._get_models_cache = {}
        else:
            from django.apps import apps
            apps.clear_cache()
        settings._wrapped = empty
        clear_url_caches()


def extend_settings(settings, extra_settings, key, insertion_point):
    for item in extra_settings[key]:
        if item not in settings[key]:
            settings[key].insert(settings[key].index(insertion_point), item)
    return settings


def _make_settings(args, application, settings, STATIC_ROOT, MEDIA_ROOT):
    """
    Setup the Django settings
    :param args: docopt arguments
    :param default_settings: default Django settings
    :param settings: Django settings module
    :param STATIC_ROOT: static root directory
    :param MEDIA_ROOT: media root directory
    :return:
    """
    import dj_database_url
    from .default_settings import get_default_settings, get_boilerplates_settings

    try:
        extra_settings_file = args.get('--extra-settings')
        if not extra_settings_file:
            extra_settings_file = HELPER_FILE
        if extra_settings_file[-3:] != '.py':
            filename, __ = os.path.splitext(extra_settings_file)
            extra_settings_file = '{0}.py'.format(filename)
        extra_settings = load_from_file(extra_settings_file).HELPER_SETTINGS
    except (IOError, AttributeError):
        extra_settings = None
    default_name = ':memory:' if args['test'] else 'local.sqlite'
    db_url = os.environ.get('DATABASE_URL', 'sqlite://localhost/%s' % default_name)
    configs = {
        'DATABASES': {'default': dj_database_url.parse(db_url)},
        'STATIC_ROOT': STATIC_ROOT,
        'MEDIA_ROOT': MEDIA_ROOT,
        'USE_TZ': True,
        'USE_CMS': args['--cms'],
        'BASE_APPLICATION': application
    }

    if configs['USE_CMS'] or getattr(extra_settings, 'USE_CMS', False):
        CMS_APPS = [
            'cms',
            'menus',
            'sekizai',
        ]
        CMS_APP_STYLE = [
            'djangocms_admin_style'
        ]
        CMS_PROCESSORS = [
            'cms.context_processors.cms_settings',
            'sekizai.context_processors.sekizai',
        ]
        CMS_MIDDLEWARE = [
            'cms.middleware.language.LanguageCookieMiddleware',
            'cms.middleware.user.CurrentUserMiddleware',
            'cms.middleware.page.CurrentPageMiddleware',
            'cms.middleware.toolbar.ToolbarMiddleware',
        ]
        URLCONF = 'djangocms_helper.urls'
    else:
        CMS_APPS = []
        CMS_APP_STYLE = []
        CMS_MIDDLEWARE = []
        CMS_PROCESSORS = []
        URLCONF = 'djangocms_helper.urls'

    CMS_1_7_MIGRATIONS = {}
    try:
        import cms.migrations_django  # NOQA # nopyflakes
        CMS_1_7_MIGRATIONS['cms'] = 'cms.migrations_django'
        CMS_1_7_MIGRATIONS['menus'] = 'menus.migrations_django'
    except ImportError:
        # we're using the Django 1.7 migrations
        pass
    try:  # pragma: no cover
        import djangocms_text_ckeditor.migrations_django  # NOQA # nopyflakes
        CMS_1_7_MIGRATIONS['djangocms_text_ckeditor'] = 'djangocms_text_ckeditor.migrations_django'
    except ImportError:  # pragma: no cover
        # we're using the Django 1.7 migrations
        pass
    try:  # pragma: no cover
        import filer.migrations_django  # NOQA # nopyflakes # pragma: no cover
        CMS_1_7_MIGRATIONS['filer'] = 'filer.migrations_django'
    except ImportError:  # pragma: no cover
        # we're using the Django 1.7 migrations
        pass
    try:  # pragma: no cover
        import cmsplugin_filer_image.migrations_django  # NOQA # nopyflakes
        CMS_1_7_MIGRATIONS['cmsplugin_filer_file'] = 'cmsplugin_filer_file.migrations_django'
        CMS_1_7_MIGRATIONS['cmsplugin_filer_folder'] = 'cmsplugin_filer_folder.migrations_django'
        CMS_1_7_MIGRATIONS['cmsplugin_filer_image'] = 'cmsplugin_filer_image.migrations_django'
        CMS_1_7_MIGRATIONS['cmsplugin_filer_link'] = 'cmsplugin_filer_link.migrations_django'
        CMS_1_7_MIGRATIONS['cmsplugin_filer_teaser'] = 'cmsplugin_filer_teaser.migrations_django'
        CMS_1_7_MIGRATIONS['cmsplugin_filer_video'] = 'cmsplugin_filer_video.migrations_django'
    except ImportError:  # pragma: no cover
        # we're using the Django 1.7 migrations
        pass

    default_settings = get_default_settings(CMS_APPS, CMS_PROCESSORS, CMS_MIDDLEWARE,
                                            CMS_APP_STYLE, URLCONF, application)
    migrate = args.get('--migrate') or not args.get('--no-migrate')
    configs['SOUTH_TESTS_MIGRATE'] = migrate
    default_settings.update(configs)

    if extra_settings:
        apps = extra_settings.pop('INSTALLED_APPS', [])
        apps_top = extra_settings.pop('TOP_INSTALLED_APPS', [])
        template_processors = extra_settings.pop('TEMPLATE_CONTEXT_PROCESSORS', [])
        template_loaders = extra_settings.pop('TEMPLATE_LOADERS', [])
        template_dirs = extra_settings.pop('TEMPLATE_DIRS', [])
        middleware = extra_settings.pop('MIDDLEWARE_CLASSES', [])
        middleware_top = extra_settings.pop('TOP_MIDDLEWARE_CLASSES', [])
        default_settings.update(extra_settings)
        for app in apps_top:
            default_settings['INSTALLED_APPS'].insert(0, app)
        default_settings['INSTALLED_APPS'].extend(apps)
        default_settings['TEMPLATE_CONTEXT_PROCESSORS'].extend(template_processors)
        default_settings['TEMPLATE_LOADERS'].extend(template_loaders)
        if 'TEMPLATE_DIRS' not in default_settings:
            default_settings['TEMPLATE_DIRS'] = []
        default_settings['TEMPLATE_DIRS'].extend(template_dirs)
        default_settings['MIDDLEWARE_CLASSES'].extend(middleware)
        for middleware in middleware_top:
            default_settings['MIDDLEWARE_CLASSES'].insert(0, middleware)

    if DJANGO_1_6:
        default_settings['INSTALLED_APPS'].append('south')
    elif args['--cms']:
        default_settings['MIGRATION_MODULES'].update(CMS_1_7_MIGRATIONS)

    if 'cms' in default_settings['INSTALLED_APPS']:
        if CMS_30:
            if 'mptt' not in default_settings['INSTALLED_APPS']:
                default_settings['INSTALLED_APPS'].append('mptt')
        else:
            if 'treebeard' not in default_settings['INSTALLED_APPS']:
                default_settings['INSTALLED_APPS'].append('treebeard')
    if ('filer' in default_settings['INSTALLED_APPS'] and
            'mptt' not in default_settings['INSTALLED_APPS']):
        default_settings['INSTALLED_APPS'].append('mptt')

    if args['--boilerplate']:
        boilerplate_settings = get_boilerplates_settings()

        # Do not override helper settings with defaults.
        if 'ALDRYN_BOILERPLATE_NAME' in default_settings.keys():
            del boilerplate_settings['ALDRYN_BOILERPLATE_NAME']

        default_settings = extend_settings(
            default_settings, boilerplate_settings, 'STATICFILES_FINDERS',
            'django.contrib.staticfiles.finders.AppDirectoriesFinder'
        )
        del boilerplate_settings['STATICFILES_FINDERS']

        default_settings = extend_settings(
            default_settings, boilerplate_settings, 'TEMPLATE_LOADERS',
            'django.template.loaders.app_directories.Loader'
        )
        del boilerplate_settings['TEMPLATE_LOADERS']

        for setting in ('INSTALLED_APPS', 'TEMPLATE_CONTEXT_PROCESSORS'):
            default_settings[setting].extend(boilerplate_settings[setting])
            del boilerplate_settings[setting]
        default_settings.update(boilerplate_settings)

    if not DJANGO_1_7:
        default_settings['TEMPLATES'] = [
            {'NAME': 'django',
             'BACKEND': 'django.template.backends.django.DjangoTemplates',
             'OPTIONS': {
                 'context_processors': [
                     template_processor.replace('django.core', 'django.template')
                     for template_processor in default_settings.pop('TEMPLATE_CONTEXT_PROCESSORS')
                 ],
                 'loaders': default_settings.pop('TEMPLATE_LOADERS')
             }}
        ]
        if 'TEMPLATE_DIRS' in default_settings:
            default_settings['TEMPLATES'][0]['DIRS'] = default_settings.pop('TEMPLATE_DIRS')

    # Support for custom user models
    if 'AUTH_USER_MODEL' in os.environ:
        custom_user_app = os.environ['AUTH_USER_MODEL'].rpartition('.')[0]
        custom_user_model = '.'.join(os.environ['AUTH_USER_MODEL'].split('.')[-2:])
        default_settings['INSTALLED_APPS'].insert(
            default_settings['INSTALLED_APPS'].index('cms'),
            custom_user_app
        )
        default_settings['AUTH_USER_MODEL'] = custom_user_model

    if args['test']:
        default_settings['SESSION_ENGINE'] = 'django.contrib.sessions.backends.cache'
    if application not in default_settings['INSTALLED_APPS']:
        default_settings['INSTALLED_APPS'].append(application)

    if not DJANGO_1_6 and not migrate:
        default_settings['MIGRATION_MODULES'] = DisableMigrations()

    _reset_django(settings)
    settings.configure(**default_settings)
    if not DJANGO_1_6:
        django.setup()
    elif 'south' in settings.INSTALLED_APPS:
        from south.management.commands import patch_for_test_db_setup
        patch_for_test_db_setup()
    reload_urls(settings, cms_apps=False)
    return settings


def reload_urls(settings, urlconf=None, cms_apps=True):
    if 'cms.urls' in sys.modules:
        reload_module(sys.modules['cms.urls'])
    if urlconf is None:
        urlconf = settings.ROOT_URLCONF
    if urlconf in sys.modules:
        reload_module(sys.modules[urlconf])
    clear_url_caches()
    if cms_apps:
        try:
            from cms.appresolver import clear_app_resolvers, get_app_patterns
            clear_app_resolvers()
            get_app_patterns()
        except ImportError:
            pass


def _create_db(migrate_cmd=False):
    if DJANGO_1_6:
        if migrate_cmd:
            call_command('syncdb', interactive=False, verbosity=1, database='default')
            call_command('migrate', interactive=False, verbosity=1, database='default')
        else:
            call_command('syncdb', interactive=False, verbosity=1, database='default',
                         migrate=False, migrate_all=True)
            call_command('migrate', interactive=False, verbosity=1, database='default',
                         fake=True)
    else:
        call_command('migrate')


def get_user_model():
    from django.contrib.auth import get_user_model
    return get_user_model()


def create_user(username, email, password, is_staff=False, is_superuser=False,
                base_cms_permissions=False, permissions=None):
    from django.contrib.auth.models import Permission
    User = get_user_model()

    try:
        if User.USERNAME_FIELD == 'email':
            user = User.objects.get(**{User.USERNAME_FIELD: email})
        else:
            user = User.objects.get(**{User.USERNAME_FIELD: username})
    except User.DoesNotExist:
        user = User()

    if User.USERNAME_FIELD != 'email':
        setattr(user, User.USERNAME_FIELD, username)

    user.email = email
    user.set_password(password)
    if is_superuser:
        user.is_superuser = True
    if is_superuser or is_staff:
        user.is_staff = True
    user.is_active = True
    user.save()
    if user.is_staff and not is_superuser and base_cms_permissions:
        user.user_permissions.add(Permission.objects.get(codename='add_text'))
        user.user_permissions.add(Permission.objects.get(codename='delete_text'))
        user.user_permissions.add(Permission.objects.get(codename='change_text'))
        user.user_permissions.add(Permission.objects.get(codename='publish_page'))

        user.user_permissions.add(Permission.objects.get(codename='add_page'))
        user.user_permissions.add(Permission.objects.get(codename='change_page'))
        user.user_permissions.add(Permission.objects.get(codename='delete_page'))
    if is_staff and not is_superuser and permissions:
        for permission in permissions:
            user.user_permissions.add(Permission.objects.get(codename=permission))
    return user


def get_user_model_labels():
    User = get_user_model()

    user_orm_label = '%s.%s' % (User._meta.app_label, User._meta.object_name)
    user_model_label = '%s.%s' % (User._meta.app_label, User._meta.model_name)
    return user_orm_label, user_model_label


class UserLoginContext(object):
    def __init__(self, testcase, user, password=None):
        self.testcase = testcase
        self.user = user
        if password is None:
            password = getattr(user, get_user_model().USERNAME_FIELD)
        self.password = password

    def __enter__(self):
        loginok = self.testcase.client.login(username=getattr(self.user,
                                                              get_user_model().USERNAME_FIELD),
                                             password=self.password)
        self.testcase.assertTrue(loginok)
        self.testcase._login_context = self

    def __exit__(self, exc, value, tb):
        self.testcase._login_context = None
        self.testcase.client.logout()


def ensure_unicoded_and_unique(args_list):
    """
    Iterate over args_list, make it unicode if needed and ensure that there
    are no duplicates.
    Returns list of unicoded arguments in the same order.
    """
    unicoded_args = []
    for argument in args_list:
        argument = (six.u(argument)
                    if not isinstance(argument, six.text_type) else argument)
        if argument not in unicoded_args:
            unicoded_args.append(argument)
    return unicoded_args
