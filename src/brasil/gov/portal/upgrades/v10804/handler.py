# -*- coding: utf-8 -*-
from brasil.gov.portal.logger import logger
from plone.app.upgrade.utils import loadMigrationProfile


def apply_profile(context):
    """Atualiza profile para versao 10804."""
    profile = 'profile-brasil.gov.portal.upgrades.v10804:default'
    loadMigrationProfile(context, profile)
    logger.info('Atualizado para versao 10804')
