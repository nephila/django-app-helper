# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.i18n import JavaScriptCatalog
from django.views.static import serve

from .utils import load_from_file

admin.autodiscover()

urlpatterns = [
    url(r'^media/(?P<path>.*)$', serve,  # NOQA
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    url(r'^jsi18n/(?P<packages>\S+?)/$', JavaScriptCatalog.as_view()),  # NOQA
]
i18n_urls = [
    url(r'^admin/', admin.site.urls),
]

try:
    load_from_file('%s.urls' % settings.BASE_APPLICATION)
    i18n_urls.append(
        url(r'^%s/' % settings.BASE_APPLICATION, include('%s.urls' % settings.BASE_APPLICATION))  # NOQA
    )
except IOError:
    pass

if settings.USE_CMS:
    i18n_urls.append(
        url(r'^', include('cms.urls'))  # NOQA
    )

urlpatterns += i18n_patterns(*i18n_urls)
urlpatterns += staticfiles_urlpatterns()
