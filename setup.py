import setuptools
import sys
from djangocms_helper import __version__

test_requirements = []
if sys.version_info[:2] < (2, 7):
    test_requirements.append('unittest2')
    test_suite = 'unittest2.collector'
else:
    test_suite = 'djangocms_helper.tests'

setuptools.setup(
    name="djangocms-helper",
    version=__version__,
    url="https://github.com/nephila/djangocms-helper",

    author="Iacopo Spalletti",
    author_email="i.spalletti@nephila.it",

    description="Helpers for django CMS plugin development",
    long_description=open('README.rst').read(),
    license='GPLv2+',

    packages=setuptools.find_packages(),
    include_package_data=True,

    install_requires=[
        'pyflakes',
        'docopt',
        'dj-database-url',
        'pyflakes',
        'south',
        'django',
        'mock',
    ],
    entry_points={
        'console_scripts': [
            'djangocms-helper = djangocms_helper.main:main',
        ]
    },
    test_suite=test_suite,
    tests_require=test_requirements,
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Framework :: Django :: 1.6',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
