# -*- coding: utf-8 -*-
import sys
from django.test.simple import DjangoTestSuiteRunner
from django.utils import unittest


class CapturedOutputRunner(DjangoTestSuiteRunner):

    def run_suite(self, suite, **kwargs):
        return unittest.TextTestRunner(
            verbosity=self.verbosity,
            failfast=self.failfast,
            stream=sys.stderr
        ).run(suite)
