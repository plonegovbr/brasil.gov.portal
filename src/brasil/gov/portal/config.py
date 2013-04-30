# -*- coding: utf-8 -*-
from five import grok
from Products.CMFQuickInstallerTool import interfaces as qi_interfaces
from Products.CMFPlone import interfaces as st_interfaces

PROJECTNAME = 'brasil.gov.portal'

REDES = [
    {'id': 'facebook',
     'title': 'Facebook',
     'icon': '++theme++verde/img/icone-facebook.png',
     'url': 'http://facebook.com/%s'},
    {'id': 'twitter',
     'title': 'Twitter',
     'icon': '++theme++verde/img/icone-twitter.png',
     'url': 'https://twitter.com/%s'},
    {'id': 'youtube',
     'title': 'YouTube',
     'icon': '++theme++verde/img/icone-youtube.png',
     'url': 'http://youtube.com/%s'},
    {'id': 'flickr',
     'title': 'Flickr',
     'icon': '++theme++verde/img/icone-flickr.png',
     'url': 'http://flickr.com/%s'},
]


DEPS = [
    'archetypes.querywidget',
    'brasil.gov.barra',
    'brasil.gov.portal.upgrades.v1000',
    'brasil.gov.tiles',
    'collective.cover',
    'collective.googleanalytics',
    'collective.js.galleria',
    'collective.js.jqueryui',
    'collective.nitf',
    'collective.oembed',
    'collective.polls',
    'collective.upload',
    'collective.z3cform.datetimewidget',
    'collective.z3cform.widgets',
    'Marshall',
    'plone.app.blocks',
    'plone.app.collection',
    'plone.app.contenttypes',
    'plone.app.dexterity',
    'plone.app.drafts',
    'plone.app.intid'
    'plone.app.iterate',
    'plone.app.jquery',
    'plone.app.jquerytools',
    'plone.app.intid',
    'plone.app.querystring',
    'plone.app.relationfield',
    'plone.app.theming',
    'plone.app.tiles',
    'plone.app.versioningbehavior',
    'plone.formwidget.autocomplete',
    'plone.formwidget.contenttree',
    'plone.formwidget.querystring',
    'plone.resource',
    'plone.session',
    'plonetheme.classic',
    'Products.PloneFormGen',
    'sc.embedder',
    'sc.social.like',
]

HIDDEN_PROFILES = [
    'archetypes.querywidget:default',
    'brasil.gov.barra:default',
    'brasil.gov.portal:default',
    'brasil.gov.portal:initcontent',
    'brasil.gov.portal.upgrades.v1000:default',
    'brasil.gov.portal:testfixture',
    'brasil.gov.portal:uninstall',
    'brasil.gov.tiles:default',
    'brasil.gov.tiles:uninstall',
    'brasil.gov.vcge:default',
    'brasil.gov.vcge.at:default',
    'brasil.gov.vcge.dx:default',
    'brasil.gov.vcge:uninstall',
    'collective.cover:default',
    'collective.cover:testfixture',
    'collective.cover:uninstall',
    'collective.googleanalytics:default',
    'collective.googleanalytics:upgrade_10a2_10a3',
    'collective.googleanalytics:upgrade_10a4_10b1',
    'collective.googleanalytics:upgrade_10b3_10',
    'collective.js.galleria:default',
    'collective.js.jqueryui:default',
    'collective.nitf:default',
    'collective.oembed:default',
    'collective.polls:default',
    'collective.upload:default',
    'collective.upload:testfixture',
    'collective.upload:uninstall',
    'collective.z3cform.widgets:1_to_2',
    'collective.z3cform.widgets:default',
    'collective.z3cform.widgets:uninstall',
    'plone.app.blocks:default',
    'plone.app.contenttypes:default',
    'plone.app.contenttypes:plone-content',
    'plone.app.dexterity:default',
    'plone.app.drafts:default',
    'plone.app.iterate:plone.app.iterate',
    'plone.app.openid:default',
    'plone.app.querystring:default',
    'plone.app.relationfield:default',
    'plone.app.theming:default',
    'plone.app.tiles:default',
    'plone.app.versioningbehavior:default',
    'plone.formwidget.autocomplete:default',
    'plone.formwidget.contenttree:default',
    'plone.formwidget.querystring:default',
    'Products.PloneFormGen:default',
    'raptus.autocompletewidget:default',
    'raptus.autocompletewidget:uninstall',
    'sc.embedder:default',
    'sc.embedder:uninstall',
    'sc.social.like:default',
    'sc.social.like:to2000',
    'sc.social.like:uninstall',
]


class HiddenProducts(grok.GlobalUtility):

    grok.implements(qi_interfaces.INonInstallable)
    grok.provides(qi_interfaces.INonInstallable)
    grok.name(PROJECTNAME)

    def getNonInstallableProducts(self):
        products = []
        products = [p for p in DEPS]
        return products


class HiddenProfiles(grok.GlobalUtility):

    grok.implements(st_interfaces.INonInstallable)
    grok.provides(st_interfaces.INonInstallable)
    grok.name(PROJECTNAME)

    def getNonInstallableProfiles(self):
        return HIDDEN_PROFILES
