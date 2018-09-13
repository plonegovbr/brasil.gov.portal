# -*- coding: utf-8 -*-
from brasil.gov.portal.logger import logger
from plone import api


def install_dropdownmenu(setup_tool):
    """Install webcouturier.dropdownmenu."""
    addon = 'webcouturier.dropdownmenu'
    qi = api.portal.get_tool('portal_quickinstaller')
    if not qi.isProductInstalled(addon):
        qi.installProduct(addon)
        logger.info(addon + ' was installed')
