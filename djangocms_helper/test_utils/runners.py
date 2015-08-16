# -*- coding: utf-8 -*-
import sys

from django.test.runner import DiscoverRunner
from django.utils import unittest


class CapturedOutputRunner(DiscoverRunner):

    def run_suite(self, suite, **kwargs):
        return unittest.TextTestRunner(
            verbosity=self.verbosity,
            failfast=self.failfast,
            stream=sys.stderr
        ).run(suite)
