# -*- coding: utf-8 -*-
from brasil.gov.portal.logger import logger
from brasil.gov.portal.setuphandlers import set_tinymce_formats
from brasil.gov.portal.upgrades import csscookresources
from plone import api
from plone.app.upgrade.utils import loadMigrationProfile


def install_product(context):
    """Instala brasil.gov.portlets"""
    qi = api.portal.get_tool('portal_quickinstaller')
    if not qi.isProductInstalled('brasil.gov.portlets'):
        logger.info('Instalando produto brasil.gov.portlets')
        qi.installProduct('brasil.gov.portlets')
    logger.info('brasil.gov.portlets instalado')


def set_some_tiny_formats(context):
    set_tinymce_formats()

    # Novas regras foram adicionadas nos arquivos css.
    csscookresources()


def apply_profile(context):
    """Atualiza perfil para versao 10600, para registrar novas viewlets."""
    profile = 'profile-brasil.gov.portal.upgrades.v10600:default'
    loadMigrationProfile(context, profile)
    logger.info('Atualizado para versao 10600')


def disable_action_site_actions_plone_setup(context):
    site_actions = api.portal.get_tool('portal_actions').site_actions
    site_actions.plone_setup.visible = False
    logger.info('Action de Configuracoes do Site desabilitada')
