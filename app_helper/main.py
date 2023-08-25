#!/usr/bin/env python
import argparse
import contextlib
import os
import subprocess
import sys
import warnings

from django.utils.encoding import force_str
from docopt import DocoptExit, docopt

from . import __version__
from .utils import _create_db, _make_settings, ensure_unicoded_and_unique, persistent_dir, temp_dir, work_in

__doc__ = """django CMS applications development helper script.

To use a different database, set the DATABASE_URL environment variable to a
dj-database-url compatible value.

Usage:
    django-app-helper <application> test [--failfast] [--migrate] [--no-migrate] [<test-label>...] [--xvfb] [--runner=<test.runner.class>] [--extra-settings=</path/to/settings.py>] [--cms] [--runner-options=<option1>,<option2>] [--native] [--persistent] [--persistent-path=<path>] [--verbose=<level>]
    django-app-helper <application> cms_check [--extra-settings=</path/to/settings.py>] [--cms] [--migrate] [--no-migrate]
    django-app-helper <application> compilemessages [--extra-settings=</path/to/settings.py>] [--cms]
    django-app-helper <application> makemessages [--extra-settings=</path/to/settings.py>] [--cms] [--locale=locale]
    django-app-helper <application> makemigrations [--extra-settings=</path/to/settings.py>] [--cms] [--merge] [--empty] [--dry-run] [<extra-applications>...]
    django-app-helper <application> authors [--extra-settings=</path/to/settings.py>] [--cms]
    django-app-helper <application> server [--port=<port>] [--bind=<bind>] [--extra-settings=</path/to/settings.py>] [--cms] [--migrate] [--no-migrate] [--persistent | --persistent-path=<path>] [--verbose=<level>] [--use-daphne] [--use-channels]
    django-app-helper <application> setup [--extra-settings=</path/to/settings.py>] [--cms]
    django-app-helper <application> <command> [options] [--extra-settings=</path/to/settings.py>] [--cms] [--persistent] [--persistent-path=<path>] [--migrate] [--no-migrate]

Options:
    -h --help                   Show this screen.
    --version                   Show version.
    --migrate                   Use migrations.
    --no-migrate                Skip south migrations.
    --cms                       Add support for CMS in the project configuration.
    --merge                     Merge migrations
    --failfast                  Stop tests on first failure.
    --native                    Use the native test command, instead of the django-app-helper on
    --persistent                Use persistent storage
    --persistent-path=<path>    Persistent storage path
    --locale=locale,-l=locale   Update messgaes for given locale
    --xvfb                      Use a virtual X framebuffer for frontend testing, requires xvfbwrapper to be installed.
    --extra-settings=</path/to/settings.py>     Filesystem path to a custom app_helper file which defines custom settings
    --runner=<test.runner.class>                Dotted path to a custom test runner
    --runner-options=<option1>,<option2>        Comma separated list of command line options for the test runner
    --port=<port>                               Port to listen on [default: 8000].
    --bind=<bind>                               Interface to bind to [default: 127.0.0.1].
    --use-channels                              Run the channels runserver instead of the Django one
    --use-daphne                                Run the Daphne runserver instead of the Django one
    <extra-applications>                        Comma separated list of applications to create migrations for
"""  # NOQA # nopyflakes


def _parse_runner_options(test_runner_class, options):
    if hasattr(test_runner_class, "add_arguments"):
        parser = argparse.ArgumentParser()
        test_runner_class.add_arguments(parser)
        args = parser.parse_args(options)
        return vars(args)
    return {}  # pragma: no cover


def _test_run_worker(test_labels, test_runner, failfast=False, runner_options=None, verbose=1):
    warnings.filterwarnings(
        "error",
        r"DateTimeField received a naive datetime",
        RuntimeWarning,
        r"django\.db\.models\.fields",
    )
    from django.conf import settings
    from django.test.utils import get_runner

    try:
        verbose = int(verbose)
    except (ValueError, TypeError):
        verbose = 1
    runner_options = runner_options or []
    settings.TEST_RUNNER = test_runner
    TestRunner = get_runner(settings)  # NOQA

    kwargs = {"verbosity": verbose, "interactive": False, "failfast": failfast}
    if runner_options:
        if "PytestTestRunner" in test_runner:
            kwargs["pytest_args"] = runner_options
        else:
            if not isinstance(runner_options, list):
                runner_options = runner_options.split(" ")
            extra = _parse_runner_options(TestRunner, runner_options)
            extra.update(kwargs)
            kwargs = extra
    test_runner = TestRunner(**kwargs)
    failures = test_runner.run_tests(test_labels)
    return failures


