# -*- coding: utf-8 -*-
from brasil.gov.portal.logger import logger
from plone.app.upgrade.utils import loadMigrationProfile


def apply_profile(context):
    """ Atualiza perfil para versao 3000 """
    profile = 'profile-brasil.gov.portal.upgrades.v3000:default'
    loadMigrationProfile(context, profile)
    logger.info('Atualizado para versao 3000')
