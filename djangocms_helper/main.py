#!/usr/bin/env python
from __future__ import print_function, with_statement
import contextlib
import subprocess
import os
import sys
import warnings

from docopt import docopt
from django.utils.encoding import force_text
from django.utils.importlib import import_module


from .utils import work_in, DJANGO_1_6, DJANGO_1_5, temp_dir, _make_settings

__doc__ = '''django CMS applications development helper script.

To use a different database, set the DATABASE_URL environment variable to a
dj-database-url compatible value.

Usage:
    djangocms-helper <application> test [--failfast] [--migrate] [<test-label>...] [--xvfb] [--runner=<test.runner.class>] [--extra-settings=</path/to/settings.py>] [--cms] [--nose-runner] [--simple-runner]
    djangocms-helper <application> shell [--extra-settings=</path/to/settings.py>] [--cms]
    djangocms-helper <application> compilemessages [--extra-settings=</path/to/settings.py>] [--cms]
    djangocms-helper <application> makemessages [--extra-settings=</path/to/settings.py>] [--cms]
    djangocms-helper <application> makemigrations [--extra-settings=</path/to/settings.py>] [--cms]
    djangocms-helper <application> pyflakes [--extra-settings=</path/to/settings.py>] [--cms]
    djangocms-helper <application> authors [--extra-settings=</path/to/settings.py>] [--cms]
    djangocms-helper <application> server [--port=<port>] [--bind=<bind>] [--extra-settings=</path/to/settings.py>] [--cms]

Options:
    -h --help                   Show this screen.
    --version                   Show version.
    --migrate                   Use south migrations in test.
    --cms                       Add support for CMS in the project configuration.
    --failfast                  Stop tests on first failure.
    --nose-runner               Use django-nose as test runner
    --simple-runner             User DjangoTestSuiteRunner
    --xvfb                      Use a virtual X framebuffer for frontend testing, requires xvfbwrapper to be installed.
    --extra-settings=</path/to/settings.py>     Filesystem path to a custom cms_helper file which defines custom settings
    --runner=<test.runner.class>                Dotted path to a custom test runner
    --port=<port>                               Port to listen on [default: 8000].
    --bind=<bind>                               Interface to bind to [default: 127.0.0.1].
'''


def _test_run_worker(test_labels, test_runner, failfast=False):
    warnings.filterwarnings(
        'error', r"DateTimeField received a naive datetime",
        RuntimeWarning, r'django\.db\.models\.fields')
    from django.conf import settings
    from django.test.utils import get_runner

    settings.TEST_RUNNER = test_runner
    TestRunner = get_runner(settings)

    # Monkeypatching sys.argv to avoid passing to nose unwanted arguments
    if test_runner == 'django_nose.NoseTestSuiteRunner':
        sys.argv = sys.argv[:2]
        if failfast:
            sys.argv.append('-x')
    test_runner = TestRunner(verbosity=1, interactive=False, failfast=failfast)
    failures = test_runner.run_tests(test_labels)
    return failures


def test(test_labels, application, failfast=False, test_runner=None):
    """
    Runs the test suite
    :param test_labels: space separated list of test labels
    :param failfast: option to stop the testsuite on the first error
    """
    if not test_labels:
        if os.path.exists('tests'):
            test_labels = ['tests']
        elif os.path.exists(os.path.join(application, 'tests')):
            test_labels = [application]
    return _test_run_worker(test_labels, test_runner, failfast)


def compilemessages(application):
    """
    Compiles locale messages
    """
    from django.core.management import call_command

    with work_in(application):
        call_command('compilemessages', all=True)


def makemessages(application):
    """
    Updates the locale message files
    """
    from django.core.management import call_command

    with work_in(application):
        if DJANGO_1_5:
            call_command('makemessages', locale='en')
        else:
            call_command('makemessages', locale=('en',))


def shell():
    """
    Returns a django shell for the test project
    """
    from django.core.management import call_command

    call_command('shell')


def makemigrations(application):
    """
    Generate migrations (for both south and django 1.7+)
    """
    from django.core.management import call_command
    from .utils import load_from_file

    if DJANGO_1_6:
        try:
            loaded = load_from_file(os.path.join(application, 'migrations',
                                                 '0001_initial.py'))
        except IOError:
            loaded = None
        initial = loaded is None
        call_command('schemamigration',
                     initial=initial,
                     auto=(not initial),
                     *(application,))
    else:
        call_command('makemigrations', *(application,))


