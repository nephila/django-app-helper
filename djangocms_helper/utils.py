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
from django.utils.datastructures import SortedDict
from django.utils.functional import empty
from django.utils.six import StringIO

DJANGO_1_4 = LooseVersion(django.get_version()) < LooseVersion('1.5')
DJANGO_1_5 = LooseVersion(django.get_version()) < LooseVersion('1.6')
DJANGO_1_6 = LooseVersion(django.get_version()) < LooseVersion('1.7')
DJANGO_1_7 = LooseVersion(django.get_version()) < LooseVersion('1.8')


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
    if args['--cms']:
        CMS_APPS = [
            'mptt',
            'cms',
            'menus',
        ]
        CMS_PROCESSORS = [
            'cms.context_processors.media',
            'sekizai.context_processors.sekizai',
        ]
        URLCONF = 'cms.urls'
    else:
        CMS_APPS = []
        CMS_PROCESSORS = []
        URLCONF = 'djangocms_helper.urls'
    default_settings = {
        'INSTALLED_APPS': [
            'django.contrib.contenttypes',
            'django.contrib.auth',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.admin',
        ] + CMS_APPS + [application],
        'DATABASES': {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        'TEMPLATE_CONTEXT_PROCESSORS': [
            'django.core.context_processors.auth',
            'django.core.context_processors.i18n',
            'django.core.context_processors.request',
            'django.core.context_processors.media',
            'django.core.context_processors.static',
        ] + CMS_PROCESSORS,
        'ROOT_URLCONF': URLCONF,
        'SITE_ID': 1,
        'LANGUAGE_CODE': 'en',
        'LANGUAGES': (('en', 'English'),)
    }

    default_name = ':memory:' if args['test'] else 'local.sqlite'

    db_url = os.environ.get("DATABASE_URL", "sqlite://localhost/%s" % default_name)
    migrate = args.get('--migrate', False)
    configs = {
        'default': dj_database_url.parse(db_url),
        'STATIC_ROOT': STATIC_ROOT,
        'MEDIA_ROOT': MEDIA_ROOT,
        'USE_TZ': True,
        'SOUTH_TESTS_MIGRATE': migrate,
    }
    default_settings.update(configs)
    try:
        extra_settings_file = args.get('--extra-settings')
        if not extra_settings_file:
            extra_settings_file = 'cms_helper.py'
        extra_settings = load_from_file(extra_settings_file).HELPER_SETTINGS
    except (IOError, AttributeError):
        extra_settings = None

    if extra_settings:
        apps = extra_settings.get('INSTALLED_APPS', [])
        template_processors = extra_settings.get('TEMPLATE_CONTEXT_PROCESSORS', [])
        if apps:
            del(extra_settings['INSTALLED_APPS'])
        if template_processors:
            del(extra_settings['TEMPLATE_CONTEXT_PROCESSORS'])
        default_settings.update(extra_settings)
        default_settings['INSTALLED_APPS'].extend(apps)
        default_settings['TEMPLATE_CONTEXT_PROCESSORS'].extend(template_processors)
    if DJANGO_1_6:
        default_settings['INSTALLED_APPS'].append('south')

    if args['test']:
        default_settings['SESSION_ENGINE'] = "django.contrib.sessions.backends.cache"

    _reset_django(settings)
    settings.configure(**default_settings)
    return settings
