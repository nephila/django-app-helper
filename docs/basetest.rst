################
Base test mixins
################

The following mixins are  available to provide helpers and methods that implements helpers and functions commonly
used in tests.
:py:class:`BaseTestCase`, :py:class:`BaseTransactionTestCase` are concrete classes implementing all the mixins and
extending respectively :py:class:`django.tests.TestCase` and :py:class:`django.tests.TransactionTestCase`


.. autoclass:: app_helper.base_test.RequestTestCaseMixin
    :members:
    :private-members:


.. autoclass:: app_helper.base_test.CreateTestDataMixin
    :members:

    .. automethod:: app_helper.base_test.CreateTestDataMixin._setup_users
    .. automethod:: app_helper.base_test.CreateTestDataMixin._teardown_users

    .. autoattribute:: app_helper.base_test.CreateTestDataMixin._admin_user_username
    .. autoattribute:: app_helper.base_test.CreateTestDataMixin._admin_user_password
    .. autoattribute:: app_helper.base_test.CreateTestDataMixin._admin_user_email
    .. autoattribute:: app_helper.base_test.CreateTestDataMixin._staff_user_username
    .. autoattribute:: app_helper.base_test.CreateTestDataMixin._staff_user_password
    .. autoattribute:: app_helper.base_test.CreateTestDataMixin._staff_user_email
    .. autoattribute:: app_helper.base_test.CreateTestDataMixin._user_user_username
    .. autoattribute:: app_helper.base_test.CreateTestDataMixin._user_user_password
    .. autoattribute:: app_helper.base_test.CreateTestDataMixin._user_user_email


.. autoclass:: app_helper.base_test.CMSPageRenderingMixin
    :members:

    .. automethod:: app_helper.base_test.CMSPageRenderingMixin._setup_cms
    .. autoattribute:: app_helper.base_test.CMSPageRenderingMixin._pages_data


.. autoclass:: app_helper.base_test.GenericHelpersMixin
    :members:
    :private-members:

.. autoclass:: app_helper.base_test.BaseNoDataTestCaseMixin
    :members:
    :private-members:


.. autoclass:: app_helper.base_test.BaseTestCaseMixin
    :members:
    :private-members:


.. autoclass:: app_helper.base_test.BaseTestCase

.. autoclass:: app_helper.base_test.BaseTransactionTestCase
