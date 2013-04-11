# -*- coding: utf-8 -*-

from brasil.gov.portal.config import PROJECTNAME

import logging

logger = logging.getLogger(PROJECTNAME)


def setup(context):
    """ Initial step
    """
    logger.info('Do nothing')
