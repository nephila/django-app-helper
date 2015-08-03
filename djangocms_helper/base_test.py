# -*- coding: utf-8 -*-
import os.path
import shutil
import sys
from contextlib import contextmanager
from copy import deepcopy
from tempfile import mkdtemp

from django.conf import settings
from django.core.handlers.base import BaseHandler
from django.core.urlresolvers import clear_url_caches
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
        super(BaseTestCase, cls).setUpClass()
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
        super(BaseTestCase, cls).tearDownClass()
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
        return self.create_pages(self._pages_data, self.languages)

    @staticmethod
    def create_pages(source, languages):
        """
        Build pages according to the pages data provided by :py:meth:`get_pages_data`
        and returns the list of the draft version of each
        """
        from cms.api import create_page, create_title
        pages = []
        for page_data in source:
            main_data = deepcopy(page_data[languages[0]])
            if 'publish' in main_data:
                main_data['published'] = main_data.pop('publish')
            main_data['language'] = languages[0]
            page = create_page(**main_data)
            for lang in languages[1:]:
                if lang in page_data:
                    publish = False
                    title_data = deepcopy(page_data[lang])
                    if 'publish' in title_data:
                        publish = title_data.pop('publish')
                    if 'published' in title_data:
                        publish = title_data.pop('published')
                    title_data['language'] = lang
                    title_data['page'] = page
                    create_title(**title_data)
                    if publish:
                        page.publish(lang)
            pages.append(page.get_draft_object())
        return pages

    @staticmethod
    def reload_urlconf(urlconf=None):
        if 'cms.urls' in sys.modules:
            reload(sys.modules['cms.urls'])
        if urlconf is None:
            urlconf = settings.ROOT_URLCONF
        if urlconf in sys.modules:
            reload(sys.modules[urlconf])
        clear_url_caches()
        try:
            from cms.appresolver import clear_app_resolvers, get_app_patterns
            clear_app_resolvers()
            get_app_patterns()
        except ImportError:
            pass

    def _prepare_request(self, request, page, user, lang, use_middlewares, use_toolbar=False):
        request.current_page = page
        request.user = user
        request.session = {}
        request.cookies = SimpleCookie()
        request.errors = StringIO()
        request.LANGUAGE_CODE = lang
        if page:
            request.current_page = page
        # Let's use middleware in case requested, otherwise just use CMS toolbar if needed
        if use_middlewares:
            handler = BaseHandler()
            handler.load_middleware()
            for middleware_method in handler._request_middleware:
                if middleware_method(request):
                    raise Exception(u'Couldn\'t create request mock object -'
                                    u'request middleware returned a response')
        elif use_toolbar:
            from cms.middleware.toolbar import ToolbarMiddleware
            mid = ToolbarMiddleware()
            mid.process_request(request)
        return request

    def get_request(self, page, lang, user=None, path=None, use_middlewares=False):
        """
        Create a GET request for the given page and language

        :param page: current page object
        :param lang: request language
        :return: request
        """
        path = path or page and page.get_absolute_url(lang)
        request = self.request_factory.get(path)
        return self._prepare_request(request, page, user, lang, use_middlewares)

    def post_request(self, page, lang, data, user=None, path=None, use_middlewares=False):
        """
        Create a POST request for the given page and language with CSRF disabled

        :param page: current page object
        :param lang: request language
        :param data: POST payload
        :param user: current user
        :param path: path (if different from the current page path)
        :param use_middlewares: whether go through all configured middlewares.
        :return: request
        """
        path = path or page and page.get_absolute_url(lang)
        request = self.request_factory.post(path, data)
        return self._prepare_request(request, page, user, lang, use_middlewares)

    def get_page_request(self, page, user, path=None, edit=False, lang='en', use_middlewares=False):
        """
        Createds a GET request for the given page suitable for use the
        django CMS toolbar

        This method requires django CMS installed to work. It will raise an ImportError otherwise;
        not a big deal as this method makes sense only in a django CMS environment

        :param page: current page object
        :param user: current user
        :param path: path (if different from the current page path)
        :param edit: whether enabling editing mode
        :param lang: request language
        :param use_middlewares: whether go through all configured middlewares.
        :return: request
        """
        from cms.utils.conf import get_cms_setting
        edit_on = get_cms_setting('CMS_TOOLBAR_URL__EDIT_ON')
        edit_off = get_cms_setting('CMS_TOOLBAR_URL__EDIT_OFF')
        path = path or page and page.get_absolute_url(lang)
        if edit:
            path = '{0}?{1}'.format(path, edit_on)
        request = self.request_factory.get(path)
        return self._prepare_request(request, page, user, lang, use_middlewares, use_toolbar=True)

    def reload_model(self, obj):
        """
        Reload a models instance from database
        :param obj: model instance to reload
        :return:
        """
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

    @contextmanager
    def temp_dir(self):
        """
        Context manager to operate on a temporary directory
        :return:
        """
        name = mkdtemp()
        yield name
        shutil.rmtree(name)

