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


def install_restapi(setup_tool):
    """Install plone.restapi."""
    addon = 'plone.restapi'
    qi = api.portal.get_tool('portal_quickinstaller')
    if not qi.isProductInstalled(addon):
        qi.installProduct(addon)
        logger.info(addon + ' was installed')


def uninstall_widgets(setup_tool):
    """Uninstall collective.z3cform.widgets."""
    from collective.z3cform.widgets.interfaces import ILayer
    from plone.browserlayer import utils
    addon = 'collective.z3cform.widgets'
    qi = api.portal.get_tool('portal_quickinstaller')
    if qi.isProductInstalled(addon):
        with api.env.adopt_roles(['Manager']):
            qi.uninstallProducts([addon])
        logger.info(addon + ' was uninstalled')
        # product must not be installable
        assert not qi.isProductInstallable(addon)

    if ILayer in utils.registered_layers():
        utils.unregister_layer(name=addon)
        logger.info(addon + ' browser layer was removed')
