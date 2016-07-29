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
                profile_id
            ))

    if step and step.dest is not None and step.checker is None:
        setup.setLastVersionForProfile(profile_id, step.dest)


def csscookresources(portal_setup=None):

    api.portal.get_tool('portal_css').cookResources()
