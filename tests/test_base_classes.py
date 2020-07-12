import os
import sys
import unittest

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.http import SimpleCookie
from django.test import Client, TestCase

from app_helper.base_test import GenericHelpersMixin, RequestTestCaseMixin
from app_helper.utils import create_user


class TestRequestTestCaseMixin(TestCase):
    class RequestTestCase(RequestTestCaseMixin, TestCase):
        client = Client()

    def test_request(self):
        """Base request object is created with cookies, session and language."""
        test_instance = self.RequestTestCase()

        request = test_instance.request("/")

        self.assertTrue(request.session)
        self.assertTrue(isinstance(request.user, AnonymousUser))
        self.assertTrue(isinstance(request.cookies, SimpleCookie))
        self.assertTrue(request.errors)
        self.assertEqual(request.LANGUAGE_CODE, "")
        with self.assertRaises(AttributeError):
            self.assertTrue(request.toolbar)

    def test_post_request(self):
        """POST request object is created with cookies, session and language, csrf checks disabled."""
        test_instance = self.RequestTestCase()

        request = test_instance.request("/", method="post", data={"some": "data"})

        self.assertEqual(request.session._session_key, "session_key")
        self.assertTrue(isinstance(request.user, AnonymousUser))
        self.assertTrue(isinstance(request.cookies, SimpleCookie))
        self.assertTrue(request.errors)
        self.assertTrue(request._dont_enforce_csrf_checks)
        self.assertEqual(request.LANGUAGE_CODE, "")
        with self.assertRaises(AttributeError):
            self.assertTrue(request.toolbar)

    def test_auth_request(self):
        """Request object with authenticated user, user is assigned to request."""

        User = get_user_model()  # noqa: N806
        user = User(username="some")
        test_instance = self.RequestTestCase()

        request = test_instance.request("/", method="post", data={"some": "data"}, user=user)
        self.assertTrue(request.session)
        self.assertEqual(request.user, user)
        self.assertTrue(isinstance(request.cookies, SimpleCookie))
        self.assertTrue(request.errors)
        self.assertTrue(request._dont_enforce_csrf_checks)
        self.assertEqual(request.LANGUAGE_CODE, "")
        with self.assertRaises(AttributeError):
            self.assertTrue(request.toolbar)

    def test_lang_request(self):
        """Request with forced language, language is assigned to LANGUAGE_CODE."""

        test_instance = self.RequestTestCase()

        request = test_instance.request("/", lang="en")
        self.assertEqual(request.LANGUAGE_CODE, "en")

    def test_login_user_context(self):
        """login_user_context force requests to be authenticated."""
        user = create_user("some", "some@testcom", "some")
        test_instance = self.RequestTestCase()
        with self.assertRaises(AssertionError):
            with test_instance.login_user_context(user, password="wrong"):
                test_instance.request("/", lang="en")
        with test_instance.login_user_context(user):
            request = test_instance.request("/", lang="en")
            self.assertEqual(request.user, user)
        request = test_instance.request("/", lang="en")
        self.assertTrue(isinstance(request.user, AnonymousUser))

    def test_apply_middleware(self):
        """Request with applied middlewares,"""
        test_instance = self.RequestTestCase()
        response = test_instance.request("/", lang="en", use_middlewares=True)

        self.assertFalse(response.current_page)
        # messages are not faked by the basic :py:attr:`request` call, we can use it to detect if middlewares are run
        self.assertIsNotNone(response._messages)
        try:
            import cms  # noqa: F401

            # toolbar is also set if django CMS is installed
            self.assertTrue(response.toolbar)
        except ImportError:
            pass

    def test_use_toolbar(self):
        """Request with django CMS toolbar."""
        try:
            import cms  # noqa: F401
        except ImportError:
            raise unittest.SkipTest("django CMS not available, skipping test")
        test_instance = self.RequestTestCase()
        response = test_instance.request("/", lang="en", use_toolbar=True)

        self.assertFalse(response.current_page)
        # messages are not faked by the basic :py:attr:`request` call, we can use it to detect if middlewares are run
        with self.assertRaises(AttributeError):
            self.assertIsNone(response._messages)
        # toolbar is also set
        self.assertTrue(response.toolbar)

    def test_set_page(self):
        """Request with django CMS page."""
        try:
            from cms.api import create_page
        except ImportError:
            raise unittest.SkipTest("django CMS not available, skipping test")
        test_instance = self.RequestTestCase()
        page = create_page(title="a page", language="en", template=settings.CMS_TEMPLATES[0][0])
        response = test_instance.request("/", lang="en", page=page)

        self.assertEqual(response.current_page, page)


class TestGenericHelpersMixin(TestCase):
    class GenericHelper(GenericHelpersMixin, TestCase):
        pass

    def test_reload_model(self):
        """:py:meth:`GenericHelper.reload_model` create a new object, do not patch the existing one."""
        user = create_user("some", "some@testcom", "some")
        test_instance = self.GenericHelper()
        user.random_attr = "random"
        user_new = test_instance.reload_model(user)
        with self.assertRaises(AttributeError):
            self.assertIsNotNone(user_new.random_attr)
        self.assertNotEqual(id(user), id(user_new))

    def test_temp_dir(self):
        """:py:meth:`GenericHelper.temp_dir` provide a temporary directory which is removed on context manager exit."""
        test_instance = self.GenericHelper()
        with test_instance.temp_dir() as temp_path:
            test_file = os.path.join(temp_path, "afile")
            open(test_file, "w")
            self.assertTrue(os.path.exists(test_file))
        self.assertFalse(os.path.exists(test_file))

    def test_captured_output(self):
        """:py:meth:`GenericHelper.captured_output` context manager capture output."""
        test_instance = self.GenericHelper()
        with test_instance.captured_output() as (out, err):
            print("out string")
            print("err string", file=sys.stderr)
        self.assertEqual(out.getvalue(), "out string\n")
        self.assertEqual(err.getvalue(), "err string\n")
