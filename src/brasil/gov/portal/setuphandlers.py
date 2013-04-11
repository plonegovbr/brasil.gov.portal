# -*- coding:utf-8 -*-
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import _createObjectByType


def setupPortalContent(p):
    '''
    '''
    existing = p.keys()
    language = 'pt_BR'

    # Pagina Inicial
    # TODO -- Cover
    if 'front-page' not in existing:
        pass

    # Pasta Assuntos
    if 'assuntos' not in existing:
        title = 'Assuntos'
        description = u'Assuntos deste Órgão'

        _createObjectByType('Folder', p, id='assuntos',
                            title=title, description=description)

        folder = p.assuntos
        folder.setOrdering('unordered')
        #folder.setConstrainTypesMode(1)
        # Permitimos preferencialmente outras pastas
        #folder.setImmediatelyAddableTypes(['Folder'])
        #folder.setLayout('folder_summary_view')
        #folder.unmarkCreationFlag()
        #folder.setLanguage(language)

    # Pasta Sobre
    if 'sobre' not in existing:
        title = 'Sobre'
        description = u'Conheça este órgão'

        _createObjectByType('Folder', p, id='sobre',
                            title=title, description=description)

        folder = p.sobre
        folder.setOrdering('unordered')
        #folder.setConstrainTypesMode(1)
        # Permitimos preferencialmente outras pastas
        #folder.setImmediatelyAddableTypes(['Folder'])
        #folder.setLayout('folder_summary_view')
        #folder.unmarkCreationFlag()
        #folder.setLanguage(language)
        # Criar algumas paginas

    wftool = getToolByName(p, "portal_workflow")
    obj_ids = ['sobre', 'assuntos']
    publish_content(wftool, p, obj_ids)


def publish_content(wftool, folder, obj_ids):
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
