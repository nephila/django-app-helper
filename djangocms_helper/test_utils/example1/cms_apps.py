# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class Example(CMSApp):
    name = _('Example')
    urls = ['djangocms_helper.urls']


apphook_pool.register(Example)
