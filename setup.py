import setuptools

setuptools.setup(
    name="djangocms-helper",
    version="0.1.0",
    url="https://github.com/nephila/djangocms-helper",

    author="Iacopo Spalletti",
    author_email="i.spalletti@nephila.it",

    description="Helpers for django CMS plugin development",
    long_description=open('README.rst').read(),
    license='GPLv2+',

    packages=setuptools.find_packages(),

    install_requires=[
        'django-cms>3',
        'docopt',
        'dj-database-url'
    ],
    entry_points={
        'console_scripts': [
            'djangocms-helper = djangocms_helper.main:main',
        ]
    },

    classifiers=[
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)