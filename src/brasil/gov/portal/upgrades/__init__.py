# -*- coding: utf-8 -*-
from brasil.gov.portal.logger import logger
from plone import api


def upgrade_profile(setup, profile_id):
    """Runs all non-installed upgrades for a profile."""
    step = None
    # get non-installed upgrades
    for upgrades in setup.listUpgrades(profile_id):
        for upgrade in upgrades:
            if upgrade['done']:
                continue

            step = upgrade['step']
            step.doStep(setup)
            logger.info('Ran upgrade step %s for profile %s' % (
                step.title,
                profile_id,
            ))

    if step and step.dest is not None and step.checker is None:
        setup.setLastVersionForProfile(profile_id, step.dest)


def cook_css_resources(context):  # pragma: no cover
    """Cook CSS resources."""
    css_tool = api.portal.get_tool('portal_css')
    css_tool.cookResources()
    logger.info('CSS resources were cooked')


def cook_javascript_resources(context):  # pragma: no cover
    """Cook JavaScripts resources."""
    js_tool = api.portal.get_tool('portal_javascripts')
    js_tool.cookResources()
    logger.info('JavaScripts resources were cooked')
