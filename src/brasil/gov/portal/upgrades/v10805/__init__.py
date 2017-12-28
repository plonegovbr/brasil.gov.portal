# -*- coding: utf-8 -*-
from brasil.gov.portal.logger import logger
from plone import api


SCRIPTS = [
    '++resource++jquery.cookie.js',
    '++resource++contraste.js'
]


def remove_scripts(setup_tool):
    """Remvove JS from registered resources."""
    js_tool = api.portal.get_tool('portal_javascripts')
    for js in SCRIPTS:
        js_tool.unregisterResource(id=js)
        assert js not in js_tool.getResourceIds()
    logger.info('Scripts removed')
