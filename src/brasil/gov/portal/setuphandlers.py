# -*- coding:utf-8 -*-
from plone.app.dexterity.behaviors import constrains
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes
from Products.CMFPlone.utils import _createObjectByType
from zope.event import notify
from zope.lifecycleevent import ObjectAddedEvent
import json


def setupPortalContent(p):
    ''' Cria conteudo de exemplo para este portal
    '''
    existing = p.keys()
    language = 'pt_BR'

    # Registra os tiles disponiveis

    # Pagina Inicial
    # TODO -- Cover
    if 'front-page' not in existing:
        cria_capa(p)

    # Pasta Assuntos
    if 'assuntos' not in existing:
        cria_assuntos(p)

    # Pasta Sobre
    if 'sobre' not in existing:
        cria_sobre(p)

    # Rodape do site
    if 'rodape' not in existing:
        cria_rodape(p)

    # Pasta Servicos
    if 'servicos' not in existing:
        cria_servicos(p)

    # Pasta Imagens
    if 'imagens' not in existing:
        cria_imagens(p)

    # Colecao de Ultimas noticias
    if 'noticias' not in existing:
        cria_ultimas_noticias(p)

    # Destaques
    # TODO -- Cover
    if 'destaques' not in existing:
        cria_destaques(p)

    wftool = getToolByName(p, "portal_workflow")
    obj_ids = ['sobre', 'assuntos', 'servicos', 'imagens',
               'noticias', 'rodape', 'destaques']
    publish_content(wftool, p, obj_ids)


def cria_capa(portal):
    #title = u'Página Inicial'
    #description = u''

    #_createObjectByType('collective.cover.content',
    #                    portal, id='front-page',
    #                    title=title, description=description)
    #capa = portal['front-page']
    pass


def cria_destaques(portal):
    title = u'Destaques do Portal'
    description = u'Listagem de destaques do portal'
    _createObjectByType('collective.cover.content',
                        portal, id='destaques',
                        title=title, description=description)
    destaques = portal['destaques']
    destaques.template_layout = 'Destaques'
    notify(ObjectAddedEvent(destaques))
    cover_data = json.loads(destaques.cover_layout)
    tile_id = cover_data[0]['children'][0]['children'][0]['id']
    tile = destaques.restrictedTraverse(str('@@em_destaque/%s' % tile_id))
    for b in portal.portal_catalog.searchResults(portal_type='Link',
                                                 sort_limit=5):
        obj = b.getObject()
        tile.populate_with_object(obj)


def cria_rodape(portal):
    title = u'Rodapé'
    description = u'Rodapé do Portal'

    portal.portal_types['Doormat'].global_allow = True

    _createObjectByType('Doormat',
                        portal, id='rodape',
                        title=title, description=description)

    portal.portal_types['Doormat'].global_allow = False
    rodape = portal['rodape']
    rodape.setExcludeFromNav(True)
    rodape.setShowTitle(False)
    colunas = [
        ('coluna-1', u'Primeira coluna'),
        ('coluna-2', u'Segunda coluna'),
        ('coluna-3', u'Terceira coluna'),
        ('coluna-4', u'Quarta coluna'),
    ]
    for col_id, col_title in colunas:
        _createObjectByType('DoormatColumn',
                            rodape, id=col_id,
                            title=col_title,
                            description=col_title)
        coluna = rodape[col_id]
        coluna.setExcludeFromNav(True)
        coluna.setShowTitle(False)

    secoes = [
        ('coluna-1', 'assuntos', u'Assuntos'),
        ('coluna-2', 'sobre', u'Sobre'),
        ('coluna-3', 'falem', u'Falem Conosco'),
        ('coluna-4', 'redes-sociais', u'Redes Sociais'),
        ('coluna-4', 'mapa', u'Mapa do Site'),
        ('coluna-4', 'rss', u'RSS'),
    ]
    for col_id, secao_id, secao_title in secoes:
        _createObjectByType('DoormatSection',
                            rodape[col_id],
                            id=secao_id,
                            title=secao_title,
                            description=secao_title)
        secao = rodape[col_id][secao_id]
        secao.setExcludeFromNav(True)
        secao.setShowTitle(True)

    assuntos = portal['assuntos']
    assuntos_doormat = rodape['coluna-1']['assuntos']
    for assunto in assuntos.objectIds():
        obj = assuntos[assunto]
        _createObjectByType('Link',
                            assuntos_doormat,
                            id=obj.getId(),
                            title=obj.Title(),
                            description=obj.Description())
        link = assuntos_doormat[obj.getId()]
        link.remoteUrl = '${portal_url}/assuntos/%s' % obj.getId()
        link.reindexObject()

    sobre = portal['sobre']
    sobre_doormat = rodape['coluna-2']['sobre']
    for item in sobre.objectIds():
        obj = sobre[item]
        _createObjectByType('Link',
                            sobre_doormat,
                            id=obj.getId(),
                            title=obj.Title(),
                            description=obj.Description())
        link = sobre_doormat[obj.getId()]
        link.remoteUrl = '${portal_url}/sobre/%s' % obj.getId()
        link.reindexObject()

    items = [
        ('coluna-3/falem', 'contact-info',
         u'Formulário de Contato', '${portal_url}/contact-info'),
        ('coluna-4/redes-sociais', 'twitter',
         u'Twitter', 'http://twitter.com/portalbrasil'),
        ('coluna-4/redes-sociais', 'youtube',
         u'YouTube', 'http://www.youtube.com/canalportalbrasil'),
    ]
    for path, item_id, item_title, item_url in items:
        secao = rodape.unrestrictedTraverse(path)
        _createObjectByType('Link',
                            secao,
                            id=item_id,
                            title=item_title,
                            description=item_title)
        link = secao[item_id]
        link.remoteUrl = item_url
        link.reindexObject()


