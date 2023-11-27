from django.utils import autoreload

from .utils import _create_db, create_user, get_user_model


def _run_django(settings, bind, port, migrate_cmd, verbose):
    """Run channels runserver."""
    from django.core.management.commands import runserver

    _setup_db(migrate_cmd)
    _init_runserver(runserver, bind, port, verbose)


def _run_daphne(settings, bind, port, migrate_cmd, verbose):
    """Run daphne runserver."""
    from daphne.cli import CommandLineInterface

    _setup_db(migrate_cmd)
    daphne_args = ["-b", bind, "-p", port, "-v", verbose or "1", settings.ASGI_APPLICATION]
    autoreload.run_with_reloader(CommandLineInterface().run, daphne_args)


def _run_channels(settings, bind, port, migrate_cmd, verbose):
    """Run channels runserver."""
    from channels.management.commands import runserver

    _setup_db(migrate_cmd)
    _init_runserver(runserver, bind, port, verbose, channels=True)


def _init_runserver(runserver_module, bind, port, verbose, logger=None, channels=False):
    """Run base django / channels runserver with autoreloader."""
    rs = runserver_module.Command()
    rs.use_ipv6 = False
    rs._raw_ipv6 = False
    rs.addr = bind
    rs.port = port
    if logger:  # pragma: no cover
        rs.logger = logger
    if channels:
        rs.http_timeout = 60
        rs.websocket_handshake_timeout = 5
    autoreload.run_with_reloader(
        rs.inner_run,
        **{
            "addrport": "{}:{}".format(bind, port),
            "insecure_serving": True,
            "use_static_handler": True,
            "use_threading": True,
            "verbosity": verbose,
            "skip_checks": True,
            "use_reloader": True,
        },
    )


def _setup_db(migrate_cmd):
    """Initialize the database running migrations and creating the default user."""
    _create_db(migrate_cmd)
    User = get_user_model()  # NOQA
    if not User.objects.filter(is_superuser=True).exists():
        usr = create_user("admin", "admin@admin.com", "admin", is_staff=True, is_superuser=True)
        print("")
        print("A admin user (username: %s, password: admin) " "has been created." % usr.get_username())
        print("")


def run(settings, bind, port, migrate_cmd, verbose, use_channels, use_daphne):
    """
    Run runserver command with reloader enabled.

    Currently support channels, daphne and plain django.

    :param settings: Django settings module
    :type settings: Settings
    :param bind: host to bind on
    :type bind: str
    :param port: port to bind on
    :type port: int
    :param migrate_cmd: run migrations when creating the database
    :type migrate_cmd: bool
    :param verbose: verbosity level
    :type verbose: int
    :param use_channels: run channels server
    :type use_channels: bool
    :param use_daphne: run daphne server
    :type use_daphne: bool
    """
    try:
        from channels.management.commands import runserver  # noqa: F401

        channels_enabled = True
    except ImportError:
        channels_enabled = False
    try:
        import daphne  # noqa: F401

        daphne_enabled = True
    except ImportError:
        daphne_enabled = False
    if use_channels and channels_enabled:
        _run_channels(settings, bind, port, migrate_cmd, verbose)
    elif use_daphne and daphne_enabled:
        _run_daphne(settings, bind, port, migrate_cmd, verbose)
    else:
        _run_django(settings, bind, port, migrate_cmd, verbose)
