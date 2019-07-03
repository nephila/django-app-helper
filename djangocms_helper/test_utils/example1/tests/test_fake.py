# -*- coding: utf-8 -*-
import os

try:
    import unittest2 as unittest
except ImportError:
    import unittest

try:
    from django.contrib.auth.models import AnonymousUser
    from djangocms_helper.base_test import BaseTestCase
    from djangocms_helper.utils import get_user_model_labels, CMS_34


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
            print('visible string')
            with self.captured_output() as (out, err):
                print('hidden string')
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
            if os.environ.get('AUTH_USER_MODEL', 'auth.User'):
                user_orm_label, user_model_label = get_user_model_labels()
                self.assertEqual(user_orm_label, 'auth.User')
                self.assertEqual(user_model_label, 'auth.user')

        def test_create_image(self):
            from filer.models import Image

            image = self.create_filer_image_object()
            self.assertEqual(image.original_filename, self.image_name)
            self.assertEqual(image.width, 800)
            self.assertEqual(image.height, 600)
            self.assertEqual(Image.objects.count(), 1)

        def test_create_filer_image(self):
            from filer.models import Image

            image = BaseTestCase.create_filer_image(self.user, 'random.jpg')
            self.assertEqual(image.original_filename, 'random.jpg')
            self.assertEqual(image.width, 800)
            self.assertEqual(image.height, 600)
            self.assertEqual(Image.objects.count(), 1)

        def test_create_django_image_object(self):
            image = self.create_django_image_object()
            self.assertEqual(image.name, self.image_name)

        def test_render_plugin(self):
            from django.conf import settings
            if 'cms' not in settings.INSTALLED_APPS:
                raise unittest.SkipTest('django CMS not available, skipping test')

            from cms.api import add_plugin
            sample_text = '\nfake text\nen\nPage title\n\n'
            pages = self.get_pages()
            public = pages[0].get_public_object()
            placeholder = pages[0].placeholders.get(slot='content')
            plugin = add_plugin(placeholder=placeholder, plugin_type='FakePlugin', language='en')
            pages[0].publish('en')
            rendered_2 = self.render_plugin(public, 'en', plugin)
            if CMS_34:
                context = self.get_plugin_context(pages[0], 'en', plugin, edit=False)
                rendered_1 = plugin.render_plugin(context, placeholder)
                self.assertEqual(rendered_2, rendered_1)
            self.assertEqual(rendered_2, sample_text)

        def test_request(self):
            from django.conf import settings
            if 'cms' not in settings.INSTALLED_APPS:
                raise unittest.SkipTest('django CMS not available, skipping test')

            pages = self.get_pages()

            request = self.get_request(pages[1], lang='en')
            self.assertIsNone(getattr(request, 'toolbar', None))

            request = self.get_page_request(pages[1], user=self.user)
            self.assertIsNotNone(getattr(request, 'toolbar', None))

            request = self.get_request(pages[1], 'en', use_middlewares=True)
            self.assertIsNotNone(getattr(request, 'toolbar', None))
            self.assertIsNotNone(getattr(request, '_messages', None))

            request = self.get_request(pages[1], 'en', secure=True)
            self.assertTrue(request.is_secure())

        def test_request_full_middlewares(self):
            # naked request
            request = self.get_request(
                page=None, lang='en', user=None, path='/en/second-page/',
                use_middlewares=True
            )
            self.assertEqual(request.user, AnonymousUser())
            with self.assertRaises(AttributeError):
                self.assertTrue(request.current_page.pk)
            self.assertIsNotNone(getattr(request, '_messages', None))

            # passing user
            request = self.get_request(
                page=None, lang='en', user=self.user, path='/en/second-page/',
                use_middlewares=True
            )
            self.assertEqual(request.user, self.user)
            with self.assertRaises(AttributeError):
                self.assertTrue(request.current_page.pk)
            self.assertIsNotNone(getattr(request, '_messages', None))

            # logged in user
            with self.login_user_context(self.user):
                request = self.get_request(
                    page=None, lang='en', user=None, path='/en/second-page/',
                    use_middlewares=True
                )
                self.assertEqual(request.user, self.user)
                with self.assertRaises(AttributeError):
                    self.assertTrue(request.current_page.pk)

        def test_request_full_middlewares_cms(self):
            from django.conf import settings
            if 'cms' not in settings.INSTALLED_APPS:
                raise unittest.SkipTest('django CMS not available, skipping test')

            pages = self.get_pages()
            # naked request, page and language is derived from path
            request = self.get_request(
                page=None, lang=None, user=None, path='/en/second-page/',
                use_middlewares=True
            )
            self.assertEqual(request.user, AnonymousUser())
            self.assertEqual(request.LANGUAGE_CODE, 'en')
            self.assertEqual(request.current_page.get_absolute_url(), pages[1].get_absolute_url())
            self.assertIsNotNone(getattr(request, '_messages', None))

            # naked request, page and language is derived from path, user is logged in
            request = self.get_request(
                page=None, lang=None, user=self.user, path='/en/second-page/',
                use_middlewares=True
            )
            self.assertEqual(request.user, self.user)
            self.assertEqual(request.LANGUAGE_CODE, 'en')
            self.assertEqual(request.current_page.get_absolute_url(), pages[1].get_absolute_url())
            self.assertIsNotNone(getattr(request, '_messages', None))

            # naked request, path is derived from path
            request = self.get_request(
                page=pages[1], lang='en', user=self.user,
                use_middlewares=True
            )
            self.assertEqual(request.user, self.user)
            self.assertEqual(request.path_info, '/en/second-page/')
            self.assertEqual(request.LANGUAGE_CODE, 'en')
            self.assertEqual(request.current_page.get_absolute_url(), pages[1].get_absolute_url())
            self.assertIsNotNone(getattr(request, '_messages', None))

            # logged in user through context manager
            with self.login_user_context(self.user):
                request = self.get_request(
                    page=None, lang=None, user=None, path='/en/second-page/',
                    use_middlewares=True
                )
                self.assertEqual(request.user, self.user)
                self.assertEqual(request.current_page.get_absolute_url(), pages[1].get_absolute_url())


except Exception as e:
    print(e)
    from unittest2 import TestCase

    class FakeTests(TestCase):

        def test_fake(self):
            self.assertTrue(True)
