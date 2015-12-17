# -*- coding: utf-8 -*-
"""Testa o controlpanel de configuração do Portal Padrão."""

from AccessControl import Unauthorized
from brasil.gov.portal.controlpanel.portal import ISettingsPortal
from brasil.gov.portal.testing import FUNCTIONAL_TESTING
from brasil.gov.portal.testing import INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.registry.interfaces import IRegistry
from plone.testing.z2 import Browser
from zope.component import getUtility

import unittest


class ControlPanelTestCase(unittest.TestCase):
    """Testes de configuração do Portal Padrão."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        """Configura ambiente de teste antes de cada teste."""
        self.portal = self.layer['portal']
        self.controlpanel = api.portal.get_tool('portal_controlpanel')

    def test_controlpanel_instalado(self):
        """Verifica se o configlet do controlpanel está instalado."""
        actions = [a.getAction(self)['id']
                   for a in self.controlpanel.listActions()]
        self.assertIn('portal', actions, 'Configlet não instalado.')

    def test_controlpanel_view_existe(self):
        """Verifica se a view de configuração existe."""
        request = self.layer['request']
        view = api.content.get_view(u'portal-settings', self.portal, request)
        view = view.__of__(self.portal)
        self.assertTrue(view())

    def test_controlpanel_permissao_view(self):
        """Testa a permissão da de configuração"""
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        with self.assertRaises(Unauthorized):
            self.portal.restrictedTraverse('@@portal-settings')

    def test_controlpanel_registry_esconde_autor(self):
        """Verifica se o registro esconde_autor existe."""
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISettingsPortal)
        self.assertTrue(hasattr(settings, 'esconde_autor'))
        self.assertEqual(settings.esconde_autor, False)

    def test_controlpanel_registry_esconde_data(self):
        """Verifica se o registro esconde_data existe."""
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISettingsPortal)
        self.assertTrue(hasattr(settings, 'esconde_data'))
        self.assertEqual(settings.esconde_data, False)


class ControlPanelFunctionalTestCase(unittest.TestCase):
    """Testes funcionais da configuração do Portal Padrão."""

    layer = FUNCTIONAL_TESTING

    def setUp(self):
        """Configura testes funcionais antes de cada teste."""
        self.portal = self.layer['portal']
        self.portal_url = self.portal.absolute_url()
        self.browser = Browser(self.layer['app'])
        self.login_browser()
        import transaction
        transaction.commit()

    def login_browser(self):
        """Autentica usuário de teste no browser"""
        setRoles(self.portal, TEST_USER_ID, ['Site Administrator'])
        self.browser.handleErrors = False
        basic_auth = 'Basic {0}'.format(
            '{0}:{1}'.format(TEST_USER_NAME, TEST_USER_PASSWORD)
        )
        self.browser.addHeader('Authorization', basic_auth)

    def test_configuracao_portal(self):
        """Testa a configuração do Portal Padrão."""
        label_autor = u'Esconde autor'
        label_data = u'Esconde data de publicação'.encode('utf8')
        self.browser.open('{0}/{1}'.format(self.portal.absolute_url(),
                                           '@@overview-controlpanel'))
        self.browser.getLink('.gov.br: Portal Padrão').click()
        self.assertFalse(self.browser.getControl(label_autor).selected,
                         'Campo Esconde autor com valor default errado.')
        self.assertFalse(self.browser.getControl(label_data).selected,
                         'Campo Esconde data com valor default errado.')
        self.browser.getControl(label_autor).selected = True
        self.browser.getControl(label_data).selected = True
        self.browser.getControl(name='form.buttons.save').click()
        self.assertTrue(self.browser.getControl(label_autor).selected,
                        'Esconde autor não foi salvo.')
        self.assertTrue(self.browser.getControl(label_data).selected,
                        'Esconde data não foi salvo.')
