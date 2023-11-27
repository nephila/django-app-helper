import os  # pragma: no cover

from django.core.asgi import get_asgi_application  # pragma: no cover

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "helper")  # pragma: no cover

application = get_asgi_application()
