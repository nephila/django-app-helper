#######################################
Project settings with Django App Helper
#######################################

.. _extra-settings:

******************
Extra settings
******************

Django App Helper provide a basic set of settings, you'll probably need to provide your own.

Extra settings can be provided by creating a ``helper.py`` file in the application root
directory and providing the settings as a dictionary named ``HELPER_SETTINGS``::

    HELPER_SETTINGS={
        'INSTALLED_APPS': [
            'any_django_app',
        ],
        'ANY_SETTING: False,
        ...
    }

An alternative, and possibly clearer form is::

    HELPER_SETTINGS=dict(
        INSTALLED_APPS=[
            'any_django_app',
        ],
        ANY_SETTING=False,
        ...
    )

By default any setting option provided in ``helper.py`` will override the default ones.

.. warning:: On Django 4.2 and up you **cannot** use ``DEFAULT_FILE_STORAGE`` and ``STATICFILES_STORAGE``
             in ``HELPER_SETTINGS``: use new ``STORAGES`` setting instead.


Special settings
================

The following settings will not override the defaults ones, but they are appended to the defaults
to make easier to customise the configuration:

* ``INSTALLED_APPS``
* ``TEMPLATE_CONTEXT_PROCESSORS``
* ``TEMPLATE_LOADERS``
* ``TEMPLATE_DIRS``
* ``MIDDLEWARE_CLASSES``

Other extra setting:

* ``TOP_INSTALLED_APPS``: items in this setting will be inserted on top of ``INSTALLED_APPS``
  (e.g.: to control the templates and static files override from standard applications
  configured by django-app-helper).

* ``TOP_MIDDLEWARE_CLASSES``: items in this setting will be inserted on top of
  ``MIDDLEWARE_CLASSES``.

Django 1.8 support
==================

All ``TEMPLATES_`` settings from Django 1.6/1.7 are automatically translated to Django 1.8
``TEMPLATE`` setting. To support both, just use the **old** names, and ``django-app-helper``
will take care of converting.

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
    'app_helper.test_data',  # this provides basic templates and urlconf
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


.. note:: On Django 1.8 these are translated to the new path ``django.template.context_processors.*``


Middlewares::

    'django.middleware.http.ConditionalGetMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',


.. _cms-option:

******************
--cms option
******************

When using ``--cms`` option, ``INSTALLED_APPS``, ``TEMPLATE_CONTEXT_PROCESSORS`` and
``MIDDLEWARE_CLASSES`` related to django CMS are added to the default settings so you
won't need to provide it yourself.

Applications::

    'djangocms_admin_style',
    'mptt',
    'cms',
    'menus',
    'sekizai',

When django CMS 3.1+ is used, ``treebeard`` is configured instead of ``mptt``.

Template context processors::

    'cms.context_processors.cms_settings',
    'sekizai.context_processors.sekizai',


Middlewares::

    'cms.middleware.language.LanguageCookieMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',

``django-app-helper`` discovers automtically the South / Django migrations layout and configure
the settings accordingly. As of the current version ``filer``, ``djangocms_text_ckeditor``,
``cmplugin_filer`` are supported.


.. _compatibility mixin: https://docs.djangoproject.com/en/1.10/topics/http/middleware/#upgrading-middleware
