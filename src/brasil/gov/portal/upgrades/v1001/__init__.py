# -*- coding: utf-8 -*-
from brasil.gov.portal.logger import logger
from plone import api


STYLES = [
    '++resource++brasil.gov.portal/css/main.css',
    '++resource++brasil.gov.portal/css/main-print.css'
]


def remove_styles(setup_tool):
    """Remvove CSS from registered resources."""
    css_tool = api.portal.get_tool('portal_css')
    for css in STYLES:
        css_tool.unregisterResource(id=css)
        assert css not in css_tool.getResourceIds()
    logger.info('Styles removed')
