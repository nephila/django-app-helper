from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import gettext_lazy as _


class Example(CMSApp):
    name = _("Example")
    urls = ["app_helper.urls"]


apphook_pool.register(Example)
