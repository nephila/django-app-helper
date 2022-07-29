from django.db import models
from django.utils.translation import gettext_lazy as _


class ExampleModel1(models.Model):
    test_field = models.CharField(max_length=20, default="", verbose_name=_("Test field"))
