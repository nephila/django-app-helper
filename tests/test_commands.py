import contextlib
import os
import os.path
import shutil
import sys
import unittest
from copy import copy
from tempfile import mkdtemp
from unittest.mock import patch

import django
from django.test.utils import setup_test_environment, teardown_test_environment

from app_helper import runner
from app_helper.main import _make_settings, core
from app_helper.utils import captured_output, get_user_model, temp_dir, work_in

User = get_user_model()


@contextlib.contextmanager
def wrap_test_environment():
    """
    Create a clean test environment context in which test env can be initialized again.

    Needed by tests in which we run tests in the fake applications invoked by app_helper API.
    """
    try:
        teardown_test_environment()
    except AttributeError:
        pass
    yield
    try:
        setup_test_environment()
    except AttributeError:
        pass


DEFAULT_ARGS = {
    "shell": False,
    "test": False,
    "cms_check": False,
    "compilemessages": False,
    "makemessages": False,
    "makemigrations": False,
    "authors": False,
    "server": False,
    "--xvfb": "",
    "--runner": None,
    "--runner-options": None,
    "--cms": True,
    "--failfast": False,
    "--merge": False,
    "--locale": "",
    "--dry-run": False,
    "--empty": False,
    "--native": False,
    "--persistent": False,
    "--persistent-path": None,
    "--use-daphne": False,
    "--use-channels": False,
    "--bind": "",
    "--port": "",
    "<test-label>": "",
    "<extra-applications>": "",
    "options": "",
    "<command>": "",
}