def cria_assuntos(portal):
    title = 'Assuntos'
    description = u'Assuntos deste Órgão'

    _createObjectByType('Folder', portal, id='assuntos',
                        title=title, description=description)

    folder = portal.assuntos
    folder.setOrdering('unordered')
    #folder.setConstrainTypesMode(1)
    # Permitimos preferencialmente outras pastas
    #folder.setImmediatelyAddableTypes(['Folder'])
    #folder.setLayout('folder_summary_view')
    #folder.unmarkCreationFlag()
    #folder.setLanguage(language)


def cria_imagens(portal):
    title = 'Imagens'
    description = u'Banco de Imagens'

    _createObjectByType('Folder', portal, id='imagens',
                        title=title, description=description)

    folder = portal.imagens
    folder.setOrdering('unordered')
    behavior = ISelectableConstrainTypes(folder)
    behavior.setConstrainTypesMode(constrains.ENABLED)
    # Permitimos apenas imagens
    behavior.setImmediatelyAddableTypes(['Image'])
    folder.setLayout('folder_summary_view')


def cria_sobre(portal):
    title = 'Sobre'
    description = u'Conheça este órgão'

    _createObjectByType('Folder', portal, id='sobre',
                        title=title, description=description)

    folder = portal.sobre
    folder.setOrdering('unordered')
    #folder.setConstrainTypesMode(1)
    # Permitimos preferencialmente outras pastas
    #folder.setImmediatelyAddableTypes(['Folder'])
    #folder.setLayout('folder_summary_view')
    #folder.unmarkCreationFlag()
    #folder.setLanguage(language)
    # Criar algumas paginas


def cria_servicos(portal):
    title = 'Serviços'
    description = u'Serviços deste órgão'

    _createObjectByType('Folder', portal, id='servicos',
                        title=title, description=description)

    folder = portal.servicos
    behavior = ISelectableConstrainTypes(folder)
    behavior.setConstrainTypesMode(constrains.ENABLED)
    # Permitimos apenas links
    behavior.setImmediatelyAddableTypes(['Link'])
    folder.setLayout('folder_summary_view')
    # Criar links
    links = [
        ('ouvidoria', 'Ouvidoria', '${portal_url}/ouvidoria'),
        ('central-servicos', 'Central de Serviços', '${portal_url}/servicos'),
    ]
    for link in links:
        id, title, url = link
        _createObjectByType('Link', folder, id=id,
                            title=title, url=url)
    publish_content(None, folder, [i[0] for i in links])
    return folder.getId()


def cria_ultimas_noticias(portal):
    oId = 'noticias'
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
#    uid = IUUID(colecao)
#    id_coluna = '++contextportlets++plone.leftcolumn'
#    mapping = portal.restrictedTraverse(id_coluna)
#    # Nosso portlet e o primeiro
#    assignment = mapping[0]
#    assignment.text = u'''
#    <a class="internal-link" href="resolveuid/%s"
#       target="_self" title="">Últimas Notícias</a>''' % uid


def publish_content(wftool, folder, obj_ids):
    if not wftool:
        wftool = getToolByName(folder, "portal_workflow")
    for oId in obj_ids:
        o = folder[oId]
        if wftool.getInfoFor(o, 'review_state') != 'published':
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
