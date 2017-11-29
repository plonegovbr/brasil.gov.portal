# -*- coding: utf-8 -*-
from brasil.gov.portal.logger import logger
from plone import api
from plone.app.viewletmanager.interfaces import IViewletSettingsStorage
from zope.component import queryUtility


STYLES = [
    '++resource++brasil.gov.portal/css/main.css',
    '++resource++brasil.gov.portal/css/main-print.css'
]


def remove_styles(setup_tool):
    """Remvove CSS from registered resources."""
    css_tool = api.portal.get_tool('portal_css')
    for css in STYLES:
        css_tool.unregisterResource(id=css)
        assert css not in css_tool.getResourceIds()
    logger.info('Styles removed')


def show_global_sections(setup_tool):
    """Show back global_sections viewlet."""
    storage = queryUtility(IViewletSettingsStorage)
    manager = u'plone.portalheader'
    for skinname in storage._hidden:
        hidden = storage.getHidden(manager, skinname)
        hidden = (x for x in hidden if x != u'plone.global_sections')
        storage.setHidden(manager, skinname, hidden)
    logger.info('Global Sections Viewlet Showed')
