 _migrating:

####################################################
Migrating from djangocms-helper to django-app-helper
####################################################

This project used to be called djangocms-helper.
It's been renamed in version 2.0 to clarify that it's not limited to django CMS apps.

Migration is straightforward as it does not require any change to the codebase:

* all imports from ``djangocms_helper`` namespace are still valid and they won't be deprecated soon
* runner filername ``cms_helper.py`` is still valid and it won't be deprecated soon

*********************************
Migration path
*********************************

* Replace ``djangocms-helper`` package name from any dependendency declaration
  (``setup.py``, ``tox.ini``, ``requirements.txt`` ...)

That's it!

*********************************
Bugfixes and further development
*********************************

Bugfixes to djangocms-helper 1.2.x will be released until reasonable under the
old package name, while new features (including new Django / django CMS
versions support will only be available in the django-app-helper package).
