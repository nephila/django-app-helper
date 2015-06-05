# -*- coding: utf-8 -*-
import os.path

from django.conf import settings
from django.http import SimpleCookie
from django.test import TestCase, RequestFactory
from django.utils.six import StringIO

from .utils import create_user, get_user_model


class BaseTestCase(TestCase):
    """
    Utils class that provides some helper methods to setup and interact with
    Django testing framework.

    """
    request_factory = None
    user = None
    user_staff = None
    user_normal = None
    site_1 = None
    languages = None

    """
    List of pages data for the different languages

    Example implementation::

    _pages_data = (
        {'en': {'title': 'Page title', 'template': 'page.html', 'publish': True},
         'fr': {'title': 'Titre', 'publish': True},
         'it': {'title': 'Titolo pagina', 'publish': False}},
    )
    """
    _pages_data = ()

    @classmethod
    def setUpClass(cls):
        from django.contrib.sites.models import Site
        cls.request_factory = RequestFactory()
        cls.user = create_user('admin', 'admin@admin.com', 'admin',
                               is_staff=True, is_superuser=True)
        cls.user_staff = create_user('staff', 'staff@admin.com', 'staff',
                                     is_staff=True)
        cls.user_normal = create_user('normal', 'normal@admin.com', 'normal')
        cls.site_1 = Site.objects.get(pk=1)

        try:
            from cms.utils import get_language_list
            cls.languages = get_language_list()
        except ImportError:
            cls.languages = [x[0] for x in settings.LANGUAGES]

    @classmethod
    def tearDownClass(cls):
        User = get_user_model()
        User.objects.all().delete()

    def get_pages_data(self):
        """
        Construct a list of pages in the different languages available for the
         project. Default implementation is to return the :py:attr:`_pages_data`
         attribute

        :return: list of pages data
        """
        return self._pages_data

    def get_pages(self):
        """
        Build pages according to the pages data provided by :py:meth:`get_pages_data`
        and returns the list of the draft version of each
        """
        from cms.api import create_page, create_title
        pages = []
        for page_data in self._pages_data:
            main_data = page_data[self.languages[0]]
            page = create_page(main_data['title'], main_data['template'],
                               language=self.languages[0])
            if main_data['publish']:
                page.publish(self.languages[0])
            for lang in self.languages[1:]:
                if lang in page_data:
                    create_title(language=lang, title=page_data[lang]['title'],
                                 page=page)
                    if page_data[lang]['publish']:
                        page.publish(lang)
            pages.append(page.get_draft_object())
        return pages

    def get_request(self, page, lang):
        """
        Create a GET request for the given page and language

        :param page: current page object
        :param lang: request language
        :return: request
        """
        request = self.request_factory.get(page.get_path(lang))
        request.current_page = page
        request.user = self.user
        request.session = {}
        request.cookies = SimpleCookie()
        request.errors = StringIO()
        return request

    def post_request(self, page, lang, data):
        """
        Create a POST request for the given page and language with CSRF disabled

        :param page: current page object
        :param lang: request language
        :return: request
        """
        request = self.request_factory.post(page.get_path(lang), data)
        request.current_page = page
        request.user = self.user
        request.session = {}
        request.cookies = SimpleCookie()
        request.errors = StringIO()
        request._dont_enforce_csrf_checks = True
        return request

    def get_page_request(self, page, user, path=None, edit=False, lang='en'):
        """
        Createds a GET request for the given page suitable for use the
        django CMS toolbar

        :param page: current page object
        :param user: current user
        :param path: path (if different from the current page path)
        :param edit: editing mode
        :param lang: request language
        :return: request
        """
        from cms.middleware.toolbar import ToolbarMiddleware
        path = path or page and page.get_absolute_url()
        if edit:
            path += '?edit'
        request = RequestFactory().get(path)
        request.session = {}
        request.user = user
        request.LANGUAGE_CODE = lang
        if edit:
            request.GET = {'edit': None}
        else:
            request.GET = {'edit_off': None}
        request.current_page = page
        mid = ToolbarMiddleware()
        mid.process_request(request)
        return request

    def reload_model(self, obj):
        return obj.__class__.objects.get(pk=obj.pk)

    def create_image(self, mode='RGB', size=(800, 600)):
        """
        Create a random image suitable for saving as DjangoFile
        :param mode: color mode
        :param size: tuple of width, height
        :return: image object

        It requires Pillow installed in the environment to work

        """
        from PIL import Image as PilImage, ImageDraw

        image = PilImage.new(mode, size)
        draw = ImageDraw.Draw(image)
        x_bit, y_bit = size[0] // 10, size[1] // 10
        draw.rectangle((x_bit, y_bit * 2, x_bit * 7, y_bit * 3), 'red')
        draw.rectangle((x_bit * 2, y_bit, x_bit * 3, y_bit * 8), 'red')
        return image

    def create_django_image_obj(self):
        """
        Create a django image file object suitable for FileField
        It also sets the following attributes:

        * ``self.image_name``: the image base name
        * ``self.filename``: the complete image path

        :return: django file object

        It requires Pillow installed in the environment to work

        """
        from django.core.files import File as DjangoFile

        img = self.create_image()
        self.image_name = 'test_file.jpg'
        self.filename = os.path.join(settings.FILE_UPLOAD_TEMP_DIR, self.image_name)
        img.save(self.filename, 'JPEG')
        return DjangoFile(open(self.filename, 'rb'), name=self.image_name)

    def create_filer_image_object(self):
        """
        Create a filer image object suitable for FilerImageField
        It also sets the following attributes:

        * ``self.image_name``: the image base name
        * ``self.filename``: the complete image path
        * ``self.filer_image``: the filer image object

        :return: filer image object

        It requires Pillow and django-filer installed in the environment to work

        """
        from filer.models import Image

        file_obj = self.create_django_image_obj()
        self.filer_image = Image.objects.create(owner=self.user, file=file_obj,
                                                original_filename=self.image_name)
        return self.filer_image