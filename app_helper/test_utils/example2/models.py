# -*- coding: utf-8 -*-
from __future__ import print_function, with_statement

from django.db import models
from django.utils.translation import ugettext_lazy as _


class ExampleModel2(models.Model):
    test_field = models.CharField(max_length=20, verbose_name=_('Test field'))
