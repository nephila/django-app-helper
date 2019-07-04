.. :changelog:

History
-------

1.2.2 (2019-07-05)
++++++++++++++++++

* Improved request generation by adding a more generic request method

1.2.1 (2019-07-04)
++++++++++++++++++

* Fixed error when creating users with non-writable email attribute

1.2.0 (2019-03-22)
++++++++++++++++++

* Dropped compatiblity with Django <1.11, Python 3.4
* Added django CMS 3.6
* Added django 2.0, 2.1

1.1.1 (2019-07-03)
++++++++++++++++++

* Fixed error when creating users with non-writable email attribute

1.1.0 (2018-02-20)
++++++++++++++++++

* Removed Django <1.8, Python 2.6, 3.3 from setup.py
* Added Django 1.11, Python 3.6
* Switched to new-style middlewares for Django 1.10+
* Created static methods to generate images
* Fixed persistent option behavior with arbitrary commands
* Added minimal changes to allow third party application to run test on django 2.0
* Fixed options for channels runserver
* Removed support for django-nose test runner

1.0.0 (2017-07-25)
++++++++++++++++++

* Added ApphookReloadMiddleware in server mode
* Added a default for FILE_UPLOAD_TEMP_DIR
* Added fix for django CMS 3.4.4 render_plugin

0.9.8 (2017-03-04)
++++++++++++++++++

* Fixed compatibility with newer channels releases

0.9.7 (2016-12-03)
++++++++++++++++++

* Added support for django-sekizai 0.10
* Fixed mock dependency in setup.py
* Fixed issue with server command in Django 1.10
* Fixed issue with urls.py in Django 1.10
* Fixed issue in tests with django CMS 3.4

0.9.6 (2016-08-25)
++++++++++++++++++

* Added support for channels runserver.
* Added verbosity level to server command.
* Added support for Django 1.10.
* Added support for django CMS 3.4.

0.9.5 (2016-06-06)
++++++++++++++++++

* Fixed issue with mocked session storage
* Added verbosity level to tests
* Fixed user creation
* Added option to allow parametrizing auto-created user
* Fixed extra_applications

0.9.4 (2016-01-20)
++++++++++++++++++

* Add Naked setup mode
* Add TEMPLATE_DIRS to special settings
* Add TEMPLATE_LOADERS to special settings
* Allow to specify a locale in makemessages

0.9.3 (2015-10-07)
++++++++++++++++++

* Add --no-migrate option to skip migrations
* Add secure argument to generate HTTPS requests
* Better request mocking
* Fix test on django CMS 3.2 (develop)
* Add support for Python 3.5
* Add --persistent option for persistent storage

0.9.2 (2015-09-14)
++++++++++++++++++

* Add support for apphooks and parent pages in BaseTestCase.create_pages
* If pages contains apphook, urlconf is reloaded automatically
* Improve documentation
* Add support for top-positioned MIDDLEWARE_CLASSES
* Code cleanup

0.9.1 (2015-08-30)
++++++++++++++++++

* Better support for aldryn-boilerplates

0.9.0 (2015-08-20)
++++++++++++++++++

* Complete support for Django 1.8 / django CMS develop
* Support for aldryn-boilerplates settings
* Migrations are now enabled by default during tests
* Minor BaseTestCase refactoring
* Remove support for Django 1.5
* Fix treebeard support
* Minor fixes
* Adds login_user_context method to BaseTestCase

0.8.1 (2015-05-31)
++++++++++++++++++

* Add basic support for Django 1.8 / django CMS develop
* Code cleanups
* Smarter migration layout detection

0.8.0 (2015-03-22)
++++++++++++++++++

* Add --native option to use native test command instead of djangocms-helper one
* Use django-discover-runner on Django 1.5 if present
* Better handling of runner options
* Add support for empty/dry-run arguments to makemigrations
* Add USE_CMS flag to settings when using django CMS configuration

0.7.0 (2015-01-22)
++++++++++++++++++

* Fix an error which prevents the runner to discover the settings
* django CMS is no more a dependency, install it manually to enable django CMS support

0.6.0 (2015-01-10)
++++++++++++++++++

* Add a runner to make cms_helper file itself a runner for djangocms-helper
* Fix issues with mptt / treebeard and Django 1.7
* Fix some makemigrations / --migrate issues
* Make djangocms-helper less django CMS dependent

0.5.0 (2015-01-01)
++++++++++++++++++

* Fixing bugs when using extra settings
* Add messages framework to default environment
* Add CSRF middleware / context_processor to default settings
* Add base helper class for test cases
* Complete Django 1.7 support
* Smarter detection of migration operations in Django 1.6-
* Add option to create migrations for external applications

0.4.0 (2014-09-18)
++++++++++++++++++

* Add support for command line test runner options;
* Add check command on Django 1.7+;
* Add cms check command (which triggers cms inclusion);
* Add squashmigration command Django 1.7+;
* Add support for makemigrations merge on Django 1.7+;
* Add helpers for custom user models;

0.3.1 (2014-08-25)
++++++++++++++++++

* Add staticfiles application;
* Add djangocms_admin_style if cms is enabled;

0.3.0 (2014-08-14)
++++++++++++++++++

* Add support for django nose test runner;
* Add default CMS template;

0.2.0 (2014-08-12)
++++++++++++++++++

* Add option to customize sample project settings;
* Add option to exclude djanigo CMS from test project configurations;
* Add support for Django 1.7;

0.1.0 (2014-08-09)
++++++++++++++++++

* First public release.
