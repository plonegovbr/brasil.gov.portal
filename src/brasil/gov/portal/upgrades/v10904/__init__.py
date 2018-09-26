# -*- coding: utf-8 -*-
from brasil.gov.portal.logger import logger
from plone import api


SCRIPTS = [
    '++resource++jquery.cookie.js',
    '++resource++contraste.js',
    '++resource++brasil.gov.portal/js/main.js',
]


def deprecate_resource_registries(setup_tool):
    """Deprecate resource registries."""
    js_tool = api.portal.get_tool('portal_javascripts')
    for js in SCRIPTS:
        js_tool.unregisterResource(id=js)
        assert js not in js_tool.getResourceIds()  # nosec
        logger.info('Scripts removed')


def uninstall_doormat(setup_tool):
    """Uninstall Products.Doormat.
    The add-on removes itself all related content at uninstall so we
    don't need to do so here.
    """
    addon = 'Doormat'
    qi = api.portal.get_tool('portal_quickinstaller')
    if qi.isProductInstalled(addon):
        qi.uninstallProducts([addon])
        logger.info(addon + ' was uninstalled')
