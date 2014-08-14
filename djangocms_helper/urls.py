from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns

from .utils import load_from_file

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',  # NOQA
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    url(r'^jsi18n/(?P<packages>\S+?)/$', 'django.views.i18n.javascript_catalog'),  # NOQA
)
urlpatterns += i18n_patterns('',
    url(r'^admin/', include(admin.site.urls)),  # NOQA
)
try:
    load_from_file('%s.urls' % settings.BASE_APPLICATION)
    urlpatterns += i18n_patterns('',
        url(r'^%s/' % settings.BASE_APPLICATION, include('%s.urls' % settings.BASE_APPLICATION))  # NOQA
    )
except IOError:
    pass

if settings.USE_CMS:
    urlpatterns += i18n_patterns('',
        url(r'^', include('cms.urls'))  # NOQA
    )
