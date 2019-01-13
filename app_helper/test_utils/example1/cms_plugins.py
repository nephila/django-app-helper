# -*- coding: utf-8 -*-
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool


class FakePlugin(CMSPluginBase):
    name = 'FakePlugin'
    render_template = 'fake_plugin.html'


plugin_pool.register_plugin(FakePlugin)
