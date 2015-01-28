#!/usr/bin/env python
from __future__ import print_function, with_statement
import contextlib
import os
import subprocess
import sys
import warnings

from docopt import docopt, DocoptExit
from django.utils.encoding import force_text
from django.utils.importlib import import_module

from . import __version__
from .utils import (work_in, DJANGO_1_6, DJANGO_1_5, temp_dir, _make_settings,
                    create_user, _create_db, get_user_model)

__doc__ = '''django CMS applications development helper script.

To use a different database, set the DATABASE_URL environment variable to a
dj-database-url compatible value.

Usage:
    djangocms-helper <application> test [--failfast] [--migrate] [<test-label>...] [--xvfb] [--runner=<test.runner.class>] [--extra-settings=</path/to/settings.py>] [--cms] [--nose-runner] [--simple-runner] [--runner-options=<option1>,<option2>]
    djangocms-helper <application> cms_check [--extra-settings=</path/to/settings.py>] [--migrate]
    djangocms-helper <application> compilemessages [--extra-settings=</path/to/settings.py>] [--cms]
    djangocms-helper <application> makemessages [--extra-settings=</path/to/settings.py>] [--cms]
    djangocms-helper <application> makemigrations [--extra-settings=</path/to/settings.py>] [--cms] [--merge] [--empty] [--dry-run] [<extra-applications>...]
    djangocms-helper <application> pyflakes [--extra-settings=</path/to/settings.py>] [--cms]
    djangocms-helper <application> authors [--extra-settings=</path/to/settings.py>] [--cms]
    djangocms-helper <application> server [--port=<port>] [--bind=<bind>] [--extra-settings=</path/to/settings.py>] [--cms] [--migrate]
    djangocms-helper <application> <command> [options] [--extra-settings=</path/to/settings.py>] [--cms]

Options:
    -h --help                   Show this screen.
    --version                   Show version.
    --migrate                   Use south migrations in test.
    --cms                       Add support for CMS in the project configuration.
    --merge                     Merge migrations
    --failfast                  Stop tests on first failure.
    --nose-runner               Use django-nose as test runner
    --simple-runner             User DjangoTestSuiteRunner
    --xvfb                      Use a virtual X framebuffer for frontend testing, requires xvfbwrapper to be installed.
    --extra-settings=</path/to/settings.py>     Filesystem path to a custom cms_helper file which defines custom settings
    --runner=<test.runner.class>                Dotted path to a custom test runner
    --runner-options=<option1>,<option2>        Comma separated list of command line options for the test runner
    --port=<port>                               Port to listen on [default: 8000].
    --bind=<bind>                               Interface to bind to [default: 127.0.0.1].
    <extra-applications>                        Comma separated list of applications to create migrations for
'''


def _test_run_worker(test_labels, test_runner, failfast=False, runner_options=[]):
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
    if runner_options:
        sys.argv.extend(runner_options.split(','))
    test_runner = TestRunner(verbosity=1, interactive=False, failfast=failfast)
    failures = test_runner.run_tests(test_labels)
    return failures


def test(test_labels, application, failfast=False, test_runner=None,
         runner_options=[]):
    """
    Runs the test suite
    :param test_labels: space separated list of test labels
    :param failfast: option to stop the testsuite on the first error
    """
    if not test_labels:
        if os.path.exists('tests'):
            test_labels = ['tests']
        elif os.path.exists(os.path.join(application, 'tests')):
            if 'DjangoTestSuiteRunner' in test_runner:
                test_labels = [application]
            else:
                test_labels = ['%s.tests' % application]
    return _test_run_worker(test_labels, test_runner, failfast, runner_options)


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


def cms_check(migrate_cmd=False):
    """
    Runs the django CMS ``cms check`` command
    """
    from django.core.management import call_command
    try:
        import cms  # nopyflakes
        _create_db(migrate_cmd)
        call_command('cms', 'check')
    except ImportError:
        print(u"cms_check available only if django CMS is installed")


def makemigrations(application, merge=False, dry_run=False, empty=False, extra_applications=None):
    """
    Generate migrations (for both south and django 1.7+)
    """
    from django.core.exceptions import DjangoRuntimeWarning, ImproperlyConfigured
    from django.core.management import call_command

    apps = [application]
    if extra_applications:
        apps += extra_applications

    if DJANGO_1_6:
        from south.exceptions import NoMigrations
        from south.migration import Migrations

        if merge:
            raise DjangoRuntimeWarning(u'Option not implemented for Django 1.6 and below')
        for app in apps:
            try:
                if not Migrations(app):
                    raise NoMigrations(app)
            except NoMigrations:
                print('ATTENTION: No migrations found for {0}, creating initial migrations.'.format(app))
                try:
                    call_command('schemamigration', *(app,), initial=True, empty=empty)
                except SystemExit:
                    pass
            except ImproperlyConfigured:
                print('WARNING: The app: {0} could not be found.'.format(app))
            else:
                try:
                    call_command('schemamigration', *(app,), auto=True, empty=empty)
                except SystemExit:
                    pass
    else:
        for app in apps:
            call_command('makemigrations', *(app,), merge=merge, dry_run=dry_run, empty=empty)


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


def server(bind='127.0.0.1', port=8000, migrate_cmd=False):  # pragma: no cover
    from django.utils import autoreload

    if os.environ.get("RUN_MAIN") != "true":
        _create_db(migrate_cmd)
        User = get_user_model()
        if not User.objects.filter(is_superuser=True).exists():
            usr = create_user('admin', 'admin@admin.com', 'admin', is_staff=True, is_superuser=True)
            print('')
            print('A admin user (username: %s, password: admin) has been created.' % usr.get_username())
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
            if args['cms_check']:
                args['--cms'] = True

            if args['<command>']:
                from django.core.management import execute_from_command_line
                options = [option for option in args['options'] if option != '--cms' and '--extra-settings' not in option]
                _make_settings(args, application, settings, STATIC_ROOT, MEDIA_ROOT)
                execute_from_command_line(options)

            else:
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
                        if DJANGO_1_5:
                            runner = 'django.test.simple.DjangoTestSuiteRunner'
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
                                            args['--failfast'], runner,
                                            args['--runner-options'])
                        sys.exit(num_failures)
                elif args['server']:
                    server(args['--bind'], args['--port'],
                           args.get('--migrate', True))
                elif args['cms_check']:
                    cms_check(args.get('--migrate', True))
                elif args['compilemessages']:
                    compilemessages(application)
                elif args['makemessages']:
                    makemessages(application)
                elif args['makemigrations']:
                    makemigrations(application, merge=args['--merge'], dry_run=args['--dry-run'],
                                   empty=args['--empty'],
                                   extra_applications=args['<extra-applications>'])
                elif args['pyflakes']:
                    return static_analisys(application)
                elif args['authors']:
                    return generate_authors()


def main(argv=sys.argv):  # pragma: no cover
    # Command is executed in the main directory of the plugin, and we must
    # include it in the current path for the imports to work
    sys.path.insert(0, '.')

    if len(argv) > 1:
        application = argv[1]
        application_module = import_module(application)
        try:
            args = docopt(__doc__, version=application_module.__version__)
            if argv[2] == 'help':
                raise DocoptExit()
        except DocoptExit:
            if argv[2] == 'help':
                raise
            args = docopt(__doc__, argv[1:3], version=application_module.__version__)
        args['options'] = [argv[0]] + argv[2:]
        core(args=args, application=application)
    else:
        args = docopt(__doc__, version=__version__)
