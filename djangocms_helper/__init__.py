"""
This is a compatibility package to allow legacy import to work without any changes
"""

import sys

# clone app_helper in djangocms_helper module
import app_helper  # NOQA

sys.modules[__name__] = sys.modules["app_helper"]
