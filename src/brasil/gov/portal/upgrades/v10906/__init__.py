# -*- coding: utf-8 -*-
from brasil.gov.portal.logger import logger
from plone import api


def fix_nitf_default_view(setup_tool):
    """Fix wrong value on News Article factory."""
    types_tool = api.portal.get_tool('portal_types')
    nitf = types_tool['collective.nitf.content']
    if nitf.default_view != 'view':
        nitf.default_view = 'view'
        logger.info('collective.nitf default_view fixed')
