from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path, re_path
from django.views.i18n import JavaScriptCatalog
from django.views.static import serve

from .utils import load_from_file

admin.autodiscover()

urlpatterns = [
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT, "show_indexes": True}),  # NOQA
    re_path(r"^jsi18n/(?P<packages>\S+?)/$", JavaScriptCatalog.as_view()),  # NOQA
]
i18n_urls = [
    re_path(r"^admin/", admin.site.urls),
]

try:
    load_from_file("%s.urls" % settings.BASE_APPLICATION)
    i18n_urls.append(
        re_path(r"^%s/" % settings.BASE_APPLICATION, include("%s.urls" % settings.BASE_APPLICATION))
    )  # NOQA
except OSError:  # pragma: no cover
    pass

if settings.USE_CMS:
    i18n_urls.append(path("", include("cms.urls")))  # NOQA

urlpatterns += i18n_patterns(*i18n_urls)
urlpatterns += staticfiles_urlpatterns()
