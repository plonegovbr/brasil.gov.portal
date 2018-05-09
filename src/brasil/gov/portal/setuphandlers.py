# -*- coding: utf-8 -*-
from brasil.gov.portal.config import SHOW_DEPS
from brasil.gov.portal.config import TINYMCE_JSON_FORMATS
from collective.transmogrifier.transmogrifier import Transmogrifier
from plone import api
from plone.app.dexterity.behaviors import constrains
from Products.CMFCore.WorkflowCore import WorkflowException
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes
from Products.CMFPlone.utils import safe_unicode
from Products.CMFQuickInstallerTool.InstalledProduct import InstalledProduct
from Products.TinyMCE.interfaces.utility import ITinyMCE
from zope.component import getUtility

import json


def setupPortalContent(p):
    """Cria conteudo de exemplo para este portal"""

    # Importa conteudo
    transmogrify = Transmogrifier(p)
    transmogrify('brasil.gov.portal.conteudo')

    # Pagina Inicial
    capa_como_padrao(p)

    # Pasta Assuntos
    configura_assuntos(p)

    # Pasta Acesso a Informacao
    configura_acesso_informacao(p)

    # Pasta de Menu de Relevancia
    configura_menu_relevancia(p)

    # Pasta Servicos
    configura_servicos(p)

    # Pasta Imagens
    configura_imagens(p)

    # Colecao de Ultimas noticias
    configura_ultimas_noticias(p)

    # Destaques
    configura_destaques(p)

    obj_ids = ['acesso-a-informacao', 'assuntos', 'servicos', 'imagens',
               'noticias', 'rodape', 'destaques', 'menu-de-relevancia',
               'links-destaques', 'home', 'contato', 'acessibilidade',
               'acesso-a-sistemas', 'area-de-imprensa', 'rss', 'eventos',
               'videos', 'audios', 'links', 'pastas-com-exemplos-de-pecas']
    publish_content(p, obj_ids)

    # Remove conteúdo default do Doormat
    remove_conteudo_doormat(p)


def capa_como_padrao(portal):
    if not hasattr(portal, 'default_page'):
        portal.manage_addProperty('default_page', 'home', 'string')


def configura_destaques(portal):
    destaques = portal['destaques']
    path = '/'.join(portal['links-destaques'].getPhysicalPath())
    tile_id = '@@em_destaque/432cf6bf0ec1431588b8cf7b1717d300'
    tile = destaques.restrictedTraverse(tile_id)
    catalog = api.portal.get_tool('portal_catalog')
    for b in catalog.searchResults(path=path,
                                   portal_type='Link',
                                   sort_limit=5):
        obj = b.getObject()
        tile.populate_with_object(obj)


def configura_assuntos(portal):
    folder = portal.assuntos
    folder.setLayout('summary_view')


def configura_imagens(portal):
    folder = portal.imagens
    behavior = ISelectableConstrainTypes(folder)
    behavior.setConstrainTypesMode(constrains.ENABLED)
    # Permitimos apenas imagens
    behavior.setImmediatelyAddableTypes(['Image'])
    folder.setLayout('summary_view')


def configura_acesso_informacao(portal):
    folder = portal['acesso-a-informacao']
    folder.setLayout('summary_view')


def configura_menu_relevancia(portal):
    folder = portal['menu-de-relevancia']
    behavior = ISelectableConstrainTypes(folder)
    behavior.setConstrainTypesMode(constrains.ENABLED)
    # Permitimos apenas links
    behavior.setImmediatelyAddableTypes(['Link'])
    folder.setLayout('summary_view')


def configura_servicos(portal):
    folder = portal.servicos
    behavior = ISelectableConstrainTypes(folder)
    behavior.setConstrainTypesMode(constrains.ENABLED)
    # Permitimos apenas links
    behavior.setImmediatelyAddableTypes(['Link'])
    folder.setLayout('summary_view')


def configura_ultimas_noticias(portal):
    oId = 'ultimas-noticias'
    if oId not in portal.objectIds():
        title = u'Últimas Notícias'
        description = u'Últimas notícias publicadas neste site'
        colecao = api.content.create(
            type='Collection',
            container=portal,
            id=oId,
            title=title,
            description=description,
        )
    else:
        colecao = portal[oId]
    colecao.sort_on = u'effective'
    colecao.reverse_sort = True
    # : Query by Type and Review State
    colecao.query = [
        {'i': u'portal_type',
         'o': u'plone.app.querystring.operation.selection.is',
         'v': [u'collective.nitf.content'],
         },
        {'i': u'review_state',
         'o': u'plone.app.querystring.operation.selection.is',
         'v': [u'published'],
         },
    ]
    colecao.setLayout('summary_view')


def publish_content(folder, obj_ids):
    for oId in obj_ids:
        o = folder[oId]
        try:
            review_state = api.content.get_state(o)
        except WorkflowException:
            # Sem informacao de workflow (Imagens, Arquivos)
            continue
        if review_state and (review_state != 'published'):
            api.content.transition(obj=o, transition='publish')
            oIds = o.objectIds()
            if oIds:
                publish_content(o, oIds)


def _instala_pacote(qi, package):
    if package not in qi.objectIds():
        ip = InstalledProduct(package)
        qi._setObject(package, ip)

    p = getattr(qi, package)
    p.update({}, locked=False, hidden=False, **{})


def instala_pacote_portal(context):
    """Marcamos o brasil.gov.portal como instalado no
       portal_quickinstaller, fazendo com que ele apareça no
       painel de controle do portal"""

    # Executado apenas se o estivermos no Profile correto
    if context.readDataFile('brasil.gov.portal.txt') is None:
        return
    qi = api.portal.get_tool('portal_quickinstaller')
    p = 'brasil.gov.portal'
    _instala_pacote(qi, p)
    instala_dependencias(context)


def instala_dependencias(context):
    """Marcamos dependencias importantes como instaladas"""
    if context.readDataFile('brasil.gov.portal.txt') is None:
        return
    qi = api.portal.get_tool('portal_quickinstaller')

    for p in SHOW_DEPS:
        _instala_pacote(qi, p)


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


def remove_conteudo_doormat(context):
    """Remove conteúdo default do Products.Doormat"""
    # presente em Products.Doormat > 0.8
    doormat = getattr(context, 'doormat', None)
    if doormat:
        api.content.delete(doormat)


def set_social_media_settings():
    """Update configuration of sc.social.like package."""
    name = 'sc.social.like.interfaces.ISocialLikeSettings.enabled_portal_types'
    value = (
        'Audio',
        'collective.cover.content',
        'collective.nitf.content',
        'collective.polls.poll',
        'Document',
        'Event',
        'Image',
        'sc.embedder',
    )
    api.portal.set_registry_record(name, value)


def importContent(context):
    """Criamos o conteudo padrao para o site."""
    # Executado apenas se o estivermos no Profile correto
    if context.readDataFile('initcontent.txt') is None:
        return
    site = api.portal.get()
    setupPortalContent(site)
    set_tinymce_formats()


def run_after(context):
    set_social_media_settings()
