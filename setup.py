# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import setuptools

from app_helper import __version__

test_requirements = []
requirements = [
    "docopt",
    "dj-database-url",
]


setuptools.setup(
    name="django-app-helper",
    version=__version__,
    url="https://github.com/nephila/django-app-helper",
    author="Iacopo Spalletti",
    author_email="i.spalletti@nephila.it",
    description="Helper for django applications development",
    long_description=open("README.rst").read(),
    license="GPLv2+",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=requirements,
    extras_require={
        ':python_version<"3.3"': ["mock"],
        "pyflakes": ["pyflakes<2.1", "django-cms>=3.4,<3.8"],
        "cms": ["django-cms>=3.4,<3.8"],
    },
    entry_points={"console_scripts": ["django-app-helper = app_helper.main:main"]},
    test_suite="app_helper.tests",
    tests_require=test_requirements,
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Development Status :: 5 - Production/Stable",
        "Framework :: Django",
        "Framework :: Django :: 1.11",
        "Framework :: Django :: 2.0",
        "Framework :: Django :: 2.1",
        "Framework :: Django :: 2.2",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
