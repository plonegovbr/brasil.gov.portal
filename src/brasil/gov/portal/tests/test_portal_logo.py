# -*- coding: utf-8 -*-
from brasil.gov.portal.controlpanel.site import SiteControlPanelAdapter
from brasil.gov.portal.interfaces import IBrasilGov
from brasil.gov.portal.testing import INTEGRATION_TESTING
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.app.theming.utils import applyTheme
from plone.app.theming.utils import getTheme
from plone.testing.z2 import Browser
from zope.interface import alsoProvides

import unittest
import transaction


class SiteControlPanelTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        # Como nao eh um teste funcional, este objeto
        # REQUEST precisa ser anotado com o browser layer
        alsoProvides(self.portal.REQUEST, IBrasilGov)
        self.request = self.layer['request']
        self.adapter = SiteControlPanelAdapter(self.portal)
        self.browser = Browser(self.layer['app'])

    def base_test(self, cor):
        """Teste base dos temas"""
        adapter = self.adapter
        adapter.site_title_1 = u'Portal'
        adapter.site_title_2 = u'Brasil'

        theme = getTheme(cor)
        applyTheme(theme)
        transaction.commit()

        self.browser.open(self.portal.absolute_url())

        # Testa se a âncora para o conteúdo aparece.
        self.assertIn(
            '<div id="portal-title"',
            self.browser.contents
        )

    def test_logo_tema_amarelo(self):
        self.base_test('amarelo')

    def test_logo_tema_azul(self):
        self.base_test('azul')

    def test_logo_tema_branco(self):
        self.base_test('branco')

    def test_logo_tema_verde(self):
        self.base_test('verde')
