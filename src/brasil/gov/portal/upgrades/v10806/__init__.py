# -*- coding: utf-8 -*-
from brasil.gov.portal.logger import logger
from plone import api


def review_galeria_image_sizes(setup_tool):
    """Review galeria de fotos image sizes."""
    settings = api.portal.get_tool('portal_properties').imaging_properties
    allowed_sizes = list(settings.allowed_sizes)
    if u'galeria_de_foto_thumb 87:49' in allowed_sizes:
        allowed_sizes.remove(u'galeria_de_foto_thumb 87:49')
    if u'galeria_de_foto_view 748:513' in allowed_sizes:
        allowed_sizes.remove(u'galeria_de_foto_view 748:513')
    if u'galeria_de_foto_view 1150:650' not in allowed_sizes:
        allowed_sizes.append(u'galeria_de_foto_view 1150:650')
    settings.allowed_sizes = tuple(allowed_sizes)
    logger.info('Galeria de fotos image sizes updated.')
