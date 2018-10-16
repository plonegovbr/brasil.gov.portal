# -*- coding: utf-8 -*-
from brasil.gov.portal.config import TINYMCE_JSON_FORMATS
from plone import api
from Products.CMFPlone.interfaces import INonInstallable
from Products.CMFPlone.utils import safe_unicode
from Products.CMFQuickInstallerTool import interfaces as BBB
from Products.TinyMCE.interfaces.utility import ITinyMCE
from zope.component import getUtility
from zope.interface import implementer

import json


@implementer(BBB.INonInstallable)  # BBB: Plone 4.3
@implementer(INonInstallable)
class NonInstallable(object):  # pragma: no cover

    @staticmethod
    def getNonInstallableProducts():
        """Hide in the add-ons configlet."""
        return [
            u'archetypes.querywidget',
            u'brasil.gov.portal.upgrades.v10900',
            u'brasil.gov.portal.upgrades.v10901',
            u'brasil.gov.portal.upgrades.v10902',
            u'brasil.gov.portal.upgrades.v10903',
            u'brasil.gov.portal.upgrades.v10904',
            u'brasil.gov.portal.upgrades.v10905',
            u'brasil.gov.tiles.upgrades.v2000',
            u'brasil.gov.vcge.at',
            u'brasil.gov.vcge.dx',
            u'brasil.gov.vcge.upgrades.v2000',
            u'collective.googleanalytics',
            u'collective.js.cycle2',
            u'collective.js.galleria',
            u'collective.js.jqueryui',
            u'collective.upload',
            u'collective.z3cform.datagridfield',
            u'collective.z3cform.datetimewidget',
            u'ftw.upgrade',
            u'plone.app.blocks',
            u'plone.app.collection',
            u'plone.app.contenttypes',
            u'plone.app.dexterity',
            u'plone.app.drafts',
            u'plone.app.event',
            u'plone.app.event.at',
            u'plone.app.intid',
            u'plone.app.iterate',
            u'plone.app.jquery',
            u'plone.app.jquerytools',
            u'plone.app.querystring',
            u'plone.app.relationfield',
            u'plone.app.theming',
            u'plone.app.tiles',
            u'plone.app.versioningbehavior',
            u'plone.formwidget.autocomplete',
            u'plone.formwidget.contenttree',
            u'plone.formwidget.datetime',
            u'plone.formwidget.querystring',
            u'plone.formwidget.recurrence',
            u'plone.resource',
            u'plone.session',
            u'plonetheme.classic',
            u'Products.Doormat',  # BBB: remove in 3.0
            u'Products.PloneFormGen',
            u'raptus.autocompletewidget',
        ]

    @staticmethod
    def getNonInstallableProfiles():
        """Hide at site creation."""
        return [
            u'archetypes.querywidget:default',
            u'brasil.gov.agenda.upgrades.v4100:default',
            u'brasil.gov.agenda:default',
            u'brasil.gov.barra.upgrades.v1002:default',
            u'brasil.gov.barra.upgrades.v1010:default',
            u'brasil.gov.barra:default',
            u'brasil.gov.portal.upgrades.v10900:default',
            u'brasil.gov.portal.upgrades.v10901:default',
            u'brasil.gov.portal.upgrades.v10902:default',
            u'brasil.gov.portal.upgrades.v10903:default',
            u'brasil.gov.portal.upgrades.v10904:default',
            u'brasil.gov.portal.upgrades.v10905:default',
            u'brasil.gov.portal:default',
            u'brasil.gov.portal:initcontent',
            u'brasil.gov.portal:uninstall',
            u'brasil.gov.tiles.upgrades.v2000:default',
            u'brasil.gov.tiles:default',
            u'brasil.gov.tiles:uninstall',
            u'brasil.gov.vcge.at:default',
            u'brasil.gov.vcge.dx:default',
            u'brasil.gov.vcge.upgrades.v2000:default',
            u'brasil.gov.vcge:default',
            u'brasil.gov.vcge:uninstall',
            u'collective.cover:default',
            u'collective.js.cycle2:default',
            u'collective.js.galleria:default',
            u'collective.js.jqueryui:default',
            u'collective.nitf:default',
            u'collective.polls:default',
            u'collective.testcaselayer:testing',
            u'collective.upload:default',
            u'collective.z3cform.datagridfield:default',
            u'ftw.upgrade:default',
            u'plone.app.blocks:default',
            u'plone.app.caching:default',
            u'plone.app.contenttypes:default',
            u'plone.app.contenttypes:plone-content',
            u'plone.app.dexterity:default',
            u'plone.app.drafts:default',
            u'plone.app.event.at:default',
            u'plone.app.event:default',
            u'plone.app.iterate:plone.app.iterate',
            u'plone.app.jquerytools:default',
            u'plone.app.openid:default',
            u'plone.app.querystring:default',
            u'plone.app.referenceablebehavior:default',
            u'plone.app.relationfield:default',
            u'plone.app.theming:default',
            u'plone.app.tiles:default',
            u'plone.app.versioningbehavior:default',
            u'plone.formwidget.autocomplete:default',
            u'plone.formwidget.autocomplete:uninstall',
            u'plone.formwidget.contenttree:default',
            u'plone.formwidget.contenttree:uninstall',
            u'plone.formwidget.querystring:default',
            u'plone.formwidget.recurrence:default',
            u'plone.restapi:performance',
            u'plone.session:default',
            u'Products.CMFPlacefulWorkflow:base',
            u'Products.Doormat:default',  # BBB: remove in 3.0
            u'Products.Doormat:uninstall',
            u'Products.PloneFormGen:default',
            u'Products.PloneKeywordManager:uninstall',
            u'Products.RedirectionTool:default',
            u'raptus.autocompletewidget:default',
            u'raptus.autocompletewidget:uninstall',
            u'sc.embedder:default',
            u'sc.microsite:default',
            u'sc.social.like:default',
        ]


