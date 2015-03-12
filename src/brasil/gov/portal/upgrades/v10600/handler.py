# -*- coding: utf-8 -*-
from brasil.gov.portal.config import PROJECTNAME
from plone import api

import logging

logger = logging.getLogger(PROJECTNAME)


def install_product(context):
    """Atualiza perfil para versao 10600"""
    qi = api.portal.get_tool('portal_quickinstaller')
    if not qi.isProductInstalled('brasil.gov.portlets'):
        logger.info('Instalando produto brasil.gov.portlets')
        qi.installProduct('brasil.gov.portlets')
    logger.info('Atualizado para versao 10600')