def test(test_labels, application, failfast=False, test_runner=None, runner_options=None, verbose=1):
    """
    Runs the test suite
    :param test_labels: space separated list of test labels
    :param failfast: option to stop the testsuite on the first error
    """
    if not test_labels and "PytestTestRunner" not in test_runner:
        if os.path.exists("tests"):  # pragma: no cover
            test_labels = ["tests"]
        elif os.path.exists(os.path.join(application, "tests")):
            test_labels = ["%s.tests" % application]
    elif isinstance(test_labels, str):  # pragma: no cover
        test_labels = [test_labels]
    runner_options = runner_options or []
    return _test_run_worker(test_labels, test_runner, failfast, runner_options, verbose)


def compilemessages(application):
    """
    Compiles locale messages
    """
    from django.core.management import call_command

    with work_in(application):
        call_command("compilemessages")


def makemessages(application, locale):
    """
    Updates the locale message files
    """
    from django.core.management import call_command

    if not locale:
        locale = "en"
    with work_in(application):
        call_command("makemessages", locale=(locale,))


def cms_check(migrate_cmd=False):
    """
    Runs the django CMS ``cms check`` command
    """
    from django.core.management import call_command

    try:
        import cms  # NOQA # nopyflakes

        _create_db(migrate_cmd)
        call_command("cms", "check")
    except ImportError:  # pragma: no cover
        print("cms_check available only if django CMS is installed")


def makemigrations(application, merge=False, dry_run=False, empty=False, extra_applications=None):
    """
    Generate migrations
    """
    from django.core.management import call_command

    apps = [application]
    if extra_applications:
        if isinstance(extra_applications, str):  # pragma: no cover
            apps += [extra_applications]
        elif isinstance(extra_applications, list):
            apps += extra_applications

    for app in apps:
        call_command("makemigrations", *(app,), merge=merge, dry_run=dry_run, empty=empty)


def generate_authors():
    """
    Updates the authors list
    """
    print("Generating AUTHORS")

    # Get our list of authors
    print("Collecting author names")
    r = subprocess.Popen(["git", "log", "--use-mailmap", "--format=%aN"], stdout=subprocess.PIPE)
    seen_authors = []
    authors = []
    for authfile in ("AUTHORS", "AUTHORS.rst"):
        if os.path.exists(authfile):
            break
    with open(authfile) as f:
        for line in f.readlines():
            if line.startswith("*"):
                author = force_str(line).strip("* \n")
                if author.lower() not in seen_authors:
                    seen_authors.append(author.lower())
                    authors.append(author)
    for author in r.stdout.readlines():
        author = force_str(author).strip()
        if author.lower() not in seen_authors:
            seen_authors.append(author.lower())
            authors.append(author)

    # Sort our list of Authors by their case insensitive name
    authors = sorted(authors, key=lambda x: x.lower())

    # Write our authors to the AUTHORS file
    print("Authors ({}):\n\n\n* {}".format(len(authors), "\n* ".join(authors)))


def server(
    settings, bind="127.0.0.1", port=8000, migrate_cmd=False, verbose=1, use_channels=False, use_daphne=False
):  # pragma: no cover
    from .server import run

    run(settings, bind, port, migrate_cmd, verbose, use_channels, use_daphne)


def setup_env(settings):
    return settings


