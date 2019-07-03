# -*- coding: utf-8 -*-
from tempfile import mkdtemp

try:
    import djangocms_text_ckeditor  # NOQA
    text_plugin = ['djangocms_text_ckeditor']
except ImportError:
    text_plugin = []

HELPER_SETTINGS = {
    'TIME_ZONE': 'Europe/Rome',
    'INSTALLED_APPS': [
        'example2',
        'filer',
    ] + text_plugin,
    'CMS_LANGUAGES': {
        1: [
            {
                'code': 'en',
                'name': 'English',
                'public': True,
            },
            {
                'code': 'it',
                'name': 'Italiano',
                'public': True,
            },
            {
                'code': 'fr',
                'name': 'French',
                'public': True,
            },
        ],
        'default': {
            'hide_untranslated': False,
        },
    },
    'FILE_UPLOAD_TEMP_DIR': mkdtemp(),
}


def run():
    from djangocms_helper import runner
    runner.cms('example1')


def setup():
    import sys
    from djangocms_helper import runner
    runner.setup('example1', sys.modules[__name__], use_cms=True)


def setup_nocms():
    import sys
    from djangocms_helper import runner
    runner.setup('example1', sys.modules[__name__], use_cms=False)


if __name__ == "__main__":
    run()
