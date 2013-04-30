# -*- coding:utf-8 -*-
from plone.app.dexterity.behaviors import constrains
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes
from Products.CMFPlone.utils import _createObjectByType
#from plone.uuid.interfaces import IUUID


def setupPortalContent(p):
    ''' Cria conteudo de exemplo para este portal
    '''
    existing = p.keys()
    language = 'pt_BR'

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

    # Pasta Servicos
    if 'servicos' not in existing:
        cria_servicos(p)

    # Pasta Imagens
    if 'imagens' not in existing:
        cria_imagens(p)

    # Colecao de Ultimas noticias
    if 'noticias' not in existing:
        cria_ultimas_noticias(p)

    wftool = getToolByName(p, "portal_workflow")
    obj_ids = ['sobre', 'assuntos', 'servicos', 'imagens', 'noticias']
    publish_content(wftool, p, obj_ids)


def cria_capa(portal):
    pass


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
