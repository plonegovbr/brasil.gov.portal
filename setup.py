# -*- coding: utf-8 -*-

from setuptools import find_packages
from setuptools import setup

import os

version = '1.0'
long_description = open("README.rst").read() + "\n" + \
    open(os.path.join("docs", "INSTALL.rst")).read() + "\n" + \
    open(os.path.join("docs", "CREDITS.rst")).read() + "\n" + \
    open(os.path.join("docs", "HISTORY.rst")).read()

setup(
    name='brasil.gov.portal',
    version=version,
    description="Policy package for the Portal Modelo.",
    long_description=long_description,
    classifiers=[
        "Development Status :: 1 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Multimedia",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='',
    author='',
    author_email='',
    url='',
    license='GPLv2',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['brasil', 'brasil.gov'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        #'brasil.gov.temas',
        'collective.cover',
        'collective.googleanalytics',
        'collective.nitf',
        'collective.polls',
        'collective.upload',
        'five.pt',
        'Pillow',
        #'plone.app.contenttypes',  # FIXME: rising AttributeError: 'module' object has no attribute 'HAVE_BLOBS'
        'plone.app.upgrade',
        'Products.CMFPlone',
        'sc.contentrules.groupbydate',
        'sc.contentrules.layout',
        'sc.contentrules.metadata',
        'sc.embedder',
        'sc.social.like',
        'setuptools',
    ],
    extras_require={
        'test': [
            'plone.app.testing',
        ]
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
