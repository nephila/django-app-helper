# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import os.path
from collections import OrderedDict
from contextlib import contextmanager
from copy import deepcopy
from tempfile import mkdtemp

from django.conf import settings
from django.core.handlers.base import BaseHandler
from django.http import SimpleCookie
from django.test import RequestFactory, TestCase, TransactionTestCase
from django.utils.functional import SimpleLazyObject
from django.utils.six import StringIO

from .utils import UserLoginContext, create_user, get_user_model, reload_urls, temp_dir

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch


class BaseTestCaseMixin(object):
    """
    Utils mixin that provides some helper methods to setup and interact with
    Django testing framework.
    """
    request_factory = None
    user = None
    user_staff = None
    user_normal = None
    site_1 = None
    languages = None
    _login_context = None
    image_name = 'test_image.jpg'

    #: Username for auto-generated superuser
    _admin_user_username = 'admin'
    #: Password for auto-generated superuser
    _admin_user_password = 'admin'
    #: Email for auto-generated superuser
    _admin_user_email = 'admin@admin.com'

    #: Username for auto-generated staff user
    _staff_user_username = 'staff'
    #: Password for auto-generated staff user
    _staff_user_password = 'staff'
    #: Email for auto-generated staff user
    _staff_user_email = 'staff@admin.com'

    #: Username for auto-generated non-staff user
    _user_user_username = 'normal'
    #: Password for auto-generated non-staff user
    _user_user_password = 'normal'
    #: Email for auto-generated non-staff user
    _user_user_email = 'user@admin.com'

    _pages_data = ()
    """
    List of pages data for the different languages.

    Each item of the list is a dictionary containing the attributes
    (as accepted by ``cms.api.create_page``) of the page to be created.

    The first language will be created with ``cms.api.create_page`` the following
    languages using ``cms.api.create_title``

    Example:
        Single page created in en, fr, it languages::

            _pages_data = (
                {
                    'en': {'title': 'Page title', 'template': 'page.html', 'publish': True},
                    'fr': {'title': 'Titre', 'publish': True},
                    'it': {'title': 'Titolo pagina', 'publish': False}
                },
            )

    """

    @classmethod
    def setUpClass(cls):
        from django.contrib.sites.models import Site
        cls.request_factory = RequestFactory()
        cls.user = create_user(
            cls._admin_user_username, cls._admin_user_email, cls._admin_user_password,
            is_staff=True, is_superuser=True
        )
        cls.user_staff = create_user(
            cls._staff_user_username, cls._staff_user_email, cls._staff_user_password,
            is_staff=True, is_superuser=False
        )
        cls.user_normal = create_user(
            cls._user_user_username, cls._user_user_email, cls._user_user_password,
            is_staff=False, is_superuser=False
        )
        cls.site_1 = Site.objects.all().first()

        try:
            from cms.utils import get_language_list
            cls.languages = get_language_list()
        except ImportError:
            cls.languages = [x[0] for x in settings.LANGUAGES]
        super(BaseTestCaseMixin, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(BaseTestCaseMixin, cls).tearDownClass()
        User = get_user_model()
        User.objects.all().delete()

    @contextmanager
    def temp_dir(self):
        """
        Context manager to operate on a temporary directory
        """
        yield temp_dir()

    def reload_model(self, obj):
        """
        Reload a models instance from database
        :param obj: model instance to reload
        :return: the reloaded model instance
        """
        return obj.__class__.objects.get(pk=obj.pk)

    @staticmethod
    def reload_urlconf(urlconf=None):
        reload_urls(settings, urlconf)

    def login_user_context(self, user, password=None):
        """
        Context manager to make logged in requests
        :param user: user username
        :param password: user password (if omitted, username is used)
        """
        return UserLoginContext(self, user, password)

    def create_user(self, username, email, password, is_staff=False, is_superuser=False,
                    base_cms_permissions=False, permissions=None):
        """
        Creates a user with the given properties

        :param username: Username
        :param email: Email
        :param password: password
        :param is_staff: Staff status
        :param is_superuser: Superuser status
        :param base_cms_permissions: Base django CMS permissions
        :param permissions: Other permissions
        :return: User instance
        """
        return create_user(username, email, password, is_staff, is_superuser, base_cms_permissions,
                           permissions)

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
        Create pages using self._pages_data and self.languages

        :return: list of created pages
        """
        return self.create_pages(self._pages_data, self.languages)

    @staticmethod
    def create_pages(source, languages):
        """
        Build pages according to the pages data provided by :py:meth:`get_pages_data`
        and returns the list of the draft version of each
        """
        from cms.api import create_page, create_title
        pages = OrderedDict()
        has_apphook = False
        home_set = False
        for page_data in source:
            main_data = deepcopy(page_data[languages[0]])
            if 'publish' in main_data:
                main_data['published'] = main_data.pop('publish')
            main_data['language'] = languages[0]
            if main_data.get('parent', None):
                main_data['parent'] = pages[main_data['parent']]
            page = create_page(**main_data)
            has_apphook = has_apphook or 'apphook' in main_data
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
            if (
                not home_set and hasattr(page, 'set_as_homepage') and
                main_data.get('published', False)
            ):
                page.set_as_homepage()
                home_set = True
            page = page.get_draft_object()
            pages[page.get_slug(languages[0])] = page
        if has_apphook:
            reload_urls(settings, cms_apps=True)
        return list(pages.values())

    def get_content_renderer(self, request):
        """
        Returns a the plugin renderer. Only for django CMS 3.4+

        :param request: request instance
        :return: ContentRenderer instance
        """
        from cms.plugin_rendering import ContentRenderer
        return ContentRenderer(request)

    def get_plugin_context(self, page, lang, plugin, edit=False):
        """
        Returns a context suitable for CMSPlugin.render_plugin / render_placeholder

        :param page: Page object
        :param lang: Current language
        :param plugin: Plugin instance
        :param edit: Enable edit mode for rendering
        :return: PluginContext instance
        """
        from cms.plugin_rendering import PluginContext
        from sekizai.context_processors import sekizai

        request = self.get_page_request(page, self.user, lang=lang, edit=edit)
        context = {
            'request': request
        }
        renderer = self.get_content_renderer(request)
        if renderer:
            context['cms_content_renderer'] = renderer
        context.update(sekizai(request))
        return PluginContext(context, plugin, plugin.placeholder)

    def render_plugin(self, page, lang, plugin, edit=False):
        """
        Renders a single plugin using CMSPlugin.render_plugin

        :param page: Page object
        :param lang: Current language
        :param plugin: Plugin instance
        :param edit: Enable edit mode for rendering
        :return: Rendered plugin
        """
        context = self.get_plugin_context(page, lang, plugin, edit)
        content_renderer = context['cms_content_renderer']
        rendered = content_renderer.render_plugin(
            instance=plugin,
            context=context,
            placeholder=plugin.placeholder,
        )
        return rendered

    def _prepare_request(self, request, page, user, lang, use_middlewares, use_toolbar=False,
                         secure=False):
        from django.contrib.auth.models import AnonymousUser
        from importlib import import_module

        engine = import_module(settings.SESSION_ENGINE)

        if page:
            request.current_page = SimpleLazyObject(lambda: page)
        if not user:
            if self._login_context:
                user = self._login_context.user
            else:
                user = AnonymousUser()
        if user.is_authenticated:
            session_key = user._meta.pk.value_to_string(user)
        else:
            session_key = 'session_key'

        request.user = user
        request._cached_user = user
        request.session = engine.SessionStore(session_key)
        if secure:
            request.environ['SERVER_PORT'] = str('443')
            request.environ['wsgi.url_scheme'] = str('https')
        request.cookies = SimpleCookie()
        request.errors = StringIO()
        request.LANGUAGE_CODE = lang
        if request.method == 'POST':
            request._dont_enforce_csrf_checks = True
        # Let's use middleware in case requested, otherwise just use CMS toolbar if needed
        if use_middlewares:
            self._apply_middlewares(request)
        elif use_toolbar:
            from cms.middleware.toolbar import ToolbarMiddleware
            mid = ToolbarMiddleware()
            mid.process_request(request)
        return request

    def _apply_middlewares(self, request):
        handler = BaseHandler()
        from django.utils.module_loading import import_string
        for middleware_path in reversed(settings.MIDDLEWARE):
            middleware = import_string(middleware_path)
            mw_instance = middleware(handler)
            if hasattr(mw_instance, 'process_request'):
                mw_instance.process_request(request)

    def request(
        self, path, method='get', data=None, page=None, lang='', user=None,
        use_middlewares=False, secure=False, use_toolbar=False
    ):
        """
        Create a request for the given parameters.

        Request will be enriched with:

        * session
        * cookies
        * user (Anonymous if :param:user is `None`)
        * django CMS toolbar (is set)
        * current_page (if provided)

        :param path: request path
        :type path: str
        :param method: HTTP verb to use
        :type method: str
        :param data: payload to pass to the underlying :py:class:`RequestFactory` method
        :type data: dict
        :param page: current page object
        :type page: cms.models.Page
        :param lang: request language
        :type lang: str
        :param user: current user
        :type user: :py:class:`django.contrib.auth.AbstractUser`
        :param use_middlewares: pass the request through configured middlewares
        :type use_middlewares: bool
        :param secure: create HTTPS request
        :type secure: bool
        :param use_toolbar: add django CMS toolbar
        :type secure: bool
        :return: request
        """
        request = getattr(RequestFactory(), method)(path, data=data, secure=secure)
        return self._prepare_request(
            request, page, user, lang, use_middlewares, secure=secure, use_toolbar=use_toolbar
        )

    def get_request(
        self, page, lang, user=None, path=None, use_middlewares=False, secure=False,
        use_toolbar=False
    ):
        """
        Create a GET request for the given page and language

        :param page: current page object
        :param lang: request language
        :param user: current user
        :param path: path (if different from the current page path)
        :param use_middlewares: pass the request through configured middlewares.
        :param secure: create HTTPS request
        :param use_toolbar: add django CMS toolbar
        :return: request
        """
        path = path or page and page.get_absolute_url(lang)
        return self.request(
            path, method='get', data={}, page=None, lang=lang, user=user,
            use_middlewares=use_middlewares, secure=secure, use_toolbar=use_toolbar
        )

    def post_request(self, page, lang, data, user=None, path=None, use_middlewares=False,
                     secure=False, use_toolbar=False):
        """
        Create a POST request for the given page and language with CSRF disabled

        :param page: current page object
        :param lang: request language
        :param data: POST payload
        :param user: current user
        :param path: path (if different from the current page path)
        :param use_middlewares: pass the request through configured middlewares.
        :param secure: create HTTPS request
        :param use_toolbar: add django CMS toolbar
        :return: request
        """
        path = path or page and page.get_absolute_url(lang)
        return self.request(
            path, method='post', data=data, page=None, lang=lang, user=user,
            use_middlewares=use_middlewares, secure=secure, use_toolbar=use_toolbar
        )

    def get_page_request(self, page, user, path=None, edit=False, lang='en',
                         use_middlewares=False, secure=False):
        """
        Create a GET request for the given page suitable for use the
        django CMS toolbar

        This method requires django CMS installed to work. It will raise an ImportError otherwise;
        not a big deal as this method makes sense only in a django CMS environment

        :param page: current page object
        :param user: current user
        :param path: path (if different from the current page path)
        :param edit: whether enabling editing mode
        :param lang: request language
        :param use_middlewares: pass the request through configured middlewares.
        :param secure: create HTTPS request
        :return: request
        """
        from cms.utils.conf import get_cms_setting
        edit_on = get_cms_setting('CMS_TOOLBAR_URL__EDIT_ON')
        path = path or page and page.get_absolute_url(lang)
        if edit:
            path = '{0}?{1}'.format(path, edit_on)
        request = self.request_factory.get(path, secure=secure)
        return self._prepare_request(request, page, user, lang, use_middlewares, use_toolbar=True,
                                     secure=secure)

    @staticmethod
    def create_image(mode='RGB', size=(800, 600)):
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

    def create_django_image_obj(self):  # pragma: no cover
        return self.create_django_image_object()

    def create_django_image_object(self):
        """
        Create a django image file object suitable for FileField
        It also sets the following attributes:

        * ``self.image_name``: the image base name
        * ``self.filename``: the complete image path

        :return: django file object

        It requires Pillow installed in the environment to work

        """
        img_obj, self.filename = self.create_django_image()
        self.image_name = img_obj.name
        return img_obj

    @staticmethod
    def create_django_image():
        """
        Create a django image file object suitable for FileField
        It also sets the following attributes:

        * ``self.image_name``: the image base name
        * ``self.filename``: the complete image path

        :return: (django file object, path to file image)

        It requires Pillow installed in the environment to work
        """
        from django.core.files import File as DjangoFile

        img = BaseTestCase.create_image()
        image_name = 'test_file.jpg'
        if settings.FILE_UPLOAD_TEMP_DIR:
            tmp_dir = settings.FILE_UPLOAD_TEMP_DIR
        else:
            tmp_dir = mkdtemp()
        filename = os.path.join(tmp_dir, image_name)
        img.save(filename, 'JPEG')
        return DjangoFile(open(filename, 'rb'), name=image_name), filename

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
        self.filer_image = self.create_filer_image(self.user, self.image_name)
        return self.filer_image

    @staticmethod
    def create_filer_image(user, image_name):
        """
        Create a filer image object suitable for FilerImageField
        It also sets the following attributes:

        * ``self.image_name``: the image base name
        * ``self.filename``: the complete image path
        * ``self.filer_image``: the filer image object

        :param user: image owner
        :param image_name: image name
        :return: filer image object

        It requires Pillow and django-filer installed in the environment to work

        """
        from filer.models import Image

        file_obj, filename = BaseTestCase.create_django_image()
        filer_image = Image.objects.create(
            owner=user, file=file_obj, original_filename=image_name
        )
        return filer_image

    @contextmanager
    def captured_output(self):
        """
        Context manager that patches stdout / stderr with StringIO and return the instances.
        Use it to test output

        :return: stdout, stderr wrappers
        """
        with patch('sys.stdout', new_callable=StringIO) as out:
            with patch('sys.stderr', new_callable=StringIO) as err:
                yield out, err


class BaseTestCase(BaseTestCaseMixin, TestCase):
    """
    Base class that implements :py:class:`BaseTestCaseMixin` and
    :py:class:`django.tests.TestCase`
    """


class BaseTransactionTestCase(BaseTestCaseMixin, TransactionTestCase):
    """
    Base class that implements :py:class:`BaseTestCaseMixin` and
    :py:class:`django.tests.TransactionTestCase`
    """
