# -*- coding: utf-8 -*-
from brasil.gov.portal.logger import logger
from plone.app.upgrade.utils import loadMigrationProfile


def apply_profile(context):
    """ Atualiza perfil para versao 4000 """
    profile = 'profile-brasil.gov.portal.upgrades.v4000:default'
    loadMigrationProfile(context, profile)
    logger.info('Atualizado para versao 4000')