class CommandTests(unittest.TestCase):
    application = None
    basedir = None
    pofile = None
    mofile = None
    migration_dir = None

    @classmethod
    def setUpClass(cls):
        os.environ.setdefault("DATABASE_URL", "sqlite://localhost/:memory:")
        cls.basedir = os.path.abspath(os.path.join("tests", "test_utils"))
        cls.application = "example1"
        cls.application_2 = "example2"
        with work_in(cls.basedir):
            with captured_output():
                cls.migration_example = os.path.abspath(
                    os.path.join(cls.application, "data", "django_0001_initial.py")
                )
                cls.migration_partial = os.path.abspath(
                    os.path.join(cls.application, "data", "django_0001_partial.py")
                )
                cls.poexample = os.path.abspath(os.path.join(cls.application, "data", "django.po"))
                cls.pofile = os.path.abspath(os.path.join(cls.application, "locale", "en", "LC_MESSAGES", "django.po"))
                cls.mofile = os.path.abspath(os.path.join(cls.application, "locale", "en", "LC_MESSAGES", "django.mo"))
                cls.migration_dir = os.path.abspath(os.path.join(cls.application, "migrations"))
                cls.migration_dir_2 = os.path.abspath(os.path.join(cls.application_2, "migrations"))
                cls.migration_file = os.path.abspath(os.path.join(cls.application, "migrations", "0001_initial.py"))
                cls.migration_file_2 = os.path.abspath(
                    os.path.join(cls.application_2, "migrations", "0001_initial.py")
                )
        try:
            import cms  # noqa: F401
        except ImportError:
            DEFAULT_ARGS["--cms"] = False

    def _clean_modules_directories(self):
        """
        Cleanup all the leftover of migration and po files tests.
        Executed in setup and teardown for simplicity.
        """
        try:
            os.unlink(self.pofile)
        except (OSError, TypeError):
            pass
        try:
            os.unlink(self.mofile)
        except (OSError, TypeError):
            pass
        try:
            if self.migration_dir:
                shutil.rmtree(self.migration_dir)
        except (OSError, TypeError):
            pass
        try:
            if self.migration_dir_2:
                shutil.rmtree(self.migration_dir_2)
        except (OSError, TypeError):
            pass
        try:
            del sys.modules["example1.migrations"]
        except KeyError:
            pass
        try:
            del sys.modules["example2.migrations"]
        except KeyError:
            pass
        try:
            del sys.modules["tests.test_utils.example1.migrations"]
        except KeyError:
            pass
        try:
            del sys.modules["tests.test_utils.example1.migrations.0001_initial"]
        except KeyError:
            pass
        try:
            del sys.modules["tests.test_utils.example2.migrations"]
        except KeyError:
            pass

    def setUp(self):
        self._clean_modules_directories()

    def tearDown(self):
        os.environ["AUTH_USER_MODEL"] = "auth.User"
        self._clean_modules_directories()

    def test_map_argv(self):
        """CLI arguments are mapped to internal options."""
        from app_helper.main import _map_argv

        argv_1 = [
            "helper.py",
            "example1",
            "test",
            "--cms",
            "--persistent-path=test",
            "--extra-settings==something.py",
            "--runner==something.py",
        ]
        target_1 = {
            "--bind": "127.0.0.1",
            "--cms": True,
            "--dry-run": False,
            "--empty": False,
            "--extra-settings": "",
            "--failfast": False,
            "--help": False,
            "--locale": None,
            "--merge": False,
            "--migrate": False,
            "--native": False,
            "--no-migrate": False,
            "--persistent": True,
            "--persistent-path": "test",
            "--port": "8000",
            "--runner": "",
            "--runner-options": None,
            "--verbose": None,
            "--version": False,
            "--xvfb": False,
            "--use-daphne": False,
            "--use-channels": False,
            "<application>": "example1",
            "<command>": None,
            "<extra-applications>": [],
            "<test-label>": [],
            "authors": False,
            "cms_check": False,
            "compilemessages": False,
            "makemessages": False,
            "makemigrations": False,
            "options": [
                "helper.py",
                "test",
                "--cms",
                "--persistent-path=test",
                "--extra-settings==something.py",
                "--runner==something.py",
            ],
            "server": False,
            "setup": False,
            "test": True,
        }
        argv_2 = [
            "helper.py",
            "example1",
            "server",
            "--cms",
            "--persistent-path=test",
            "--extra-settings==something.py",
            "--runner==something.py",
        ]
        target_2 = {
            "--bind": "127.0.0.1",
            "--cms": True,
            "--dry-run": False,
            "--empty": False,
            "--extra-settings": "",
            "--failfast": False,
            "--help": False,
            "--locale": None,
            "--merge": False,
            "--migrate": False,
            "--native": False,
            "--no-migrate": False,
            "--persistent": True,
            "--persistent-path": "test",
            "--port": "8000",
            "--runner": "",
            "--runner-options": None,
            "--verbose": None,
            "--version": False,
            "--xvfb": False,
            "--use-daphne": False,
            "--use-channels": False,
            "<application>": "example1",
            "<command>": None,
            "<extra-applications>": [],
            "<test-label>": [],
            "authors": False,
            "cms_check": False,
            "compilemessages": False,
            "makemessages": False,
            "makemigrations": False,
            "options": [
                "helper.py",
                "server",
                "--cms",
                "--persistent-path=test",
                "--extra-settings==something.py",
                "--runner==something.py",
            ],
            "server": True,
            "setup": False,
            "test": False,
        }

        argv_3 = [
            "helper.py",
            "example1",
            "some_command",
            "--cms",
            "--persistent-path=test",
            "--extra-settings==something.py",
            "--runner==something.py",
        ]
        target_3 = {
            "--bind": "127.0.0.1",
            "--cms": True,
            "--dry-run": False,
            "--empty": False,
            "--extra-settings": "",
            "--failfast": False,
            "--help": False,
            "--locale": None,
            "--merge": False,
            "--migrate": False,
            "--native": False,
            "--no-migrate": False,
            "--persistent": True,
            "--persistent-path": "test",
            "--port": "8000",
            "--runner": "",
            "--runner-options": None,
            "--verbose": None,
            "--version": False,
            "--xvfb": False,
            "--use-daphne": False,
            "--use-channels": False,
            "<application>": "example1",
            "<command>": "some_command",
            "<extra-applications>": [],
            "<test-label>": [],
            "authors": False,
            "cms_check": False,
            "compilemessages": False,
            "makemessages": False,
            "makemigrations": False,
            "options": [
                "helper.py",
                "some_command",
                "--cms",
                "--persistent-path=test",
                "--extra-settings==something.py",
                "--runner==something.py",
            ],
            "server": False,
            "setup": False,
            "test": False,
        }

        application_module = __import__(argv_1[1])
        args = _map_argv(argv_1, application_module)
        self.assertEqual(target_1, args)

        application_module = __import__(argv_2[1])
        args = _map_argv(argv_2, application_module)
        self.assertEqual(target_2, args)

        application_module = __import__(argv_3[1])
        args = _map_argv(argv_3, application_module)
        self.assertEqual(target_3, args)

    def test_extra_settings(self):
        """Settings declared in helper file are merged in default settings."""
        from django.conf import settings

        with work_in(self.basedir):
            with captured_output():
                args = copy(DEFAULT_ARGS)
                with temp_dir() as STATIC_ROOT:  # noqa: N806
                    with temp_dir() as MEDIA_ROOT:  # noqa: N806
                        local_settings = _make_settings(args, self.application, settings, STATIC_ROOT, MEDIA_ROOT)
                        # Testing that helper.py in custom project is loaded
                        self.assertEqual(local_settings.TIME_ZONE, "Europe/Rome")

                        args["--extra-settings"] = "cms_helper_extra.py"
                        local_settings = _make_settings(args, self.application, settings, STATIC_ROOT, MEDIA_ROOT)
                        # Testing that helper.py in the command option is loaded
                        self.assertEqual(local_settings.TIME_ZONE, "Europe/Paris")
                        # Existing application is kept
                        self.assertTrue("app_helper.test_data" in local_settings.INSTALLED_APPS)
                        # New ones are added both on top and in random positions
                        self.assertEqual("djangocms_admin_style", local_settings.INSTALLED_APPS[0])
                        self.assertTrue("some_app" in local_settings.INSTALLED_APPS)

                        self.assertTrue(
                            "django.contrib.sessions.middleware.SessionMiddleware" in local_settings.MIDDLEWARE
                        )
                        self.assertEqual("top_middleware", local_settings.MIDDLEWARE[0])
                        self.assertTrue("some_middleware" in local_settings.MIDDLEWARE)

                        # Check the loaders
                        self.assertTrue(
                            "django.template.loaders.app_directories.Loader"
                            in local_settings.TEMPLATES[0]["OPTIONS"]["loaders"]
                        )
                        # Loaders declared in settings
                        self.assertTrue(
                            "admin_tools.template_loaders.Loader" in local_settings.TEMPLATES[0]["OPTIONS"]["loaders"]
                        )
                        # Existing application is kept
                        self.assertTrue(
                            "django.template.context_processors.request"
                            in local_settings.TEMPLATES[0]["OPTIONS"]["context_processors"]
                        )
                        # New one is added
                        self.assertTrue(
                            "django.template.context_processors.debug"
                            in local_settings.TEMPLATES[0]["OPTIONS"]["context_processors"]
                        )
                        # Check template dirs
                        self.assertTrue("some/dir" in local_settings.TEMPLATES[0]["DIRS"])

    @patch("app_helper.server.autoreload.run_with_reloader")
    def test_server_django(self, run_with_reloader):
        """Run server command and create default user - django version."""
        with work_in(self.basedir):
            User = get_user_model()
            User.objects.all().delete()
            with captured_output() as (out, err):
                args = copy(DEFAULT_ARGS)
                args["server"] = True
                core(args, self.application)
            self.assertTrue("A admin user (username: admin, password: admin) has been created." in out.getvalue())
            self.assertEqual(run_with_reloader.call_args[0][0].__module__, "django.core.management.commands.runserver")
        User.objects.all().delete()

    @patch("app_helper.server.autoreload.run_with_reloader")
    def test_server_channels(self, run_with_reloader):
        """Run server command and create default user - channels version."""
        try:
            import channels  # noqa: F401
        except ImportError:
            raise unittest.SkipTest("channels is not available, skipping test")
        if channels.__version__ > "4.0":
            raise unittest.SkipTest("channels 4 removed support for runserver, use daphne version instead, skipping")
        with work_in(self.basedir):
            with captured_output() as (out, err):
                args = copy(DEFAULT_ARGS)
                args["server"] = True
                args["--use-channels"] = True
                core(args, self.application)
            self.assertTrue("A admin user (username: admin, password: admin) has been created." in out.getvalue())
            self.assertEqual(run_with_reloader.call_args[0][0].__module__, "channels.management.commands.runserver")
        User.objects.all().delete()

    @unittest.skipIf(django.VERSION < (3, 0), "Daphne support requires Django 3.0+")
    @patch("app_helper.server.autoreload.run_with_reloader")
    def test_server_daphne(self, run_with_reloader):
        """Run server command and create default user - daphne version."""
        try:
            import daphne  # noqa: F401
        except ImportError:
            raise unittest.SkipTest("daphne is not available, skipping test")
        with work_in(self.basedir):
            User = get_user_model()
            User.objects.all().delete()
            with captured_output() as (out, err):
                args = copy(DEFAULT_ARGS)
                args["server"] = True
                args["--use-daphne"] = True
                core(args, self.application)
            self.assertTrue("A admin user (username: admin, password: admin) has been created." in out.getvalue())
            self.assertEqual(run_with_reloader.call_args[0][0].__module__, "daphne.cli")
        User.objects.all().delete()

    def test_makemigrations(self):
        """Run makemigrations command."""
        with captured_output() as (out, err):
            args = copy(DEFAULT_ARGS)
            args["makemigrations"] = True
            args["<extra-applications>"] = ["example2"]
            core(args, self.application)
        self.assertTrue(os.path.exists(self.migration_file))
        self.assertTrue(os.path.exists(self.migration_file_2))
        self.assertTrue("Create model ExampleModel1" in out.getvalue())
        self.assertTrue("Create model ExampleModel2" in out.getvalue())

    def test_makemigrations_update(self):
        """Update migrations if code changes."""
        os.makedirs(self.migration_dir)
        open(os.path.join(self.migration_dir, "__init__.py"), "w")
        shutil.copy(self.migration_partial, self.migration_file)
        with captured_output() as (out, err):
            args = copy(DEFAULT_ARGS)
            args["makemigrations"] = True
            core(args, self.application)
        self.assertTrue("Migrations for 'example1':" in out.getvalue())

    def test_makemigrations_empty(self):
        """Create empty migrations with makemigrations --empty."""
        with captured_output() as (out, err):
            os.makedirs(self.migration_dir)
            open(os.path.join(self.migration_dir, "__init__.py"), "w")
            shutil.copy(self.migration_example, self.migration_file)
            args = copy(DEFAULT_ARGS)
            args["makemigrations"] = True
            args["--empty"] = True
            core(args, self.application)
        self.assertTrue("Migrations for 'example1':" in out.getvalue())

    def test_makemigrations_merge(self):
        """Run makemigrations --merge."""
        with captured_output() as (out, err):
            args = copy(DEFAULT_ARGS)
            args["makemigrations"] = True
            args["--merge"] = True
            core(args, self.application)
            self.assertTrue("No conflicts detected to merge" in out.getvalue())

    def test_makemessages(self):
        """Run makemessages command runs."""
        with work_in(self.basedir):
            with captured_output():
                args = copy(DEFAULT_ARGS)
                args["makemessages"] = True
                core(args, self.application)
                self.assertTrue(os.path.exists(self.pofile))

    def test_compilemessages(self):
        """Run compilemessages command."""
        with work_in(self.basedir):
            with captured_output():
                shutil.copy(self.poexample, self.pofile)
                args = copy(DEFAULT_ARGS)
                args["compilemessages"] = True
                core(args, self.application)
                self.assertTrue(os.path.exists(self.mofile))

    def test_cms_check(self):
        """Run cms check command via app-helper."""
        try:
            import cms  # noqa: F401
        except ImportError:
            raise unittest.SkipTest("django CMS not available, skipping test")
        with captured_output() as (out, err):
            shutil.copy(self.poexample, self.pofile)
            args = copy(DEFAULT_ARGS)
            args["cms_check"] = True
            args["--extra-settings"] = "helper.py"
            args["--migrate"] = False
            core(args, self.application)
        self.assertTrue("Installation okay" in out.getvalue())
        self.assertFalse("[WARNING]" in out.getvalue())
        self.assertFalse("[ERROR]" in out.getvalue())

    def test_cms_check_nocms(self):
        """cms check raise exception if cms is not available."""
        try:
            import cms  # noqa: F401

            raise unittest.SkipTest("django CMS available, skipping test")
        except ImportError:
            pass
        with work_in(self.basedir):
            with self.assertRaises(ImportError):
                shutil.copy(self.poexample, self.pofile)
                args = copy(DEFAULT_ARGS)
                args["cms_check"] = True
                args["--extra-settings"] = "helper.py"
                args["--migrate"] = False
                core(args, self.application)

    def test_any_command_check(self):
        """Run any django command via app-helper."""
        with work_in(self.basedir):
            with captured_output() as (out, err):
                args = copy(DEFAULT_ARGS)
                args["<command>"] = "check"
                args["options"] = ["helper", "check", "--extra-settings=cms_helper_extra.py"]
                core(args, self.application)
        self.assertTrue("no issues" in out.getvalue())

    def test_any_command_compilemessages(self):
        """Run compilemessages as plain django command."""
        with work_in(os.path.join(self.basedir, self.application)):
            with captured_output() as (out, err):
                shutil.copy(self.poexample, self.pofile)
                args = copy(DEFAULT_ARGS)
                args["<command>"] = "compilemessages"
                args["options"] = "helper compilemessages --cms -len --verbosity=2".split(" ")
                core(args, self.application)
                self.assertTrue(os.path.exists(self.mofile))

    def test_any_command_migrations(self):
        """Run makemigrations as plain django command."""
        with captured_output() as (out, err):
            args = copy(DEFAULT_ARGS)
            args["<command>"] = "makemigrations"
            args["options"] = "helper makemigrations example2 --verbosity=2".split(" ")
            core(args, self.application)
        self.assertFalse("Create model ExampleModel1" in out.getvalue())
        self.assertFalse(os.path.exists(self.migration_file))
        self.assertTrue("Create model ExampleModel2" in out.getvalue())
        self.assertTrue(os.path.exists(self.migration_file_2))

    def test_testrun(self):
        """Run test via API using custom runner which only picks tests in sample applications."""
        try:
            import cms  # noqa: F401
        except ImportError:
            raise unittest.SkipTest("django CMS not available, skipping test")
        path = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), "data"))
        with wrap_test_environment():
            with captured_output() as (out, err):
                with self.assertRaises(SystemExit) as exit_state:
                    args = copy(DEFAULT_ARGS)
                    args["test"] = True
                    args["<application>"] = "example1"
                    args["--persistent"] = True
                    args["--runner"] = "runners.CapturedOutputRunner"
                    args["<test-label>"] = self.application
                    core(args, self.application)
            self.assertTrue("Ran 14 tests in" in err.getvalue())
            self.assertEqual(exit_state.exception.code, 0)
            self.assertTrue(args["STATIC_ROOT"].startswith(path))
            self.assertTrue(args["MEDIA_ROOT"].startswith(path))
            self.assertTrue(os.path.exists(args["STATIC_ROOT"]))
            self.assertTrue(os.path.exists(args["MEDIA_ROOT"]))

    def test_testrun_runner_options(self):
        """Run test with additional options."""
        try:
            import cms  # noqa: F401
        except ImportError:
            raise unittest.SkipTest("django CMS not available, skipping test")
        with wrap_test_environment():
            with captured_output() as (out, err):
                with self.assertRaises(SystemExit) as exit_state:
                    args = copy(DEFAULT_ARGS)
                    args["test"] = True
                    args["<application>"] = "example1"
                    args["--persistent"] = True
                    args["--runner"] = "runners.CapturedOutputRunner"
                    args["<test-label>"] = self.application
                    args["--runner-options"] = ["--tag=a-tag"]
                    core(args, self.application)
            self.assertTrue("Ran 1 test in" in err.getvalue())
            self.assertEqual(exit_state.exception.code, 0)

    def test_testrun_persistent_path(self):
        """Run test via API using custom runner which only picks tests in sample applications with persistent data."""
        try:
            import cms  # noqa: F401
        except ImportError:
            raise unittest.SkipTest("django CMS not available, skipping test")
        path = mkdtemp()
        with wrap_test_environment():
            with captured_output() as (out, err):
                with self.assertRaises(SystemExit) as exit_state:
                    args = copy(DEFAULT_ARGS)
                    args["test"] = True
                    args["--persistent"] = True
                    args["--persistent-path"] = path
                    args["--runner"] = "runners.CapturedOutputRunner"
                    args["<test-label>"] = self.application
                    core(args, self.application)
            self.assertTrue("Ran 14 tests in" in err.getvalue())
            self.assertEqual(exit_state.exception.code, 0)
            self.assertTrue(args["STATIC_ROOT"].startswith(path))
            self.assertTrue(args["MEDIA_ROOT"].startswith(path))
            self.assertTrue(os.path.exists(args["STATIC_ROOT"]))
            self.assertTrue(os.path.exists(args["MEDIA_ROOT"]))

    def test_runner_wrong(self):
        """Run non existing test labels via runner file using custom runner."""
        try:
            import cms  # noqa: F401
        except ImportError:
            raise unittest.SkipTest("django CMS not available, skipping test")
        if sys.version_info < (3, 5):
            exception = ImportError
        else:
            exception = SystemExit
        with wrap_test_environment():
            with captured_output():
                with self.assertRaises(exception) as exit_state:
                    args = []
                    args.append("helper")
                    args.append("test")
                    args.append("example1")
                    args.append("--runner=runners.CapturedOutputRunner")
                    # passing extra_args is the same as appending to args, except that in real life, args are taken
                    # from sys.argv and extra_args is an argument for developer to use
                    runner.cms("example1", args, extra_args=["whatever"])
        if sys.version_info >= (3, 5):
            self.assertEqual(exit_state.exception.code, 1)

    def test_runner(self):
        """Run tests from helper file."""
        try:
            import cms  # noqa: F401
        except ImportError:
            raise unittest.SkipTest("django CMS not available, skipping test")

        with wrap_test_environment():
            with captured_output() as (out, err):
                with self.assertRaises(SystemExit) as exit_state:
                    args = []
                    args.append("helper")
                    args.append("test")
                    args.append("--extra-settings=helper.py")
                    args.append("example1")
                    runner.cms("example1", args)
            self.assertTrue("visible string" in out.getvalue())
            self.assertFalse("hidden string" in out.getvalue())
            self.assertFalse("hidden string" in err.getvalue())
            self.assertTrue("Ran 14 tests in" in err.getvalue())
            self.assertEqual(exit_state.exception.code, 0)

    def test_runner_compat(self):
        """Run tests from previous helper file default name cms_helper."""
        try:
            import cms  # noqa: F401
        except ImportError:
            raise unittest.SkipTest("django CMS not available, skipping test")

        with wrap_test_environment():
            with captured_output() as (out, err):
                with self.assertRaises(SystemExit) as exit_state:
                    args = []
                    args.append("cms_helper")
                    args.append("test")
                    args.append("example1")
                    runner.cms("example1", args)
        self.assertTrue("visible string" in out.getvalue())
        self.assertFalse("hidden string" in out.getvalue())
        self.assertFalse("hidden string" in err.getvalue())
        self.assertTrue("Ran 14 tests in" in err.getvalue())
        self.assertEqual(exit_state.exception.code, 0)

    def test_runner_cms_exception(self):
        """Raise exception if cms-enabled tests are invoked without django CMS."""
        try:
            import cms  # noqa: F401

            raise unittest.SkipTest("django CMS available, skipping test")
        except ImportError:
            pass
        from tests.test_utils.runners import CapturedOutputRunner

        with patch("django.test.runner.DiscoverRunner", CapturedOutputRunner):
            with work_in(self.basedir):
                with captured_output() as (__a, __b):
                    with self.assertRaises(ImportError):
                        args = []
                        args.append("helper")
                        runner.cms("example1", args)

    def test_runner_cms_argv(self):
        """Arguments are mapped via cms helper."""
        try:
            import cms  # noqa: F401
        except ImportError:
            raise unittest.SkipTest("django CMS not available, skipping test")

        def fake_runner(argv):
            return argv

        from tests.test_utils.runners import CapturedOutputRunner

        with patch("django.test.runner.DiscoverRunner", CapturedOutputRunner):
            with work_in(self.basedir):
                with captured_output() as (out, err):
                    args = []
                    args.append("helper")
                    with patch("app_helper.runner.runner", fake_runner):
                        data = runner.cms("example1", args)
                    self.assertEqual(data, ["helper", "example1", "test", "--cms"])

    def test_runner_argv(self):
        """Arguments are mapped via non-cms helper."""

        def fake_runner(argv):
            return argv

        from tests.test_utils.runners import CapturedOutputRunner

        with patch("django.test.runner.DiscoverRunner", CapturedOutputRunner):
            with work_in(self.basedir):
                with captured_output() as (out, err):
                    args = []
                    args.append("helper")
                    with patch("app_helper.runner.runner", fake_runner):
                        data = runner.run("example1", args)
                    self.assertEqual(data, ["helper", "example1", "test"])

    def test_setup_cms(self):
        """Settings are set from runner setup."""
        try:
            import cms  # noqa: F401
        except ImportError:
            raise unittest.SkipTest("django CMS not available, skipping test")
        with captured_output():
            from tests.test_utils import helper

            settings = runner.setup("example1", helper, use_cms=True, extra_args=["--cms"])
        self.assertTrue("example2" in settings.INSTALLED_APPS)
        self.assertTrue("djangocms_text_ckeditor" in settings.INSTALLED_APPS)
        self.assertTrue("sekizai" in settings.INSTALLED_APPS)
        self.assertTrue("cms" in settings.INSTALLED_APPS)

    def test_setup_custom_user(self):
        """Settings are set by cms runner setup."""
        os.environ["AUTH_USER_MODEL"] = "custom_user.CustomUser"
        try:
            import cms  # noqa: F401
        except ImportError:
            raise unittest.SkipTest("django CMS not available, skipping test")
        with captured_output():
            from tests.test_utils import cms_helper_custom

            settings = runner.setup("example1", cms_helper_custom, use_cms=True, extra_args=["--cms"])
        self.assertTrue("example2" in settings.INSTALLED_APPS)
        self.assertTrue("custom_user" in settings.INSTALLED_APPS)
        self.assertTrue("djangocms_text_ckeditor" in settings.INSTALLED_APPS)
        self.assertTrue("sekizai" in settings.INSTALLED_APPS)
        self.assertTrue("cms" in settings.INSTALLED_APPS)
        del os.environ["AUTH_USER_MODEL"]

    def test_setup_nocms(self):
        """Settings are set by non cms runner setup."""
        with captured_output():
            from tests.test_utils import helper

            settings = runner.setup("example1", helper, extra_args=[])
        self.assertTrue("example2" in settings.INSTALLED_APPS)
        self.assertFalse("sekizai" in settings.INSTALLED_APPS)
        self.assertFalse("cms" in settings.INSTALLED_APPS)

    def test_testrun_nocms(self):
        with wrap_test_environment():
            with work_in(self.basedir):
                with captured_output() as (out, err):
                    with self.assertRaises(SystemExit) as exit_state:
                        args = copy(DEFAULT_ARGS)
                        args["test"] = True
                        args["--cms"] = False
                        args["--runner"] = "runners.CapturedOutputRunner"
                        core(args, self.application)
        self.assertTrue("Ran 14 tests in" in err.getvalue())
        self.assertEqual(exit_state.exception.code, 0)

    def test_runner_nocms(self):
        """Run tests via non cms runner."""
        with wrap_test_environment():
            with work_in(self.basedir):
                with captured_output() as (out, err):
                    with self.assertRaises(SystemExit) as exit_state:
                        args = []
                        args.append("helper")
                        args.append("example1")
                        args.append("test")
                        args.append("--extra-settings=helper.py")
                        runner.run("example1", args, extra_args=["--runner=runners.CapturedOutputRunner"])
        self.assertTrue("Ran 14 tests in" in err.getvalue())
        self.assertEqual(exit_state.exception.code, 0)

    def test_testrun_native(self):
        """Run tests via api with extra settings file."""
        try:
            import cms  # noqa: F401
        except ImportError:
            raise unittest.SkipTest("django CMS not available, skipping test")
        with wrap_test_environment():
            with work_in(self.basedir):
                with captured_output() as (out, err):
                    args = copy(DEFAULT_ARGS)
                    args["<command>"] = None
                    args["test"] = True
                    args["--cms"] = False
                    args["--native"] = True
                    args["--extra-settings"] = "cms_helper_extra_runner.py"
                    try:
                        core(args, self.application)
                    except SystemExit:
                        pass
        self.assertTrue("Ran 14 tests in" in err.getvalue())

    def test_testrun_pytest(self):
        """Run tests via pytest via API."""
        try:
            import cms  # noqa: F401
        except ImportError:
            raise unittest.SkipTest("django CMS not available, skipping test")
        with wrap_test_environment():
            with captured_output() as (out, err):
                args = copy(DEFAULT_ARGS)
                args["<command>"] = None
                args["test"] = True
                args["--cms"] = False
                args["--runner"] = "app_helper.pytest_runner.PytestTestRunner"
                args["--extra-settings"] = "helper_no_cms.py"
                args["--runner-options"] = "'-k test_create_django_image_object'"
                args["options"] = ["helper", "test", "--failfast", "--verbosity=2"]
                try:
                    core(args, self.application)
                except SystemExit:
                    pass
        self.assertTrue("64 items / 63 deselected / 1 selected" in out.getvalue())
        # warnings will depend on django version and adds too much noise
        self.assertTrue("1 passed, 63 deselected" in out.getvalue())

    def test_runner_pytest(self):
        """Run tests via pytest via helper runner."""
        with wrap_test_environment():
            with captured_output() as (out, err):
                with self.assertRaises(SystemExit) as exit_state:
                    args = []
                    args.append("helper_no_cms")
                    args.append("example1")
                    args.append("test")
                    args.append("--extra-settings=helper_no_cms.py")
                    args.append("--runner-options='-k test_create_django_image_object'")
                    args.append("--runner=app_helper.pytest_runner.PytestTestRunner")
                    runner.run("example1", args)
            self.assertTrue("64 items / 63 deselected / 1 selected" in out.getvalue())
            # # warnings will depend on django version and adds too much noise
            self.assertTrue("1 passed, 63 deselected" in out.getvalue())
            self.assertEqual(exit_state.exception.code, 0)

    def test_authors(self):
        """Generate authors file."""
        with work_in(self.basedir):
            with captured_output() as (out, err):
                args = copy(DEFAULT_ARGS)
                args["authors"] = True
                core(args, self.application)
        self.assertTrue("Generating AUTHORS" in out.getvalue())
        self.assertTrue("* Iacopo Spalletti" in out.getvalue())
        self.assertTrue("Authors (" in out.getvalue())

    def test_urls(self):
        """cms urlconf is loaded if django CMS is installed."""
        try:
            import cms  # noqa: F401
        except ImportError:
            raise unittest.SkipTest("django CMS not available, skipping test")
        from django.urls import reverse

        with work_in(self.basedir):
            with captured_output() as (out, err):
                shutil.copy(self.poexample, self.pofile)
                args = copy(DEFAULT_ARGS)
                args["makemessages"] = True
                core(args, self.application)
                self.assertTrue(reverse("pages-root"))

    def test_urls_nocms(self):
        """cms urlconf is not loaded if django CMS is not installed."""
        from django.urls import NoReverseMatch, reverse

        with work_in(self.basedir):
            with captured_output() as (out, err):
                shutil.copy(self.poexample, self.pofile)
                args = copy(DEFAULT_ARGS)
                args["makemessages"] = True
                args["--cms"] = False
                core(args, self.application)
                with self.assertRaises(NoReverseMatch):
                    reverse("pages-root")
