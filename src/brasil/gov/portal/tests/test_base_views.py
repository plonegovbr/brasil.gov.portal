# -*- coding: utf-8 -*-

from brasil.gov.portal.browser.plone.admin import Overview
from brasil.gov.portal.testing import FUNCTIONAL_TESTING
from brasil.gov.portal.testing import INTEGRATION_TESTING
from plone import api
from plone.testing.z2 import Browser

import unittest


class OverviewViewFunctionalTestCase(unittest.TestCase):

    layer = FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.app = self.layer['app']
        self.request = self.layer['request']

    def test_overview_view(self):
        browser = Browser(self.layer['app'])
        browser.open('{0}/plone-overview'.format(self.app.absolute_url()))
        self.assertIn("<title>Portal Padr", browser.contents)


class OverviewViewIntegrationTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.app = self.layer['app']
        self.request = self.layer['request']
        self.view = Overview(self.app, self.request)

    def test_overview_sites(self):
        sites = self.view.sites()
        # By default we have one site created
        self.assertEqual(len(sites), 1)
        self.assertEqual(sites[0], self.portal)

    def test_overview_can_manage(self):
        # Anonymous
        self.assertEqual(self.view.can_manage(), None)
        with api.env.adopt_roles(['Manager']):
            # As manager
            self.assertEqual(self.view.can_manage(), True)

    def test_overview_upgrade_url(self):
        # Anonymous
        self.assertEqual(
            self.view.upgrade_url(self.portal),
            '{0}/@@plone-root-login'.format(self.app.absolute_url())
        )
        with api.env.adopt_roles(['Manager']):
            # As manager
            self.assertEqual(
                self.view.upgrade_url(self.portal),
                '{0}/@@plone-upgrade'.format(self.portal.absolute_url())
            )

    def test_overview_outdated(self):
        # If we pass an object without portal_migration, we will receive
        # False as return
        self.assertEqual(self.view.outdated(self.app), False)

        # We have a fresh new site, not outdated
        self.assertEqual(self.view.outdated(self.portal), False)
