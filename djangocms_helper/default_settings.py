# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals


def get_default_settings(CMS_APP, CMS_PROCESSORS, CMS_MIDDLEWARE,
                         CMS_APP_STYLE, URLCONF, application):
    return dict(
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'django.contrib.auth',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.staticfiles',
        ] + CMS_APP_STYLE + [
            'django.contrib.admin',
            'djangocms_helper.test_data',
            'django.contrib.messages',
        ] + CMS_APP,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        TEMPLATE_LOADERS=[
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ],
        STATICFILES_FINDERS=[
            'django.contrib.staticfiles.finders.FileSystemFinder',
            'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        ],
        TEMPLATE_CONTEXT_PROCESSORS=[
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
            'django.core.context_processors.i18n',
            'django.core.context_processors.csrf',
            'django.core.context_processors.debug',
            'django.core.context_processors.tz',
            'django.core.context_processors.request',
            'django.core.context_processors.media',
            'django.core.context_processors.static',
        ] + CMS_PROCESSORS,
        MIDDLEWARE_CLASSES=[
            'django.middleware.http.ConditionalGetMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.middleware.locale.LocaleMiddleware',
            'django.middleware.common.CommonMiddleware',
        ] + CMS_MIDDLEWARE,
        ROOT_URLCONF=URLCONF,
        SITE_ID=1,
        LANGUAGE_CODE='en',
        LANGUAGES=(('en', 'English'),),
        STATIC_URL='/static/',
        MEDIA_URL='/media/',
        DEBUG=True,
        CMS_TEMPLATES=(
            ('fullwidth.html', 'Fullwidth'),
            ('page.html', 'Normal page'),
        ),
        PASSWORD_HASHERS=(
            'django.contrib.auth.hashers.MD5PasswordHasher',
        ),
        MIGRATION_MODULES={},
        EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
    )


def get_boilerplates_settings():
    return {
        'STATICFILES_FINDERS': [
            'aldryn_boilerplates.staticfile_finders.AppDirectoriesFinder',
        ],
        'TEMPLATE_LOADERS': [
            'aldryn_boilerplates.template_loaders.AppDirectoriesLoader',
        ],
        'TEMPLATE_CONTEXT_PROCESSORS': [
            'aldryn_boilerplates.context_processors.boilerplate',
        ],
        'ALDRYN_BOILERPLATE_NAME': 'bootstrap3',
        'INSTALLED_APPS': [
            'aldryn_boilerplates'
        ]
    }
