import inspect
import os.path
import sys


def run(app, argv=sys.argv, extra_args=None):
    """
    Run commands in a plain django environment

    :param app: application
    :param argv: arguments (default to sys.argv)
    :param extra_args: list of extra arguments
    """
    if app not in argv[:2]:
        # app is automatically added if not present
        argv.insert(1, app)
    if len(argv) < 3 and "test" not in argv[:2]:
        # test argument is given if not argument is passed
        argv.insert(2, "test")
    if extra_args:
        argv.extend(extra_args)
    return runner(argv)


def cms(app, argv=sys.argv, extra_args=None):
    """
    Run commands in a django cMS environment

    :param app: application
    :param argv: arguments (default to sys.argv)
    :param extra_args: list of extra arguments
    """
    try:
        import cms  # NOQA  # nopyflakes
    except ImportError:
        print("runner.cms is available only if django CMS is installed")
        raise
    if app not in argv[:2]:
        # app is automatically added if not present
        argv.insert(1, app)
    if len(argv) < 3 and "test" not in argv[:2]:
        # test argument is given if not argument is passed
        argv.insert(2, "test")
    if "--cms" not in argv:
        # this is the cms runner, just add the cms argument
        argv.append("--cms")
    if extra_args:
        argv.extend(extra_args)
    return runner(argv)


def setup(app, helper_module, extra_args=None, use_cms=False):
    """
    Setup the Django / django CMS environment and return the environment settings.

    :param app: application
    :param helper_module: helper module
    :param extra_args: list of extra arguments
    :param use_cms: setup a django CMS environemtn
    :return: Django settings module
    """

    def _pytest_setup(settings, module):
        excluded_settings = {
            "PASSWORD_RESET_TIMEOUT": "PASSWORD_RESET_TIMEOUT_DAYS",
            "DEFAULT_FILE_STORAGE": "STORAGES",
            "STATICFILES_STORAGE": "STORAGES",
        }
        default_settings = {"SECRET_KEY": "secret"}
        for setting in dir(settings):
            if setting.isupper():
                setting_value = getattr(settings, setting)

                # Empty settings value in the original value which must have a default are checked on
                # default_settings dictionary and default is set, if available
                default_value = default_settings.get(setting, None)
                if default_value and not setting_value:
                    setting_value = default_value

                # If two settings exclude each other, we check if the alternate setting is already defined
                # in the settings module and if not, we set the current setting
                alternate_setting = excluded_settings.get(setting, None)
                alternate_setting_value = None
                if alternate_setting:
                    alternate_setting_value = getattr(settings, alternate_setting, None)
                if not alternate_setting_value:
                    setattr(module, setting, setting_value)

    helper = helper_module.__file__
    argv = [os.path.basename(helper), app, "setup", "--extra-settings={}".format(helper)]
    if use_cms:
        argv.append("--cms")
    if extra_args:
        argv.extend(extra_args)
    settings = runner(argv)
    if "pytest_django" in sys.modules:
        _pytest_setup(settings, helper_module)
    return settings


def runner(argv):
    from . import HELPER_FILE
    from .main import main

    # This is a hackish way to get the caller file which is the file
    # which contains the HELPER_SETTINGS
    helper = os.path.abspath(inspect.getframeinfo(inspect.stack()[2][0]).filename)
    # check if extra settings has been passed
    # if not, user the helper file
    extra_settings = any(x.startswith("--extra-settings=") for x in argv)
    if os.path.basename(helper) not in (HELPER_FILE,) and not extra_settings:
        argv.append("--extra-settings=%s" % helper)
    return main(argv)
