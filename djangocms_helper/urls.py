# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.views.i18n import javascript_catalog
from django.views.static import serve

from .utils import DJANGO_1_7, load_from_file

admin.autodiscover()

urlpatterns = [
    url(r'^media/(?P<path>.*)$', serve,  # NOQA
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    url(r'^jsi18n/(?P<packages>\S+?)/$', javascript_catalog),  # NOQA
]

i18n_urls = [
    url(r'^admin/', include(admin.site.urls)),  # NOQA
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

if not DJANGO_1_7:
    urlpatterns += i18n_patterns(*i18n_urls)
else:
    urlpatterns += i18n_patterns('', *i18n_urls)
