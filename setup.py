# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import setuptools

setuptools.setup(
    entry_points={"console_scripts": ["django-app-helper = app_helper.main:main"]},
)
