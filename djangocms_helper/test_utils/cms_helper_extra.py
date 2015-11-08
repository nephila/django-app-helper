# -*- coding: utf-8 -*-
try:
    import djangocms_text_ckeditor  # NOQA
    text_plugin = ['djangocms_text_ckeditor']
except ImportError:
    text_plugin = []

HELPER_SETTINGS = {
    'TIME_ZONE': 'Europe/Paris',
    'INSTALLED_APPS': [
        'some_app',
    ] + text_plugin,
    'TEMPLATE_CONTEXT_PROCESSORS': [
        'django.core.context_processors.debug'
    ],
    'TEMPLATE_LOADERS': [
        'admin_tools.template_loaders.Loader',
    ],
    'TOP_MIDDLEWARE_CLASSES': [
        'top_middleware',
    ],
    'MIDDLEWARE_CLASSES': [
        'some_middleware',
    ],
    'TOP_INSTALLED_APPS': [
        'djangocms_admin_style'
    ],
    'ALDRYN_BOILERPLATE_NAME': 'legacy',
    'TEMPLATE_DIRS': [
        'some/dir'
    ],
}
