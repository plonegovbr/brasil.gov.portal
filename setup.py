# -*- coding: utf-8 -*-

from setuptools import find_packages
from setuptools import setup

version = '1.1.3'
long_description = (
    open('README.rst').read() + '\n' +
    open('CONTRIBUTORS.rst').read() + '\n' +
    open('CHANGES.rst').read()
)

setup(
    name='brasil.gov.portal',
    version=version,
    description="Implementação Modelo da Identidade Digital de Governo",
    long_description=long_description,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
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
    keywords='plone .gov.br identidade_digital egov',
    author='PloneGov.BR',
    author_email='gov@plone.org.br',
    url='https://github.com/plonegovbr/brasil.gov.portal',
    license='GPLv2',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['brasil', 'brasil.gov'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'AccessControl',
        'Acquisition',
        'brasil.gov.agenda',
        'brasil.gov.barra',
        'brasil.gov.portlets',
        'brasil.gov.temas',
        'brasil.gov.tiles',
        'brasil.gov.vcge',
        'collective.cover > 1.0a8',
        'collective.jsonmigrator',
        'collective.nitf',
        'collective.polls',
        'collective.upload',
        'five.grok',
        'five.pt',
        'plone.api > 1.1.0',
        'plone.app.contenttypes',
        'plone.app.controlpanel',
        'plone.app.dexterity',
        'plone.app.layout',
        'plone.app.portlets',
        'plone.app.search',
        'plone.app.theming',
        'plone.app.transmogrifier',
        'plone.app.upgrade',
        'plone.contentrules',
        'plone.dexterity',
        'plone.directives.form',
        'plone.memoize',
        'plone.namedfile',
        'plone.supermodel',
        'plone.tiles',
        'Products.CMFCore',
        'Products.CMFDefault',
        'Products.CMFPlone',
        'Products.Doormat>0.7',
        'Products.GenericSetup',
        'Products.PloneFormGen',
        'Products.PloneHotfix20150910',
        'sc.contentrules.groupbydate',
        'sc.contentrules.layout',
        'sc.contentrules.metadata',
        'sc.embedder',
        'sc.social.like',
        'setuptools',
        'transmogrify.dexterity',
        'z3c.unconfigure',
        'zope.component',
        'zope.interface',
        'zope.schema',
    ],
    extras_require={
        'test': [
            'plone.app.robotframework',
            'plone.app.testing [robot]',
            'plone.browserlayer',
            'plone.registry',
            'plone.testing',
            'plonetheme.sunburst',
            'robotframework-wavelibrary',
            'robotsuite',
        ]
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