def _map_argv(argv, application_module):
    try:
        # by default docopt uses sys.argv[1:]; ensure correct args passed
        args = docopt(__doc__, argv=argv[1:], version=application_module.__version__)
        if argv[2] == "help":
            raise DocoptExit()
    except DocoptExit:
        if argv[2] == "help":
            raise
        args = docopt(__doc__, argv[1:3], version=application_module.__version__)
    args["--cms"] = "--cms" in argv
    args["--persistent"] = "--persistent" in argv
    for arg in argv:
        if arg.startswith("--extra-settings="):
            args["--extra-settings"] = arg.split("=")[1]
        if arg.startswith("--runner="):
            args["--runner"] = arg.split("=")[1]
        if arg.startswith("--persistent-path="):
            args["--persistent-path"] = arg.split("=")[1]
            args["--persistent"] = True
    args["options"] = [argv[0]] + argv[2:]
    if args["test"] and "--native" in args["options"]:
        args["test"] = False
        args["<command>"] = "test"
        args["options"].remove("--native")
    return args


def core(args, application):
    from django.conf import settings

    # configure django
    warnings.filterwarnings(
        "error",
        r"DateTimeField received a naive datetime",
        RuntimeWarning,
        r"django\.db\.models\.fields",
    )
    if args["--persistent"]:
        create_dir = persistent_dir
        if args["--persistent-path"]:
            parent_path = args["--persistent-path"]
        else:
            parent_path = "data"
    else:
        create_dir = temp_dir
        parent_path = "/dev/shm"

    with create_dir("static", parent_path) as STATIC_ROOT:  # NOQA
        with create_dir("media", parent_path) as MEDIA_ROOT:  # NOQA
            args["MEDIA_ROOT"] = MEDIA_ROOT
            args["STATIC_ROOT"] = STATIC_ROOT
            if args["cms_check"]:
                args["--cms"] = True

            if args["<command>"]:
                from django.core.management import execute_from_command_line

                options = [
                    option
                    for option in args["options"]
                    if (
                        option != "--cms"
                        and "--extra-settings" not in option
                        and not option.startswith("--persistent")
                    )
                ]
                _make_settings(args, application, settings, STATIC_ROOT, MEDIA_ROOT)
                execute_from_command_line(options)

            else:
                _make_settings(args, application, settings, STATIC_ROOT, MEDIA_ROOT)
                # run
                if args["test"]:
                    if args["--runner"]:
                        runner = args["--runner"]
                    else:
                        runner = settings.TEST_RUNNER

                    # make "Address already in use" errors less likely, see Django
                    # docs for more details on this env variable.
                    os.environ.setdefault("DJANGO_LIVE_TEST_SERVER_ADDRESS", "localhost:8000-9000")
                    if args["--xvfb"]:  # pragma: no cover
                        import xvfbwrapper

                        context = xvfbwrapper.Xvfb(width=1280, height=720)
                    else:

                        @contextlib.contextmanager
                        def null_context():
                            yield

                        context = null_context()

                    with context:
                        num_failures = test(
                            args["<test-label>"],
                            application,
                            args["--failfast"],
                            runner,
                            args["--runner-options"],
                            args.get("--verbose", 1),
                        )
                        sys.exit(num_failures)
                elif args["server"]:
                    server(
                        settings,
                        args["--bind"],
                        args["--port"],
                        args.get("--migrate", True),
                        args.get("--verbose", 1),
                        args.get("--use-channels", False),
                        args.get("--use-daphne", False),
                    )
                elif args["cms_check"]:
                    cms_check(args.get("--migrate", True))
                elif args["compilemessages"]:
                    compilemessages(application)
                elif args["makemessages"]:
                    makemessages(application, locale=args["--locale"])
                elif args["makemigrations"]:
                    makemigrations(
                        application,
                        merge=args["--merge"],
                        dry_run=args["--dry-run"],
                        empty=args["--empty"],
                        extra_applications=args["<extra-applications>"],
                    )
                elif args["authors"]:
                    return generate_authors()
                elif args["setup"]:
                    return setup_env(settings)


def main(argv=sys.argv):  # pragma: no cover
    # Command is executed in the main directory of the plugin, and we must
    # include it in the current path for the imports to work
    sys.path.insert(0, ".")
    if len(argv) > 1:
        application = argv[1]
        # ensure that argv, are unique and the same type as doc string
        argv = ensure_unicoded_and_unique(argv, application)
        application_module = __import__(application)
        args = _map_argv(argv, application_module)
        return core(args=args, application=application)
    else:
        args = docopt(__doc__, version=__version__)
