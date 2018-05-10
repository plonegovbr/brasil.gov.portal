# -*- coding: utf-8 -*-

from brasil.gov.portal.browser.plone.admin import Overview
from brasil.gov.portal.testing import FUNCTIONAL_TESTING
from brasil.gov.portal.testing import INTEGRATION_TESTING
from plone import api
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
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
        self.assertIn('<title>e-Government Digital Identity', browser.contents)


class OverviewViewIntegrationTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.app = self.layer['app']
        self.request = self.layer['request']
        self.view = Overview(self.app, self.request)

    def test_overview_sites(self):
        # Listagem de sites disponiveis nesta instalacao
        sites = self.view.sites()
        # Como estamos rodando um teste, teremos um site criado
        self.assertEqual(len(sites), 1)
        self.assertEqual(sites[0], self.portal)

    def test_overview_can_manage(self):
        # Usuarios anonimos nao podem gerenciar o ambiente
        self.assertEqual(self.view.can_manage(), None)
        with api.env.adopt_roles(['Manager']):
            # Usuarios com papel de Manager podem
            self.assertEqual(self.view.can_manage(), True)

    def test_overview_upgrade_url(self):
        # Usuarios anonimos serao redirecionados para o login
        self.assertEqual(
            self.view.upgrade_url(self.portal),
            '{0}/@@plone-root-login'.format(self.app.absolute_url()))
        with api.env.adopt_roles(['Manager']):
            # Usuarios com papel de manager poderao realizar o upgrade
            self.assertEqual(
                self.view.upgrade_url(self.portal),
                '{0}/@@plone-upgrade'.format(self.portal.absolute_url()))

    def test_overview_outdated(self):
        # Objetos que nao contenham o portal_migration nao podem
        # estar 'desatualizados'
        self.assertEqual(self.view.outdated(self.app), False)

        # Como temos um portal novissimo, ele nao precisa atualizacao
        self.assertEqual(self.view.outdated(self.portal), False)


class AddSiteViewFunctionalTestCase(unittest.TestCase):

    layer = FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.app = self.layer['app']
        self.request = self.layer['request']

    def test_addsite_view(self):
        import base64
        browser = Browser(self.layer['app'])
        browser.handleErrors = False
        basic_auth = 'Basic {0}'.format(base64.encodestring('{0}:{1}'.format(SITE_OWNER_NAME, SITE_OWNER_PASSWORD)))
        browser.addHeader('Authorization', basic_auth)
        browser.open('{0}/@@plone-addsite?site_id=site'.format(self.app.absolute_url()))
        # site_id veio do parametro de query string
        self.assertIn('"site"', browser.contents)
        self.assertIn('Name of Ministry or', browser.contents)
