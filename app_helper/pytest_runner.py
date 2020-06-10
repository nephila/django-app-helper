import os
import shlex


class PytestTestRunner:
    """Runs pytest to discover and run tests."""

    def __init__(self, verbosity=1, failfast=False, keepdb=False, **kwargs):
        self.verbosity = verbosity
        self.failfast = failfast
        self.keepdb = keepdb
        self.extra_args = kwargs.pop("pytest_args", "")

    def run_tests(self, test_labels, *args, **kwargs):
        """Run pytest and return the exitcode.

        It translates some of Django's test command option to pytest's.
        """
        import pytest

        self.verbosity = kwargs.get("verbosity", self.verbosity)
        self.failfast = kwargs.get("failfast", self.failfast)
        self.keepdb = kwargs.get("keepdb", self.keepdb)
        argv = shlex.split(os.environ.get("PYTEST_ARGS", ""))
        if self.extra_args:
            argv.extend(shlex.split(self.extra_args))
        if self.verbosity == 0:  # pragma: no cover
            argv.append("--quiet")
        if self.verbosity == 2:  # pragma: no cover
            argv.append("--verbose")
        if self.verbosity == 3:  # pragma: no cover
            argv.append("-vv")
        if self.failfast:  # pragma: no cover
            argv.append("--exitfirst")
        if self.keepdb:  # pragma: no cover
            argv.append("--reuse-db")

        argv.extend(test_labels)
        return pytest.main(argv)
