# -*- coding: utf-8 -*-
import os

try:
    import unittest2 as unittest
except ImportError:
    import unittest

try:
    from django.contrib.auth.models import AnonymousUser
    from djangocms_helper.base_test import BaseTestCase
    from djangocms_helper.utils import get_user_model_labels

    class FakeTests(BaseTestCase):
        _pages_data = (
            {'en': {'title': 'Page title', 'template': 'page.html', 'publish': True},
             'fr': {'title': 'Titre', 'publish': True},
             'it': {'title': 'Titolo pagina', 'publish': False}},
            {'en': {'title': 'Second page', 'template': 'page.html', 'publish': True,
                    'parent': 'page-title', 'apphook': 'Example'
                    },
             'fr': {'title': 'Deuxieme', 'publish': True},
             'it': {'title': 'Seconda pagina', 'publish': False}},
        )

        def test_fake(self):
            self.assertTrue(True)

        def test_pages(self):
            from django.conf import settings
            data = self.get_pages_data()
            self.assertEqual(set(data[0].keys()), set(('en', 'fr', 'it')))

            if 'cms' in settings.INSTALLED_APPS:
                pages = self.get_pages()
                self.assertEqual(len(pages), 2)

        def test_get(self):
            from django.conf import settings
            if 'cms' not in settings.INSTALLED_APPS:
                raise unittest.SkipTest('django CMS not available, skipping test')
            from cms.api import add_plugin
            pages = self.get_pages()
            add_plugin(placeholder=pages[0].placeholders.get(slot='content'),
                       plugin_type='FakePlugin', language='en')
            pages[0].publish('en')
            response = self.client.get('/en/')
            self.assertContains(response, 'fake text')
            self.assertContains(response, 'body{font-weight: bold;}')
            self.assertContains(response, 'Page title')

        def test_create_user(self):
            from django.conf import settings
            if 'cms' not in settings.INSTALLED_APPS:
                raise unittest.SkipTest('django CMS not available, skipping test')
            user = self.create_user(username='random', email='random@example.com',
                                    password='random', is_staff=True,
                                    base_cms_permissions=True, permissions=['add_placeholder'])
            self._login_context = self.login_user_context(user)
            self._login_context.user.has_perm('add_placeholdr')
            self._login_context.user.has_perm('add_text')

        def test_login_context(self):
            request = self.get_request(None, 'en', path='/en')
            self.assertTrue(request.user, AnonymousUser())

            self._login_context = self.login_user_context(self.user)
            request = self.get_request(None, 'en', path='/en')
            self.assertTrue(request.user, self.user)
            self._login_context.__exit__(None, None, None)

            request = self.get_request(None, 'en', path='/en')
            self.assertTrue(request.user, AnonymousUser())

            with self.login_user_context(self.user):
                request = self.get_request(None, 'en', path='/en')
                self.assertTrue(request.user, self.user)

            request = self.get_request(None, 'en', path='/en')
            self.assertTrue(request.user, AnonymousUser())

        def test_requests(self):
            from django.conf import settings
            if 'cms' in settings.INSTALLED_APPS:
                pages = self.get_pages()

                request = self.get_request(pages[1], 'en')
                self.assertEqual(request.path, '/en/second-page/')
                self.assertEqual(request.META['REQUEST_METHOD'], 'GET')

                request = self.post_request(pages[1], 'en', data={'payload': 1})
                self.assertEqual(request.path, '/en/second-page/')
                self.assertEqual(request.META['REQUEST_METHOD'], 'POST')
                self.assertEqual(request.POST.get('payload'), '1')

                request = self.get_page_request(pages[1], lang='en',
                                                user=self.user_staff, edit=True,)
                self.assertEqual(request.path, '/en/second-page/')
                self.assertTrue(request.toolbar)
                self.assertEqual(request.META['REQUEST_METHOD'], 'GET')

        def test_get_user_model(self):
            if 'AUTH_USER_MODEL' not in os.environ:
                user_orm_label, user_model_label = get_user_model_labels()
                self.assertEqual(user_orm_label, 'auth.User')
                self.assertEqual(user_model_label, 'auth.user')

except Exception:
    from unittest2 import TestCase

    class FakeTests(TestCase):

        def test_fake(self):
            self.assertTrue(True)
