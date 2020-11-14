import unittest
from tempfile import gettempdir

from app_helper.utils import make_temp_dir


class TestUtils(unittest.TestCase):
    def test_make_temp_dir(self):
        temp1 = make_temp_dir("suff")
        self.assertTrue(temp1.startswith("/dev/shm"))
        self.assertTrue(temp1.endswith("suff"))

    def test_make_temp_dir_not_shm(self):
        temp1 = make_temp_dir("suff", container="/some/random/path")
        self.assertTrue(temp1.startswith(gettempdir()))
        self.assertTrue(temp1.endswith("suff"))
