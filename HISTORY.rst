.. :changelog:

*******
History
*******

.. towncrier release notes start

3.3.4 (2024-01-28)
==================

Features
--------

- Add DjangoCMS 3.11 to Django 5.0 test matrix (#252)


Bugfixes
--------

- Fix support for DEFAULT_FILE_STORAGE/STATICFILES_STORAGE in django 4.2 (#255)


3.3.3 (2023-11-28)
==================

Features
--------

- Prepare for Django 5.0 / Python 3.12 compatibility (#244)
- Switch to Coveralls Github action (#248)


3.3.2 (2023-09-26)
==================

Features
--------

- Migrate to bump-my-version (#237)


Bugfixes
--------

- Fix ruff linting (#232)


3.3.1 (2023-07-09)
==================

Bugfixes
--------

- Fix runner-options argument on Django test runner (#220)
- Do not add mptt with django-filer 3+ (#225)


3.3.0 (2023-05-07)
==================

Features
--------

- Add support for Django 4.x (#208)


3.2.0 (2023-01-19)
==================

Features
--------

- Add djangocms 3.11 to tox, fix tests accordingly (#311)


3.1.0 (2022-07-29)
==================

Features
--------

- Upgrade Python / Django versions (#204)
- Add minimal django 4.0 support (#208)


3.0.1 (2020-12-09)
==================

Bugfixes
--------

- Fix loading setting with pytest-django and django 3.1 (#202)


3.0.0 (2020-11-14)
==================

Features
--------

- Add support for Django 3.1 / django CMS 3.8 (#196)
- Add Django 3.0 / django CMS 3.7.2 support (#142)
- Drop Python 2 / Django 1.11 (#148)
- Add support for Daphne / channels runserver (#198)
- Refactor BaseTestCaseMixin to more composable mixins (#107)
- Replace makefile with invoke (#143)
- Use pre-commit for code formatting (#149)
- Allow to pass arguments to pytest via runner-options argument (#159)
- Add support to pytest command (#167)
- Update dotfiles to latest version (#189)
- Reorganize tests outside main package (#191)
- Remove support for aldryn-boilerplates (#199)


Bugfixes
--------

- Fix runner_options support (#92)
- Improve GA - Update contribution guide (#161)
- Allow extra arguments in PytestTestRunner.run_tests (#165)
- Update isort and linting configuration (#188)


Misc
----

- #152, #185


2.2.2 (2020-05-15)
=======================

Bugfixes
--------

- Fix pytest args splitting (#155)
- Fix runserver autoreload with channels 2.4 (#157)


2.2.1 (2020-04-23)
==================

- Fix packaging error

2.2.0 (2020-04-23)
==================

Features
--------

- Add Django 3.0 / django CMS 3.7.2 support (#142)
- Replace makefile with invoke (#143)


2.1.1 (2020-02-04)
==================

- Improved pytest compatibility

2.1.0 (2019-12-27)
==================

- Reformat code with black and improve flake8 configuration
- Add pytest-compatible runner

2.0.1 (2019-12-22)
==================

- Add Django 3.0 preliminary support

2.0.0 (2019-10-13)
==================

- Rename application to django-app-helper

1.2.5 (2019-08-16)
==================

- Add django CMS 3.7
- Add Django 2.2

1.2.4 (2019-08-08)
==================

- Fix regression introduced by #116

1.2.3 (2019-08-05)
==================

- Move pyflakes to extras_require
- Fix error in get_request / post_request not preserving current_page

1.2.2 (2019-07-05)
==================

- Improve request generation by adding a more generic request method

1.2.1 (2019-07-04)
==================

- Fix error when creating users with non-writable email attribute

1.2.0 (2019-03-22)
==================

- Drop compatiblity with Django <1.11, Python 3.4
- Add django CMS 3.6
- Add django 2.0, 2.1

1.1.1 (2019-07-03)
==================

- Fix error when creating users with non-writable email attribute

1.1.0 (2018-02-20)
==================

- Remove Django <1.8, Python 2.6, 3.3 from setup.py
- Add Django 1.11, Python 3.6
- Switch to new-style middlewares for Django 1.10+
- Create static methods to generate images
- Fix persistent option behavior with arbitrary commands
- Add minimal changes to allow third party application to run test on django 2.0
- Fix options for channels runserver
- Remove support for django-nose test runner

1.0.0 (2017-07-25)
==================

- Add ApphookReloadMiddleware in server mode
- Add a default for FILE_UPLOAD_TEMP_DIR
- Add fix for django CMS 3.4.4 render_plugin

0.9.8 (2017-03-04)
==================

- Fix compatibility with newer channels releases

0.9.7 (2016-12-03)
==================

- Add support for django-sekizai 0.10
- Fix mock dependency in setup.py
- Fix issue with server command in Django 1.10
- Fix issue with urls.py in Django 1.10
- Fix issue in tests with django CMS 3.4

0.9.6 (2016-08-25)
==================

- Add support for channels runserver.
- Add verbosity level to server command.
- Add support for Django 1.10.
- Add support for django CMS 3.4.

0.9.5 (2016-06-06)
==================

- Fix issue with mocked session storage
- Add verbosity level to tests
- Fix user creation
- Add option to allow parametrizing auto-created user
- Fix extra_applications

0.9.4 (2016-01-20)
==================

- Add Naked setup mode
- Add TEMPLATE_DIRS to special settings
- Add TEMPLATE_LOADERS to special settings
- Allow to specify a locale in makemessages

0.9.3 (2015-10-07)
==================

- Add --no-migrate option to skip migrations
- Add secure argument to generate HTTPS requests
- Better request mocking
- Fix test on django CMS 3.2 (develop)
- Add support for Python 3.5
- Add --persistent option for persistent storage

0.9.2 (2015-09-14)
==================

- Add support for apphooks and parent pages in BaseTestCase.create_pages
- If pages contains apphook, urlconf is reloaded automatically
- Improve documentation
- Add support for top-positioned MIDDLEWARE_CLASSES
- Code cleanup

0.9.1 (2015-08-30)
==================

- Better support for aldryn-boilerplates

0.9.0 (2015-08-20)
==================

- Complete support for Django 1.8 / django CMS develop
- Support for aldryn-boilerplates settings
- Migrations are now enabled by default during tests
- Minor BaseTestCase refactoring
- Remove support for Django 1.5
- Fix treebeard support
- Minor fixes
- Adds login_user_context method to BaseTestCase

0.8.1 (2015-05-31)
==================

- Add basic support for Django 1.8 / django CMS develop
- Code cleanups
- Smarter migration layout detection

0.8.0 (2015-03-22)
==================

- Add --native option to use native test command instead of django-app-helper one
- Use django-discover-runner on Django 1.5 if present
- Better handling of runner options
- Add support for empty/dry-run arguments to makemigrations
- Add USE_CMS flag to settings when using django CMS configuration

0.7.0 (2015-01-22)
==================

- Fix an error which prevents the runner to discover the settings
- django CMS is no more a dependency, install it manually to enable django CMS support

0.6.0 (2015-01-10)
==================

- Add a runner to make cms_helper file itself a runner for django-app-helper
- Fix issues with mptt / treebeard and Django 1.7
- Fix some makemigrations / --migrate issues
- Make django-app-helper less django CMS dependent

0.5.0 (2015-01-01)
==================

- Fixing bugs when using extra settings
- Add messages framework to default environment
- Add CSRF middleware / context_processor to default settings
- Add base helper class for test cases
- Complete Django 1.7 support
- Smarter detection of migration operations in Django 1.6-
- Add option to create migrations for external applications

0.4.0 (2014-09-18)
==================

- Add support for command line test runner options;
- Add check command on Django 1.7+;
- Add cms check command (which triggers cms inclusion);
- Add squashmigration command Django 1.7+;
- Add support for makemigrations merge on Django 1.7+;
- Add helpers for custom user models;

0.3.1 (2014-08-25)
==================

- Add staticfiles application;
- Add djangocms_admin_style if cms is enabled;

0.3.0 (2014-08-14)
==================

- Add support for django nose test runner;
- Add default CMS template;

0.2.0 (2014-08-12)
==================

- Add option to customize sample project settings;
- Add option to exclude django CMS from test project configurations;
- Add support for Django 1.7;

0.1.0 (2014-08-09)
==================

- First public release.
