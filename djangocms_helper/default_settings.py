# -*- coding: utf-8 -*-


def get_default_settings(CMS_APP, CMS_PROCESSORS, CMS_MIDDLEWARE,
                         CMS_APP_STYLE, URLCONF, application):
    return {
        'INSTALLED_APPS': [
            'django.contrib.contenttypes',
            'django.contrib.auth',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.staticfiles',
        ] + CMS_APP_STYLE + [
            'django.contrib.admin',
            'djangocms_helper.test_data',
        ] + CMS_APP + [application],
        'DATABASES': {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        'TEMPLATE_CONTEXT_PROCESSORS': [
            'django.contrib.auth.context_processors.auth',
            'django.core.context_processors.i18n',
            'django.core.context_processors.request',
            'django.core.context_processors.media',
            'django.core.context_processors.static',
        ] + CMS_PROCESSORS,
        'MIDDLEWARE_CLASSES': [
            'django.middleware.http.ConditionalGetMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.locale.LocaleMiddleware',
            'django.middleware.doc.XViewMiddleware',
            'django.middleware.common.CommonMiddleware',
        ] + CMS_MIDDLEWARE,
        'ROOT_URLCONF': URLCONF,
        'SITE_ID': 1,
        'LANGUAGE_CODE': 'en',
        'LANGUAGES': (('en', 'English'),),
        'STATIC_URL': '/static/',
        'MEDIA_URL': '/media/',
        'DEBUG': True,
        'CMS_TEMPLATES': (
            ('fullwidth.html', 'Fullwidth'),
            ('page.html', 'Normal page'),
        ),

    }
