###########################
django CMS Helper reference
###########################

==============
Extra settings
==============

django CMS Helper provide a basic set of settings, you'll probably need to provide your own.

Extra settings can be provided by creating a ``cms_helper.py`` file in the application root
directory and providing the settings as a dictionary named ``HELPER_SETTINGS``::

    HELPER_SETTINGS={
        'INSTALLED_APPS': [
            'any_django_app',
        ],
        'ANY_SETTING: False,
        ...
    }

The settings provided are then merged with the default ones (user-provided ones overrides
the default, except ``INSTALLED_APPS``, ``TEMPLATE_CONTEXT_PROCESSORS`` and ``MIDDLEWARE_CLASSES``
which are appended to the default ones.

================
default settings
================

These are the applications, context processors and middlewares loaded by default

Applications::

    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'djangocms_helper.test_data',  # this provides basic templates and urlconf
    'django.contrib.messages',

Template context processors::

    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.i18n',
    'django.core.context_processors.csrf',
    'django.core.context_processors.debug',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',

Middlewares::

    'django.middleware.http.ConditionalGetMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.middleware.common.CommonMiddleware',


.. _cms_option:

==========
cms option
==========

When using ``--cms`` option, ``INSTALLED_APPS``, ``TEMPLATE_CONTEXT_PROCESSORS`` and
``MIDDLEWARE_CLASSES`` related to django CMS are added to the default settings so you
won't need to provide it yourself.

Applications::

    'djangocms_admin_style',
    'mptt',
    'cms',
    'menus',
    'sekizai',

Template context processors::

    'cms.context_processors.cms_settings',
    'sekizai.context_processors.sekizai',
    'django.contrib.messages.context_processors.messages',


Middlewares::

    'cms.middleware.language.LanguageCookieMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',