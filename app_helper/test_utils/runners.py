# -*- coding: utf-8 -*-
import sys

from django.test.runner import DiscoverRunner

try:
    from django.utils import unittest
except ImportError:
    import unittest


class CapturedOutputRunner(DiscoverRunner):

    def run_suite(self, suite, **kwargs):
        return unittest.TextTestRunner(
            verbosity=self.verbosity,
            failfast=self.failfast,
            stream=sys.stderr
        ).run(suite)


try:
    from django.test.simple import DjangoTestSuiteRunner

    class CapturedOutputSimpleRunner(DjangoTestSuiteRunner):

        def run_suite(self, suite, **kwargs):
            return unittest.TextTestRunner(
                verbosity=self.verbosity,
                failfast=self.failfast,
                stream=sys.stderr
            ).run(suite)

except ImportError:
    CapturedOutputSimpleRunner = CapturedOutputRunner
