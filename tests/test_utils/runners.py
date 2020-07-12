import os
import sys
import unittest

from django.test.runner import DiscoverRunner

from app_helper.utils import work_in


class CapturedOutputRunner(DiscoverRunner):
    """Custom runner to discover tests only in sample applications."""

    def build_suite(self, test_labels=None, extra_tests=None, **kwargs):
        self.top_level = os.path.dirname(__file__)
        with work_in(os.path.dirname(__file__)):
            return super().build_suite(test_labels=test_labels, extra_tests=extra_tests, **kwargs)

    def run_suite(self, suite, **kwargs):
        return unittest.TextTestRunner(verbosity=self.verbosity, failfast=self.failfast, stream=sys.stderr).run(suite)
