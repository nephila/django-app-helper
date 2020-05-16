import sys
import unittest  # noqa

from django.test.runner import DiscoverRunner


class CapturedOutputRunner(DiscoverRunner):
    def run_suite(self, suite, **kwargs):
        return unittest.TextTestRunner(verbosity=self.verbosity, failfast=self.failfast, stream=sys.stderr).run(suite)
