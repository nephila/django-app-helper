# -*- coding: utf-8 -*-
HELPER_SETTINGS = {
    'TIME_ZONE': 'Europe/Paris',
    'INSTALLED_APPS': [
        'some_app',
    ],
    'TEMPLATE_CONTEXT_PROCESSORS': [
        'django.core.context_processors.debug'
    ],
    'TOP_MIDDLEWARE_CLASSES': [
        'top_middleware',
    ],
    'MIDDLEWARE_CLASSES': [
        'some_middleware',
    ],
    'TOP_INSTALLED_APPS': [
        'djangocms_admin_style'
    ]
}
