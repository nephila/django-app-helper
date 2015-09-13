# -*- coding: utf-8 -*-
try:
    import djangocms_text_ckeditor  # NOQA
    text_plugin = ['djangocms_text_ckeditor']
except ImportError:
    text_plugin = []

HELPER_SETTINGS = {
    'TIME_ZONE': 'Europe/Paris',
    'INSTALLED_APPS': [
        'djangocms_admin_style',
    ] + text_plugin,
    'TEMPLATE_CONTEXT_PROCESSORS': [
        'django.core.context_processors.debug'
    ],
    'TEST_RUNNER': 'runners.CapturedOutputRunner',
}
