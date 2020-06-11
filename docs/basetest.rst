###############
Base test class
###############


:py:class:`BaseTestCaseMixin` is available to provide helpers and methods that implements
repetitive tasks during development.
:py:class:`BaseTestCase`, :py:class:`BaseTransactionTestCase` are concrete classes extending
:py:class:`django.tests.TestCase` and :py:class:`django.tests.TransactionTestCase`


.. autoclass:: app_helper.base_test.BaseTestCaseMixin
    :members:
    :private-members:

    .. automethod:: app_helper.base_test.BaseTestCase._setup_users
    .. automethod:: app_helper.base_test.BaseTestCase._teardown_users
    .. automethod:: app_helper.base_test.BaseTestCase._setup_utils

    .. autoattribute:: app_helper.base_test.BaseTestCase._admin_user_username
    .. autoattribute:: app_helper.base_test.BaseTestCase._admin_user_password
    .. autoattribute:: app_helper.base_test.BaseTestCase._admin_user_email
    .. autoattribute:: app_helper.base_test.BaseTestCase._staff_user_username
    .. autoattribute:: app_helper.base_test.BaseTestCase._staff_user_password
    .. autoattribute:: app_helper.base_test.BaseTestCase._staff_user_email
    .. autoattribute:: app_helper.base_test.BaseTestCase._user_user_username
    .. autoattribute:: app_helper.base_test.BaseTestCase._user_user_password
    .. autoattribute:: app_helper.base_test.BaseTestCase._user_user_email
    .. autoattribute:: app_helper.base_test.BaseTestCase._pages_data


.. autoclass:: app_helper.base_test.BaseTestCase

.. autoclass:: app_helper.base_test.BaseTransactionTestCase
