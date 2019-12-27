# -*- coding: utf-8 -*-
from tempfile import mkdtemp

HELPER_SETTINGS = {
    "TIME_ZONE": "Europe/Rome",
    "INSTALLED_APPS": ["example2", "filer"],
    "CMS_LANGUAGES": {
        1: [
            {"code": "en", "name": "English", "public": True},
            {"code": "it", "name": "Italiano", "public": True},
            {"code": "fr", "name": "French", "public": True},
        ],
        "default": {"hide_untranslated": False},
    },
    "FILE_UPLOAD_TEMP_DIR": mkdtemp(),
    "TEST_RUNNER": "app_helper.pytest_runner.PytestTestRunner",
    "ALLOWED_HOSTS": ["testserver"]
}


def run():
    from app_helper import runner

    runner.run("example1")


def setup():
    import sys
    from app_helper import runner

    runner.setup("example1", sys.modules[__name__], use_cms=False)
