# -*- coding: utf-8 -*-
from brasil.gov.portal.logger import logger
from plone import api
from plone.app.viewletmanager.interfaces import IViewletSettingsStorage
from zope.component import queryUtility


STYLES = [
    '++resource++brasil.gov.portal/css/main.css',
    '++resource++brasil.gov.portal/css/main-print.css',
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


def remove_nitf_customizations(setup_tool):
    """Remove collective.nitf customizations."""
    # remove customized view from types tool
    custom_view = 'nitf_custom_view'
    types_tool = api.portal.get_tool('portal_types')
    nitf = types_tool['collective.nitf.content']
    if custom_view in nitf.view_methods:
        nitf.view_methods.remove(custom_view)
    nitf.default_view_fallback = True
    logger.info('collective.nitf types tool customizations removed')

    # set default view on objects using custom view
    # get_valid_objects asserts catalog objects are valid
    from collective.nitf.content import INITF
    from collective.nitf.upgrades.v2000 import get_valid_objects
    import transaction
    results = api.content.find(object_provides=INITF.__identifier__)
    logger.info('Found {0} news articles'.format(len(results)))
    for n, obj in enumerate(get_valid_objects(results), start=1):
        if obj.getLayout() != custom_view:
            continue

        obj.setLayout('view')
        if n % 1000 == 0:
            transaction.commit()
            logger.info('{0} items processed'.format(n))

    transaction.commit()
    logger.info('Done')
