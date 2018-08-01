# -*- coding: utf-8 -*-

from setuptools import find_packages
from setuptools import setup

version = '2.0a6.dev0'
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
        "Development Status :: 2 - Pre-Alpha",
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
        # Com a atualização para collective.nitf >= 2.1b2, a versão compatível
        # do brasil.gov.tiles passa a ser essa.
        'brasil.gov.tiles >= 1.4b1',
        'brasil.gov.vcge [dexterity]',
        # Versão mínima requerida por brasil.gov.tiles.
        'collective.cover > 1.3b1',
        'collective.fingerpointing',
        'collective.jsonmigrator',
        'collective.lazysizes',
        'collective.liveblog',
        # Imports como
        # "from collective.nitf.browser import NITFBylineViewlet as CollectiveNITFBylineViewlet"
        # Só a partir dessa versão.
        'collective.nitf >= 2.1b2',
        'collective.polls',
        'collective.upload',
        'five.pt',
        'lxml',
        'plone.api > 1.1.0',
        # Passo a referenciar visões novas adicionadas nesse marco:
        # https://github.com/plone/plone.app.contenttypes/blob/1.1.1/plone/app/contenttypes/upgrades.py#L153
        'plone.app.contenttypes >= 1.1.1',
        'plone.app.controlpanel',
        'plone.app.dexterity',
        'plone.app.layout',
        'plone.app.search',
        'plone.app.theming',
        'plone.contentrules',
        'plone.dexterity',
        'plone.directives.form',
        'plone.indexer',
        'plone.memoize',
        'plone.namedfile',
        'plone.portlets',
        'plone.protect >= 3.0.26',
        'plone.restapi',
        'plone.supermodel',
        'Products.CMFCore',
        'Products.CMFDefault',
        'Products.CMFPlone',
        'Products.Doormat>0.7',
        'Products.GenericSetup',
        'Products.PloneFormGen',
        'Products.PloneKeywordManager',
        'Products.RedirectionTool',
        'Products.TinyMCE',
        'sc.contentrules.groupbydate',
        'sc.contentrules.layout',
        'sc.contentrules.metadata',
        'sc.embedder',
        'sc.photogallery',
        'sc.social.like',
        'setuptools',
        'six',
        'webcouturier.dropdownmenu',
        'z3c.jbot',
        'z3c.unconfigure',
        'zope.component',
        'zope.interface',
        'zope.lifecycleevent',
        'zope.schema',
    ],
    extras_require={
        'migration': [
            'collective.jsonmigrator',
            'collective.transmogrifier',
            'plone.app.transmogrifier',
            'transmogrify.dexterity',
        ],
        'test': [
            'brasil.gov.agenda',
            'collective.cover',
            'plone.app.robotframework[debug]',
            'plone.app.testing [robot]',
            'plone.browserlayer',
            'plone.registry',
            'plone.testing',
            'plonetheme.sunburst',
            'Products.GenericSetup',
            'robotframework-wavelibrary',
            'robotsuite',
            'transaction',
            'zope.publisher',
            'zope.viewlet',
        ]
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
