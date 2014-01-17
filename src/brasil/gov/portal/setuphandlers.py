# -*- coding:utf-8 -*-
from plone.app.dexterity.behaviors import constrains
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes
from Products.CMFPlone.utils import _createObjectByType
from collective.transmogrifier.transmogrifier import Transmogrifier


def setupPortalContent(p):
    ''' Cria conteudo de exemplo para este portal
    '''
    # Importa conteudo
    transmogrify = Transmogrifier(p)
    transmogrify("brasil.gov.portal.conteudo")

    # Pagina Inicial
    capa_como_padrao(p)

    # Pasta Assuntos
    configura_assuntos(p)

    # Pasta Sobre
    configura_sobre(p)

    # Pasta de Menu de Apoio
    configura_menu_apoio(p)

    # Pasta Servicos
    configura_servicos(p)

    # Pasta Imagens
    configura_imagens(p)

    # Colecao de Ultimas noticias
    configura_ultimas_noticias(p)

    # Destaques
    configura_destaques(p)

    wftool = getToolByName(p, "portal_workflow")
    obj_ids = ['sobre', 'assuntos', 'servicos', 'imagens',
               'noticias', 'rodape', 'destaques', 'menu-de-apoio',
               'links-destaques', 'home', 'contato', 'acessibilidade',
               'acesso-a-sistemas', 'area-imprensa', 'rss', 'eventos',
               'videos', 'audios', 'links', 'pastas-com-exemplos-de-pecas']
    publish_content(wftool, p, obj_ids)


def capa_como_padrao(portal):
    if not hasattr(portal, 'default_page'):
        portal.manage_addProperty('default_page', 'home', 'string')


def configura_destaques(portal):
    destaques = portal['destaques']
    path = '/'.join(portal['links-destaques'].getPhysicalPath())
    tile_id = '@@em_destaque/432cf6bf0ec1431588b8cf7b1717d300'
    tile = destaques.restrictedTraverse(tile_id)
    for b in portal.portal_catalog.searchResults(path=path,
                                                 portal_type='Link',
                                                 sort_limit=5):
        obj = b.getObject()
        tile.populate_with_object(obj)


def configura_assuntos(portal):
    folder = portal.assuntos
    folder.setOrdering('unordered')
    folder.setLayout('folder_summary_view')


def configura_imagens(portal):
    folder = portal.imagens
    folder.setOrdering('unordered')
    behavior = ISelectableConstrainTypes(folder)
    behavior.setConstrainTypesMode(constrains.ENABLED)
    # Permitimos apenas imagens
    behavior.setImmediatelyAddableTypes(['Image'])
    folder.setLayout('folder_summary_view')


def configura_sobre(portal):
    folder = portal.sobre
    folder.setOrdering('unordered')
    folder.setLayout('folder_summary_view')


def configura_menu_apoio(portal):
    folder = portal['menu-de-apoio']
    behavior = ISelectableConstrainTypes(folder)
    behavior.setConstrainTypesMode(constrains.ENABLED)
    # Permitimos apenas links
    behavior.setImmediatelyAddableTypes(['Link'])
    folder.setLayout('folder_summary_view')


def configura_servicos(portal):
    folder = portal.servicos
    behavior = ISelectableConstrainTypes(folder)
    behavior.setConstrainTypesMode(constrains.ENABLED)
    # Permitimos apenas links
    behavior.setImmediatelyAddableTypes(['Link'])
    folder.setLayout('folder_summary_view')


def configura_ultimas_noticias(portal):
    oId = 'noticias'
    if not oId in portal.objectIds():
        title = u'Últimas Notícias'
        description = u'Últimas notícias publicadas neste site'
        _createObjectByType('Collection', portal,
                            id=oId, title=title,
                            description=description)
    colecao = portal[oId]
    colecao.sort_on = u'effective'
    colecao.reverse_sort = True
    #: Query by Type and Review State
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


def publish_content(wftool, folder, obj_ids):
    if not wftool:
        wftool = getToolByName(folder, "portal_workflow")
    for oId in obj_ids:
        o = folder[oId]
        review_state = wftool.getInfoFor(o, 'review_state', None)
        if review_state and (review_state != 'published'):
            wftool.doActionFor(o, 'publish')
            oIds = o.objectIds()
            if oIds:
                publish_content(wftool, o, oIds)


def importContent(context):
    ''' Criamos o conteudo padrao para o site
    '''
    # Executado apenas se o estivermos no Profile correto
    if context.readDataFile('initcontent.txt') is None:
        return
    site = context.getSite()
    setupPortalContent(site)
