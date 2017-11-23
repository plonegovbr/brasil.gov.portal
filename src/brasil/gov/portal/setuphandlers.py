# -*- coding: utf-8 -*-
from brasil.gov.portal.config import TINYMCE_JSON_FORMATS
from plone import api
from Products.CMFPlone.utils import safe_unicode
from Products.TinyMCE.interfaces.utility import ITinyMCE
from zope.component import getUtility

import json


def set_tinymce_formats():
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


def remove_doormat_content(portal):
    """Remove conteúdo default do Products.Doormat."""
    # presente em Products.Doormat > 0.8
    doormat = 'doormat'
    if doormat in portal.objectIds():
        api.content.delete(portal[doormat])


def run_after(context):
    portal = api.portal.get()
    set_tinymce_formats()
    remove_doormat_content(portal)
