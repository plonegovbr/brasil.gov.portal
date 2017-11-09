# -*- coding: utf-8 -*-
from brasil.gov.portal.logger import logger
from plone import api


def install_redirection_tool(setup_tool):
    """Install Products.RedirectionTool."""
    redirection_tool = 'RedirectionTool'
    qi = api.portal.get_tool('portal_quickinstaller')
    if not qi.isProductInstalled(redirection_tool):
        qi.installProduct(redirection_tool)
        logger.info('Products.RedirectionTool was installed')
