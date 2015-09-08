# -*- coding: utf-8 -*-
from brasil.gov.portal.config import PROJECTNAME
from plone.app.contenttypes.interfaces import IFolder
from plone.app.upgrade.utils import loadMigrationProfile
from plone.folder.default import DefaultOrdering

import logging


logger = logging.getLogger(PROJECTNAME)


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


def apply_profile(context):
    """Atualiza profile para versao 10700."""
    profile = 'profile-brasil.gov.portal.upgrades.v10700:default'
    loadMigrationProfile(context, profile)
    logger.info('Atualizado para versao 10700')