def generate_authors():
    """
    Updates the authors list
    """
    print("Generating AUTHORS")

    # Get our list of authors
    print("Collecting author names")
    r = subprocess.Popen(["git", "log", "--use-mailmap", "--format=%aN"],
                         stdout=subprocess.PIPE)
    seen_authors = []
    authors = []
    for authfile in ('AUTHORS', 'AUTHORS.rst'):
        if os.path.exists(authfile):
            break
    with open(authfile, 'r') as f:
        for line in f.readlines():
            if line.startswith("*"):
                author = force_text(line).strip("* \n")
                if author.lower() not in seen_authors:
                    seen_authors.append(author.lower())
                    authors.append(author)
    for author in r.stdout.readlines():
        author = force_text(author).strip()
        if author.lower() not in seen_authors:
            seen_authors.append(author.lower())
            authors.append(author)

    # Sort our list of Authors by their case insensitive name
    authors = sorted(authors, key=lambda x: x.lower())

    # Write our authors to the AUTHORS file
    print(u"Authors (%s):\n\n\n* %s" % (len(authors), u"\n* ".join(authors)))


def static_analisys(application):
    """
    Performs a pyflakes static analysis with the same configuration as
    django CMS testsuite
    """
    try:
        from cms.test_utils.util.static_analysis import pyflakes
        application_module = import_module(application)
        assert pyflakes((application_module,)) == 0
    except ImportError:
        print(u"Static analisys available only if django CMS is installed")


def server(bind='127.0.0.1', port=8000, migrate_cmd=False):
    from cms.utils.compat.dj import get_user_model
    from django.core.management import call_command
    from django.utils import autoreload

    if os.environ.get("RUN_MAIN") != "true":
        if DJANGO_1_6:
            if migrate_cmd:
                call_command("syncdb", interactive=False, verbosity=1, database='default')
                call_command("migrate", interactive=False, verbosity=1, database='default')
            else:
                call_command("syncdb", interactive=False, verbosity=1, database='default', migrate=False, migrate_all=True)
                call_command("migrate", interactive=False, verbosity=1, database='default', fake=True)
        else:
            call_command("migrate", database='default')
        User = get_user_model()
        if not User.objects.filter(is_superuser=True).exists():
            usr = User()

            if(User.USERNAME_FIELD != 'email'):
                setattr(usr, User.USERNAME_FIELD, 'admin')

            usr.email = 'admin@admin.com'
            usr.set_password('admin')
            usr.is_superuser = True
            usr.is_staff = True
            usr.is_active = True
            usr.save()
            print('')
            print("A admin user (username: admin, password: admin) has been created.")
            print('')
    from django.contrib.staticfiles.management.commands import runserver
    rs = runserver.Command()
    rs.stdout = sys.stdout
    rs.stderr = sys.stderr
    rs.use_ipv6 = False
    rs._raw_ipv6 = False
    rs.addr = bind
    rs.port = port
    autoreload.main(rs.inner_run, (), {
        'addrport': '%s:%s' % (bind, port),
        'insecure_serving': True,
        'use_threading': True
    })


def core(args, application):
    from django.conf import settings

    # configure django
    warnings.filterwarnings(
        'error', r"DateTimeField received a naive datetime",
        RuntimeWarning, r'django\.db\.models\.fields')

    with temp_dir() as STATIC_ROOT:
        with temp_dir() as MEDIA_ROOT:

            _make_settings(args, application, settings, STATIC_ROOT, MEDIA_ROOT)

            # run
            if args['test']:
                if args['--nose-runner']:
                    runner = 'django_nose.NoseTestSuiteRunner'
                elif args['--simple-runner']:
                    runner = 'django.test.simple.DjangoTestSuiteRunner'
                elif args['--runner']:
                    runner = args['--runner']
                else:
                    runner = 'django.test.runner.DiscoverRunner'
                # make "Address already in use" errors less likely, see Django
                # docs for more details on this env variable.
                os.environ.setdefault(
                    'DJANGO_LIVE_TEST_SERVER_ADDRESS',
                    'localhost:8000-9000'
                )
                if args['--xvfb']:  # pragma: no cover
                    import xvfbwrapper

                    context = xvfbwrapper.Xvfb(width=1280, height=720)
                else:
                    @contextlib.contextmanager
                    def null_context():
                        yield

                    context = null_context()

                with context:
                    num_failures = test(args['<test-label>'], application,
                                        args['--failfast'], runner)
                    sys.exit(num_failures)
            elif args['server']:
                server(args['--bind'], args['--port'], args.get('--migrate', True))
            elif args['shell']:
                shell()
            elif args['compilemessages']:
                compilemessages(application)
            elif args['makemessages']:
                makemessages(application)
            elif args['makemigrations']:
                makemigrations(application)
            elif args['pyflakes']:
                return static_analisys(application)
            elif args['authors']:
                return generate_authors()


def main():  # pragma: no cover
    # Command is executed in the main directory of the plugin, and we must
    # include it in the current path for the imports to work
    sys.path.insert(0, '.')

    application = sys.argv[1]
    application_module = import_module(application)
    args = docopt(__doc__, version=application_module.__version__)
    core(args=args, application=application)
