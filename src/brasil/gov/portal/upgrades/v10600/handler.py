# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from brasil.gov.portal.config import PROJECTNAME

import logging

logger = logging.getLogger(PROJECTNAME)


def install_product(context):
    """Atualiza perfil para versao 10600"""
    portal = getToolByName(context, 'portal_url').getPortalObject()
    qi = getToolByName(portal, 'portal_quickinstaller')
    if not qi.isProductInstalled('brasil.gov.portlets'):
        logger.info('Instalando produto brasil.gov.portlets')
        qi.installProduct('brasil.gov.portlets')
    logger.info('Atualizado para versao 10600')
