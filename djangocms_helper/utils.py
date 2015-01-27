# -*- coding: utf-8 -*-
import contextlib
from distutils.version import LooseVersion
import os
import random
import shutil
import stat
import sys
from tempfile import mkdtemp

import django
from django.core.management import call_command
from django.core.urlresolvers import clear_url_caches
from django.utils.datastructures import SortedDict
from django.utils.functional import empty
from django.utils.six import StringIO

try:
    import cms  # NOQA
    CMS_31 = LooseVersion('3.1') <= LooseVersion(cms.__version__) < LooseVersion('3.2')
    CMS_30 = LooseVersion('3.0') <= LooseVersion(cms.__version__) < LooseVersion('3.1')
except ImportError:
    CMS_31 = False
    CMS_30 = False

DJANGO_1_4 = LooseVersion(django.get_version()) < LooseVersion('1.5')
DJANGO_1_5 = LooseVersion(django.get_version()) < LooseVersion('1.6')
DJANGO_1_6 = LooseVersion(django.get_version()) < LooseVersion('1.7')
DJANGO_1_7 = LooseVersion(django.get_version()) < LooseVersion('1.8')


from . import HELPER_FILE


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


# Borrowed from django CMS codebase
@contextlib.contextmanager
def temp_dir():
    name = make_temp_dir()
    yield name
    shutil.rmtree(name)


def make_temp_dir():
    if os.path.exists('/dev/shm/'):
        if os.stat('/dev/shm').st_mode & stat.S_IWGRP:
            dirname = 'djangocms-helpder-%s' % random.randint(1, 1000000)
            path = os.path.join('/dev/shm', dirname)
            while os.path.exists(path):
                dirname = 'djangocms-helpder-%s' % random.randint(1, 1000000)
                path = os.path.join('/dev/shm', dirname)
                os.mkdir(path)
                return path
    return mkdtemp()


