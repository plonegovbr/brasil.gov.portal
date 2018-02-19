# -*- coding: utf-8 -*-
from brasil.gov.portal.logger import logger
from plone import api


def search_for_embedder(setup_tool):
    """Remove sc.embedder from types_not_searched."""
    settings = api.portal.get_tool('portal_properties').site_properties
    if 'sc.embedder' in settings.types_not_searched:
        types_not_searched = list(settings.types_not_searched)
        types_not_searched.remove('sc.embedder')
        settings.types_not_searched = tuple(types_not_searched)
        logger.info('Search for sc.embedder objects is enabled')
