# -*- coding: utf-8 -*-
from brasil.gov.portal.logger import logger
from plone import api
from plone.app.upgrade.utils import loadMigrationProfile


def apply_profile(context):
    """Atualiza perfil para versao 10400"""
    profile = 'profile-brasil.gov.portal.upgrades.v10400:default'
    loadMigrationProfile(context, profile)
    logger.info('Atualizado para versao 10400')


def aplica_view_noticias(context):
    """Aplica visao sumaria para pasta Noticias"""
    noticias = api.content.get(path='/noticias')
    if noticias:
        noticias.setLayout('summary_view')
        noticias.reindexObject()
        logger.info(u'Visão sumária aplicada na pasta Notícias')
