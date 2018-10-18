# -*- coding: utf-8 -*-

from setuptools import find_packages
from setuptools import setup

version = '1.5.4'
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
        # Com a atualização para collective.nitf >= 2.1b2, a versão compatível
        # do brasil.gov.tiles passa a ser essa.
        'brasil.gov.tiles >= 1.4b1',
        'brasil.gov.vcge',
        # Versão mínima requerida por brasil.gov.tiles.
        'collective.cover > 1.3b1',
        'collective.fingerpointing',
        'collective.jsonmigrator',
        'collective.lazysizes',
        'collective.liveblog',
        'collective.monkeypatcher',
        # Imports como
        # "from collective.nitf.browser import NITFBylineViewlet as CollectiveNITFBylineViewlet"
        # Só a partir de 2.1b2, e get_valid_objects usado em upgradeStep, 2.1b4.
        'collective.nitf >= 2.1b4',
        'collective.polls',
        'collective.upload',
        'collective.z3cform.widgets',  # TODO: remove on release 2.0
        'five.grok',
        'five.pt',
        'lxml',
        'plone.api > 1.1.0',
        # Passo a referenciar visões novas adicionadas nesse marco:
        # https://github.com/plone/plone.app.contenttypes/blob/1.1.1/plone/app/contenttypes/upgrades.py#L153
        'plone.app.contenttypes >= 1.1.1',
        'plone.app.controlpanel',
        'plone.app.dexterity',
        'plone.app.layout',
        'plone.app.portlets',
        'plone.app.search',
        'plone.app.theming',
        'plone.app.transmogrifier',
        'plone.app.upgrade',
        'plone.browserlayer',
        'plone.contentrules',
        'plone.dexterity',
        'plone.directives.form',
        'plone.indexer',
        'plone.memoize',
        'plone.namedfile',
        'plone.registry',
        'plone.restapi',
        'plone.supermodel',
        'plone.tiles',
        'Products.CMFCore',
        'Products.CMFDefault',
        'Products.CMFPlone',
        'Products.Doormat>0.7',
        'Products.GenericSetup',
        'Products.PloneFormGen',
        'Products.RedirectionTool',
        'Products.TinyMCE',
        'sc.contentrules.groupbydate',
        'sc.contentrules.layout',
        'sc.contentrules.metadata',
        'sc.embedder',
        'sc.photogallery',
        'sc.social.like',
        'setuptools',
        'transmogrify.dexterity',
        'z3c.jbot',
        'z3c.unconfigure',
        'zope.component',
        'zope.event',
        'zope.interface',
        'zope.lifecycleevent',
        'zope.schema',
        'plone4.csrffixes',
    ],
    extras_require={
        'test': [
            'brasil.gov.agenda',
            'collective.cover',
            'plone.app.robotframework[debug]',
            'plone.app.testing [robot]',
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