def _reset_django(settings):
    """
    Hackish way to reset the django instance settings and AppConfig
    :param settings: django settings module
    """
    if settings._wrapped != empty:
        clear_url_caches()
        if DJANGO_1_5:
            from django.db.models.loading import cache as apps
            apps.app_store = SortedDict()
            apps.loaded = False
            apps.handled = {}
            apps.postponed = []
            apps.nesting_level = 0
            apps._get_models_cache = {}
        elif DJANGO_1_6:
            from django.db.models.loading import cache as apps
            apps.app_store = SortedDict()
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
    from .default_settings import get_default_settings

    try:
        extra_settings_file = args.get('--extra-settings')
        if not extra_settings_file:
            extra_settings_file = HELPER_FILE
        if extra_settings_file[-3:] != '.py':
            extra_settings_file = '%s.py' % extra_settings_file
        extra_settings = load_from_file(extra_settings_file).HELPER_SETTINGS
    except (IOError, AttributeError):
        extra_settings = None
    default_name = ':memory:' if not args['server'] else 'local.sqlite'
    db_url = os.environ.get("DATABASE_URL", "sqlite://localhost/%s" % default_name)
    migrate = args.get('--migrate', False)
    configs = {
        'DATABASES': {'default': dj_database_url.parse(db_url)},
        'STATIC_ROOT': STATIC_ROOT,
        'MEDIA_ROOT': MEDIA_ROOT,
        'USE_TZ': True,
        'SOUTH_TESTS_MIGRATE': migrate,
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
            'django.contrib.messages.context_processors.messages',
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

    if CMS_30:
        CMS_1_7_MIGRATIONS = {
            'cms': 'cms.migrations_django',
            'menus': 'menus.migrations_django',
            'djangocms_text_ckeditor': 'djangocms_text_ckeditor.migrations_django',
            'filer': 'filer.migrations_django',
            'cmsplugin_filer_image': 'cmsplugin_filer_image.migrations_django',
            'cmsplugin_filer_file': 'cmsplugin_filer_file.migrations_django',
            'cmsplugin_filer_folder': 'cmsplugin_filer_folder.migrations_django',
        }
    else:
        CMS_1_7_MIGRATIONS = {
            'djangocms_text_ckeditor': 'djangocms_text_ckeditor.migrations_django',
            'filer': 'filer.migrations_django',
            'cmsplugin_filer_image': 'cmsplugin_filer_image.migrations_django',
            'cmsplugin_filer_file': 'cmsplugin_filer_file.migrations_django',
            'cmsplugin_filer_folder': 'cmsplugin_filer_folder.migrations_django',
        }
    default_settings = get_default_settings(CMS_APPS, CMS_PROCESSORS,
                                            CMS_MIDDLEWARE, CMS_APP_STYLE,
                                            URLCONF, application)

    default_settings.update(configs)

    if extra_settings:
        apps = extra_settings.get('INSTALLED_APPS', [])
        template_processors = extra_settings.get('TEMPLATE_CONTEXT_PROCESSORS', [])
        middleware = extra_settings.get('MIDDLEWARE_CLASSES', [])
        if 'INSTALLED_APPS' in extra_settings:
            del(extra_settings['INSTALLED_APPS'])
        if 'TEMPLATE_CONTEXT_PROCESSORS' in extra_settings:
            del(extra_settings['TEMPLATE_CONTEXT_PROCESSORS'])
        if 'MIDDLEWARE_CLASSES' in extra_settings:
            del(extra_settings['MIDDLEWARE_CLASSES'])
        if application in default_settings['INSTALLED_APPS'] and application in apps:
            default_settings['INSTALLED_APPS'].remove(application)
        default_settings.update(extra_settings)
        default_settings['INSTALLED_APPS'].extend(apps)
        default_settings['TEMPLATE_CONTEXT_PROCESSORS'].extend(template_processors)
        default_settings['MIDDLEWARE_CLASSES'].extend(middleware)

    if DJANGO_1_6:
        default_settings['INSTALLED_APPS'].append('south')
    elif args['--cms']:
        default_settings['MIGRATION_MODULES'].update(CMS_1_7_MIGRATIONS)
    if CMS_31:
        if 'treebeard' not in default_settings['INSTALLED_APPS']:
            default_settings['INSTALLED_APPS'].append('treebeard')
        if ('filer' in default_settings['INSTALLED_APPS'] and 
                'mptt' not in default_settings['INSTALLED_APPS']):
            default_settings['INSTALLED_APPS'].append('mptt')
    else:
        if ('cms' in default_settings['INSTALLED_APPS'] and
                'mptt' not in default_settings['INSTALLED_APPS']):
            default_settings['INSTALLED_APPS'].append('mptt')

    # Support for custom user models
    if django.VERSION >= (1, 5) and 'AUTH_USER_MODEL' in os.environ:
        custom_user_app = os.environ['AUTH_USER_MODEL'].rpartition('.')[0]
        custom_user_model = '.'.join(os.environ['AUTH_USER_MODEL'].split('.')[-2:])
        default_settings['INSTALLED_APPS'].insert(default_settings['INSTALLED_APPS'].index('cms'), custom_user_app)
        default_settings['AUTH_USER_MODEL'] = custom_user_model

    if args['test']:
        default_settings['SESSION_ENGINE'] = "django.contrib.sessions.backends.cache"

    _reset_django(settings)
    settings.configure(**default_settings)
    if not DJANGO_1_6:
        django.setup()
    if 'south' in settings.INSTALLED_APPS:
        from south.management.commands import patch_for_test_db_setup
        patch_for_test_db_setup()
    reload_urls(settings)
    return settings


def reload_urls(settings):
    url_modules = [
        settings.ROOT_URLCONF,
    ]

    clear_url_caches()

    for module in url_modules:
        if module in sys.modules:
            del sys.modules[module]


def _create_db(migrate_cmd=False):
    if DJANGO_1_6:
        if migrate_cmd:
            call_command("syncdb", interactive=False, verbosity=1, database='default')
            call_command("migrate", interactive=False, verbosity=1, database='default')
        else:
            call_command("syncdb", interactive=False, verbosity=1, database='default',
                         migrate=False, migrate_all=True)
            call_command("migrate", interactive=False, verbosity=1, database='default',
                         fake=True)
    else:
        call_command("migrate")


def get_user_model():
    # Django 1.5+ compatibility
    if django.VERSION >= (1, 5):
        from django.contrib.auth import get_user_model
    else:
        from django.contrib.auth.models import User
        User.USERNAME_FIELD = 'username'
        get_user_model = lambda: User
    return get_user_model()


def create_user(username, email, password, is_staff=False, is_superuser=False):
    User = get_user_model()
    usr = User()

    if User.USERNAME_FIELD != 'email':
        setattr(usr, User.USERNAME_FIELD, username)

    usr.email = email
    usr.set_password(password)
    if is_superuser:
        usr.is_superuser = True
    if is_superuser or is_staff:
        usr.is_staff = True
    usr.is_active = True
    usr.save()
    return usr


def get_user_model_labels():
    User = get_user_model()

    user_orm_label = '%s.%s' % (User._meta.app_label, User._meta.object_name)
    user_model_label = '%s.%s' % (User._meta.app_label, User._meta.module_name)
    return user_orm_label, user_model_label