def set_tinymce_formats():
    # Baseado em: https://dev.plone.org/ticket/13715
    if getUtility(ITinyMCE).formats is None:
        # Como ainda não existem estilos, posso adicionar diretamente.
        json_formats = safe_unicode(json.dumps(TINYMCE_JSON_FORMATS), 'utf-8')
        getUtility(ITinyMCE).formats = json_formats
    else:
        # Podem já existir estilos adicionados pelo gestor, portanto preciso
        # concatenar com os existentes.
        dict_formats = json.loads(getUtility(ITinyMCE).formats)
        for key in TINYMCE_JSON_FORMATS:
            if key not in dict_formats:
                dict_formats[key] = TINYMCE_JSON_FORMATS[key]

        json_formats = safe_unicode(json.dumps(dict_formats), 'utf-8')
        getUtility(ITinyMCE).formats = json_formats


def set_social_media_settings():
    """Update configuration of sc.social.like package."""
    name = 'sc.social.like.interfaces.ISocialLikeSettings.enabled_portal_types'
    value = (
        'Audio',
        'collective.cover.content',
        'collective.nitf.content',
        'collective.polls.poll',
        'Document',
        'Event',
        'Image',
        'sc.embedder',
    )
    api.portal.set_registry_record(name, value)


def add_content_central_menu():
    """Add Content Central menu option to Folder content type."""
    view = 'centrais-de-conteudo'
    folder_fti = api.portal.get_tool('portal_types')['Folder']
    folder_fti.view_methods += (view,)
    assert view in folder_fti.view_methods  # nosec


def add_results_filter_menu():
    """Add Results Filter menu option to Collection content type."""
    view = 'filtro-de-resultados'
    collection_fti = api.portal.get_tool('portal_types')['Collection']
    collection_fti.view_methods += (view,)
    assert view in collection_fti.view_methods  # nosec


def update_infographic_workflow():
    """Remove workflow from Infographic content type."""
    wftool = api.portal.get_tool('portal_workflow')
    wftool.setChainForPortalTypes(['Infographic'], '')
    assert wftool.getChainForPortalType('Infographic') == ()  # nosec


def run_after(context):
    set_tinymce_formats()
    set_social_media_settings()
    add_content_central_menu()
    add_results_filter_menu()
    update_infographic_workflow()
