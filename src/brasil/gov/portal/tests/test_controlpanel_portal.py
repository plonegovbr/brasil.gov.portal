# -*- coding: utf-8 -*-
"""Testa o controlpanel de configuração do Portal Padrão."""
from AccessControl import Unauthorized
from brasil.gov.portal.controlpanel.portal import ISettingsPortal
from brasil.gov.portal.testing import INTEGRATION_TESTING
from plone import api
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

import unittest


class ControlPanelTestCase(unittest.TestCase):
    """Testes de configuração do Portal Padrão."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        """Configura ambiente de teste antes de cada teste."""
        self.portal = self.layer['portal']
        self.controlpanel = api.portal.get_tool('portal_controlpanel')

    def test_controlpanel_has_view(self):
        """Verifica se a view de configuração existe."""
        request = self.layer['request']
        view = api.content.get_view(u'portal-settings', self.portal, request)
        view = view.__of__(self.portal)
        self.assertTrue(view())

    def test_controlpanel_view_is_protected(self):
        from plone.app.testing import logout
        logout()
        with self.assertRaises(Unauthorized):
            self.portal.restrictedTraverse('@@portal-settings')

    def test_controlpanel_installed(self):
        """Verifica se o configlet do controlpanel está instalado."""
        actions = [a.getAction(self)['id']
                   for a in self.controlpanel.listActions()]
        self.assertIn('portal', actions)

    def test_controlpanel_permissions(self):
        """Testa a permissão de acesso ao configlet."""
        roles = ['Manager', 'Site Administrator']
        for r in roles:
            with api.env.adopt_roles([r]):
                configlets = self.controlpanel.enumConfiglets(group='Products')
                configlets = [a['id'] for a in configlets]
                self.assertIn('portal', configlets, 'configlet not listed for ' + r)


class RegistryTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.registry = getUtility(IRegistry)
        self.settings = self.registry.forInterface(ISettingsPortal)

    def test_esconde_autor_record_in_registry(self):
        """Verifica se o registro esconde_autor existe."""
        self.assertTrue(hasattr(self.settings, 'esconde_autor'))
        self.assertFalse(self.settings.esconde_autor)

    def test_esconde_data_record_in_registry(self):
        """Verifica se o registro esconde_data existe."""
        self.assertTrue(hasattr(self.settings, 'esconde_data'))
        self.assertFalse(self.settings.esconde_data)
