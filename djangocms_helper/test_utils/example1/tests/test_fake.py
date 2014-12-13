# -*- coding: utf-8 -*-

try:
    from djangocms_helper.base_test import BaseTestCase

    class FakeTests(BaseTestCase):
        _pages_data = (
            {'en': {'title': 'Page title', 'template': 'page.html', 'publish': True},
             'fr': {'title': 'Titre', 'publish': True},
             'it': {'title': 'Titolo pagina', 'publish': False}},
            {'en': {'title': 'Second page', 'template': 'page.html', 'publish': True},
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

        def test_requests(self):
            from django.conf import settings
            if 'cms' in settings.INSTALLED_APPS:
                pages = self.get_pages()

                request = self.get_request(pages[1], 'en')
                self.assertEqual(request.path, u'/second-page')
                self.assertEqual(request.META['REQUEST_METHOD'], 'GET')

                request = self.post_request(pages[1], 'en', data={'payload': 1})
                self.assertEqual(request.path, u'/second-page')
                self.assertEqual(request.META['REQUEST_METHOD'], 'POST')
                self.assertEqual(request.POST.get('payload'), u'1')

                request = self.get_page_request(pages[1], lang='en',
                                                user=self.user_staff, edit=True,)
                self.assertEqual(request.path, u'/en/second-page/')
                self.assertTrue(request.toolbar)
                self.assertEqual(request.META['REQUEST_METHOD'], 'GET')
except Exception:
    from unittest2 import TestCase

    class FakeTests(TestCase):

        def test_fake(self):
            self.assertTrue(True)
