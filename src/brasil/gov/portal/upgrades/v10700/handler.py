# -*- coding: utf-8 -*-
from brasil.gov.portal.config import PROJECTNAME
from brasil.gov.portal.upgrades import upgrade_profile
from collective.cover.controlpanel import ICoverSettings
from collective.cover.interfaces import ICover
from plone import api
from plone.app.contenttypes.interfaces import IFolder
from plone.app.upgrade.utils import loadMigrationProfile
from plone.folder.default import DefaultOrdering
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

import json
import logging


logger = logging.getLogger(PROJECTNAME)


def atualiza_produtos_terceiros(context):
    """ Atualiza os profiles de produtos de terceiros."""
    profiles = (
        'brasil.gov.agenda:default',
        'brasil.gov.barra:default',
        'brasil.gov.portlets:default',
        'brasil.gov.tiles:default',
        'brasil.gov.vcge:default',
        'collective.cover:default',
        'collective.nitf:default',
        'collective.polls:default',
        'sc.embedder:default',
        'sc.social.like:default',
    )
    for profile_id in profiles:
        upgrade_profile(context, profile_id)

    logger.info('Produtos de terceiros foram atualizados')


def ordernacao_pastas(context):
    """ Ajusta a ordenacao das pastas da raiz do portal setando ordenação
        padrão Plone. Similar ao ordenacao_pastas feito no upgradeStep 5000, só
        que ao invés de ordenar pastas pontuais ele é executado em todas as
        pastas.
    """
    plone_view = context.restrictedTraverse('@@plone_portal_state')
    site = plone_view.portal()
    for pasta_id in site.objectIds():
        pasta = site[pasta_id]
        # Se não for diretório e já estiver com a ordenação default, não faça
        # nada.
        if (not IFolder.providedBy(pasta) or
           isinstance(pasta.getOrdering(), DefaultOrdering)):
            continue

        # Define ordenacao padrao
        pasta.setOrdering()
        ordering = pasta.getOrdering()
        # A ordenacao dos itens na pasta e mantida em uma
        # Annotation. Aqui vamos repopula-la com os dados
        # corretos
        real = [o for o in pasta.objectIds(ordered=False)]
        stored = [o for o in pasta.objectIds(ordered=True)]
        for o in stored:
            ordering.notifyRemoved(o)
        for o in real:
            ordering.notifyAdded(o)
        logger.info('Pasta %s atualizada', pasta.Title())


def _corrige_css_class(row):
    """ Verifica se o campo css_class não é uma
        string válida, e substitui por uma string vazia.
    """
    if 'css_class' in row:
        css_class = row['css_class']
        if (type(css_class) is not str or
           css_class == '--NOVALUE--'):
            css_class = ''
        row['css_class'] = css_class
    return row


def _corrige_conteudo_collectivecover(obj, layout, is_child=False):
    """ Verifica recursivamente se o campo css_class não é uma
        string válida, e substitui por uma string vazia.
        Caso for um tile, corrige sua configuração.
    """
    if not is_child:
        layout = json.loads(layout)
    fixed_layout = []
    for row in layout:
        fixed_row = row
        if (obj is not None and
           fixed_row.get('type', u'') == u'tile'):
            tile_url = '@@{0}/{1}'.format(fixed_row.get('tile-type'),
                                          fixed_row.get('id'))
            tile = obj.restrictedTraverse(tile_url.encode(), None)
            if tile is not None:
                tile_conf = tile.get_tile_configuration()
                tile_conf = _corrige_css_class(tile_conf)
                tile.set_tile_configuration(tile_conf)
        fixed_row = _corrige_css_class(fixed_row)
        if u'children' in fixed_row:
            fixed_row[u'children'] = _corrige_conteudo_collectivecover(
                obj,
                fixed_row[u'children'],
                True
            )
        fixed_layout.append(fixed_row)
    if is_child:
        return fixed_layout
    else:
        fixed_layout = json.dumps(fixed_layout)
        return fixed_layout.decode('utf-8')


def _reindex_covers():
    """Reindexa as capas do conteúdo inicial."""
    catalog = api.portal.get_tool(name='portal_catalog')
    covers = catalog(portal_type='collective.cover.content')
    for brain in covers:
        cover = brain.getObject()
        cover.reindexObject()


def corrige_conteudo_collectivecover(context):
    """ Verifica se o campo css_class não é uma string válida,
        e substitui por uma string vazia.
    """
    # Initial content was not indexed correctly, reindex all covers
    _reindex_covers()
    logger.info('All covers were reindexed.')
    # Make sure collective.cover is upgraded before continuing
    upgrade_profile(context, 'collective.cover:default')

    logger.info('CSS classes will be fixed from Cover layouts.')
    # Fix registry layouts
    registry = getUtility(IRegistry)
    settings = registry.forInterface(ICoverSettings)
    fixed_layouts = {}
    for name, layout in settings.layouts.iteritems():
        fixed_layouts[name] = _corrige_conteudo_collectivecover(None, layout)
    settings.layouts = fixed_layouts
    logger.info('Registry layouts were updated.')

    # Fix cover layouts
    covers = context.portal_catalog(object_provides=ICover.__identifier__)
    logger.info('Layout of {0} objects will be updated'.format(len(covers)))

    for cover in covers:
        obj = cover.getObject()
        obj.cover_layout = _corrige_conteudo_collectivecover(obj,
                                                             obj.cover_layout)
        logger.info('"{0}" was updated'.format(obj.absolute_url_path()))


def apply_profile(context):
    """Atualiza profile para versao 10700."""
    profile = 'profile-brasil.gov.portal.upgrades.v10700:default'
    loadMigrationProfile(context, profile)
    logger.info('Atualizado para versao 10700')
