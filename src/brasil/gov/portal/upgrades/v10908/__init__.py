# -*- coding: utf-8 -*-
from brasil.gov.portal.logger import logger
from plone import api


def enable_livesearch(setup_tool):
    """Enable livesearch by default."""
    settings = api.portal.get_tool('portal_properties').site_properties
    if not settings.enable_livesearch:
        settings.enable_livesearch = True
        logger.info('Live search enabled.')
