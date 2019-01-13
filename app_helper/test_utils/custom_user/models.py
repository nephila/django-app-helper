# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):

    @property
    def email(self):
        return 'some@example.com'
