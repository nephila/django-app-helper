# -*- coding: utf-8 -*-
try:
    import djangocms_text_ckeditor  # NOQA
    text_plugin = ['djangocms_text_ckeditor']
except ImportError:
    text_plugin = []

HELPER_SETTINGS = {
    'TIME_ZONE': 'Europe/Rome',
    'INSTALLED_APPS': [
        'example2'
    ] + text_plugin,
}
