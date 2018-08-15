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
    """Remove CSS from registered resources."""
    css_tool = api.portal.get_tool('portal_css')
    for css in STYLES:
        css_tool.unregisterResource(id=css)
        assert css not in css_tool.getResourceIds()  # nosec
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
        view_methods = list(nitf.view_methods)
        view_methods.remove(custom_view)
        nitf.view_methods = tuple(view_methods)
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


def search_for_embedder(setup_tool):
    """Remove sc.embedder from types_not_searched."""
    settings = api.portal.get_tool('portal_properties').site_properties
    if 'sc.embedder' in settings.types_not_searched:
        types_not_searched = list(settings.types_not_searched)
        types_not_searched.remove('sc.embedder')
        settings.types_not_searched = tuple(types_not_searched)
        logger.info('Search for sc.embedder objects is enabled')


def update_galeria_image_sizes(setup_tool):
    """Update galeria de fotos image sizes."""
    settings = api.portal.get_tool('portal_properties').imaging_properties
    allowed_sizes = set(settings.allowed_sizes)
    allowed_sizes -= frozenset([
        u'galeria_de_foto_thumb 87:49', u'galeria_de_foto_view 748:513'])
    allowed_sizes |= frozenset([u'galeria_de_foto_view 1150:650'])
    settings.allowed_sizes = tuple(allowed_sizes)
    logger.info('Galeria de fotos image sizes updated.')


def install_keyword_manager(setup_tool):
    """Install Products.PloneKeywordManager."""
    addon = 'PloneKeywordManager'
    qi = api.portal.get_tool('portal_quickinstaller')
    if not qi.isProductInstalled(addon):
        qi.installProduct(addon)
        logger.info(addon + ' was installed')
