# -*- coding: utf-8 -*-
from brasil.gov.portal.config import PROJECTNAME
from plone.app.upgrade.utils import loadMigrationProfile

import logging

logger = logging.getLogger(PROJECTNAME)


def apply_profile(context):
    ''' Atualiza perfil para versao 5000 '''
    profile = 'profile-brasil.gov.portal.upgrades.v5000:default'
    loadMigrationProfile(context, profile)
    logger.info('Atualizado para versao 5000')


def ordernacao_pastas(context):
    """ Ajusta a ordenacao das pastas
        assuntos, imagens e sobre
    """
    plone_view = context.restrictedTraverse('@@plone_portal_state')
    site = plone_view.portal()
    pastas = ['assuntos', 'imagens', 'sobre']
    for pasta_id in pastas:
        if pasta_id not in site.objectIds():
            continue
        pasta = site[pasta_id]
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
        logger.info('Pasta %s atualizada' % pasta.Title())
