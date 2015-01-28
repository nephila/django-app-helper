# -*- coding: utf-8 -*-
from __future__ import print_function, with_statement
from django.utils.translation import ugettext_lazy as _
from django.db import models


class ExampleModel1(models.Model):
    test_field = models.CharField(max_length=20, default='',
                                  verbose_name=_(u'Test field'))
