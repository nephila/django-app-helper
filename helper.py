#!/usr/bin/env python

import sys


def gettext(s):
    return s


HELPER_SETTINGS = dict(
    INSTALLED_APPS=[
        "tests.test_utils",
        "tests.test_utils.example1",
        "tests.test_utils.example2",
        "filer",
        "easy_thumbnails",
    ],
    LANGUAGE_CODE="en",
)
try:
    import cms  # noqa: F401

    HELPER_SETTINGS["INSTALLED_APPS"].append("djangocms_text_ckeditor")
except ImportError:
    pass


def run():
    from app_helper import runner

    try:
        import cms  # noqa: F401 F811

        runner.cms("app_helper")
    except ImportError:
        runner.run("app_helper")


def setup():
    from app_helper import runner

    try:
        import cms  # noqa: F401 F811

        use_cms = True
    except ImportError:
        use_cms = False
    runner.setup("app_helper", sys.modules[__name__], use_cms=use_cms)


if __name__ == "__main__":
    run()

if __name__ == "helper":
    # this is needed to run cms_helper in pycharm
    setup()
