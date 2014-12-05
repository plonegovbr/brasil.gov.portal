# -*- coding: utf-8 -*-

from brasil.gov.portal.config import PROJECTNAME
from plone.app.upgrade.utils import loadMigrationProfile

import logging


def apply_profile(context):
    ''' Atualiza perfil para versao 2000 '''
    logger = logging.getLogger(PROJECTNAME)
    profile = 'profile-brasil.gov.portal.upgrades.v2000:default'
    loadMigrationProfile(context, profile)
    logger.info('Atualizado para versao 2000')
