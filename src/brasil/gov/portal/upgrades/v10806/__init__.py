# -*- coding: utf-8 -*-
from brasil.gov.portal.logger import logger
from plone import api


def update_galeria_image_sizes(setup_tool):
    """Update galeria de fotos image sizes."""
    settings = api.portal.get_tool('portal_properties').imaging_properties
    allowed_sizes = set(settings.allowed_sizes)
    allowed_sizes -= frozenset([
        u'galeria_de_foto_thumb 87:49', u'galeria_de_foto_view 748:513'])
    allowed_sizes |= frozenset([u'galeria_de_foto_view 1150:650'])
    settings.allowed_sizes = tuple(allowed_sizes)
    logger.info('Galeria de fotos image sizes updated.')
