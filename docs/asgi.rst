#######################
ASGI / Channels support
#######################

django-app-helper comes with minimal channels / ASGI support.

Default configuration provides a sample ``asgi`` application already enabled in ``ASGI_APPLICATION`` setting.

This means that if you install ``channels`` or ``daphne`` in your rest environment ``./helper.py server`` can run a channels / ASGI enabled instance.

.. note:: Pure ASGI support is available only for Django 3.0+.

************************
Run with channels
************************

To run with channels you must provide an ``ASGI_APPLICATION`` in the project ``helper.py`` pointing to your base channels application.

Optionally you can set ``CHANNEL_LAYERS``.

Example:

    .. code-block:: python

        # required
        ASGI_APPLICATION='tests.example_app.routing.application',
        # Optional
        CHANNEL_LAYERS={
            'default': {
                'BACKEND': 'channels_redis.core.RedisChannelLayer',
                'CONFIG': {
                    'hosts': [('localhost', 6379)],
                },
            },
        }


The run the ``server`` command with the ``--use-channels`` option set::

    $ python helper.py server --use-channels

************************
Run with daphne
************************

To run with daphne you can provide a custom ``ASGI_APPLICATION`` in the project ``helper.py`` if you actually have one or more ASGI application configure beyond django. The default ``ASGI_APPLICATION`` will run the django runserver command.

Example:

    .. code-block:: python

        ASGI_APPLICATION='my_project.asgi:application',


The run the ``server`` command with the ``--use-daphne`` option set::

    $ python helper.py server --use-daphne
