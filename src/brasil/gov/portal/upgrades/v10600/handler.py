# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from brasil.gov.portal.config import PROJECTNAME
from brasil.gov.portal.config import TINYMCE_JSON_FORMATS
from brasil.gov.portal.setuphandlers import set_tinymce_formats
from plone import api
from zope.component import getUtility

import logging


logger = logging.getLogger(PROJECTNAME)


def install_product(context):
    """Atualiza perfil para versao 10600"""
    qi = api.portal.get_tool('portal_quickinstaller')
    if not qi.isProductInstalled('brasil.gov.portlets'):
        logger.info('Instalando produto brasil.gov.portlets')
        qi.installProduct('brasil.gov.portlets')
    logger.info('Atualizado para versao 10600')


def set_some_tiny_formats(context):
    set_tinymce_formats(context)

    # Novas regras foram adicionadas nos arquivos css.
    getToolByName(context, 'portal_css').cookResources()
