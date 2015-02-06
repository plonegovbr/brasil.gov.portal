# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from Products.TinyMCE.interfaces.utility import ITinyMCE
from brasil.gov.portal.config import PROJECTNAME
from brasil.gov.portal.config import TINYMCE_JSON_FORMATS
from plone import api
from zope.component import getUtility

import json
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
    # Baseado em: https://dev.plone.org/ticket/13715
    if getUtility(ITinyMCE).formats is None:
        # Como ainda não existem estilos, posso adicionar diretamente.
        json_formats = safe_unicode(json.dumps(TINYMCE_JSON_FORMATS), 'utf-8')
        getUtility(ITinyMCE).formats = json_formats
    else:
        # Podem já existir estilos adicionados pelo gestor, portanto preciso
        # concatenar com os existentes.
        dict_formats = json.loads(getUtility(ITinyMCE).formats)
        for key in TINYMCE_JSON_FORMATS:
            if key not in dict_formats:
                dict_formats[key] = TINYMCE_JSON_FORMATS[key]

        json_formats = safe_unicode(json.dumps(dict_formats), 'utf-8')
        getUtility(ITinyMCE).formats = json_formats

    # Novas regras foram adicionadas nos arquivos css.
    getToolByName(context, 'portal_css').cookResources()
