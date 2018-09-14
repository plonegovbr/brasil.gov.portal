# -*- coding: utf-8 -*-
from brasil.gov.portal.logger import logger
from plone import api
from plone.app.upgrade.utils import loadMigrationProfile


def install_redirection_tool(setup_tool):
    """Install Products.RedirectionTool."""
    addon = 'RedirectionTool'
    qi = api.portal.get_tool('portal_quickinstaller')
    if not qi.isProductInstalled(addon):
        qi.installProduct(addon)
        logger.info('Products.RedirectionTool was installed')


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


def apply_profile(setup_tool):
    """Atualiza profile para versao 10803."""
    profile = 'profile-brasil.gov.portal.upgrades.v10803:default'
    loadMigrationProfile(setup_tool, profile)
    logger.info('Atualizado para versao 10803')
