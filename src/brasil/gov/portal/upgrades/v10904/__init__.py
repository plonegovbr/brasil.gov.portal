# -*- coding: utf-8 -*-
from brasil.gov.portal.logger import logger
from plone import api


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
