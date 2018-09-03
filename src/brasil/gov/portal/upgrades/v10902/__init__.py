# -*- coding: utf-8 -*-
from brasil.gov.portal.logger import logger
from plone import api


SCALES_TO_ADD = [
    u'Imagem-Full: 1150:1150',
    u'Imagem-8C 760:760',
    u'Imagem-7C 663:663',
    u'Imagem-6C 565:565',
    u'Imagem-5C 468:468',
    u'Imagem-4C 370:370',
    u'Imagem-3C 273:273',
]


def add_image_sizes(setup_tool):
    """Add image sizes."""
    settings = api.portal.get_tool('portal_properties').imaging_properties
    allowed_sizes = set(settings.allowed_sizes)
    allowed_sizes |= frozenset(SCALES_TO_ADD)
    settings.allowed_sizes = tuple(allowed_sizes)
    logger.info('Added image sizes.')
