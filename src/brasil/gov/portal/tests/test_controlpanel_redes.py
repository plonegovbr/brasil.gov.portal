# -*- coding: utf-8 -*-
from brasil.gov.portal.controlpanel import socialnetworks
from brasil.gov.portal.interfaces import IBrasilGov
from brasil.gov.portal.testing import INTEGRATION_TESTING
from plone import api
from zope.interface import alsoProvides

import unittest


class ControlPanelTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        # Como nao eh um teste funcional, este objeto
        # REQUEST precisa ser anotado com o browser layer
        alsoProvides(self.portal.REQUEST, IBrasilGov)
        self.adapter = socialnetworks.SocialNetworksPanelAdapter(self.portal)

    def test_controlpanel_view(self):
        ''' Validamos se o control panel esta acessivel '''
        view = api.content.get_view(
            name='brasil.gov.portal-social',
            context=self.portal,
            request=self.portal.REQUEST,
        )
        view = view.__of__(self.portal)
        self.assertTrue(view())

    def test_controlpanel_view_protected(self):
        ''' Acesso a view nao pode ser feito por usuario anonimo '''
        # Importamos a excecao esperada
        from AccessControl import Unauthorized
        with api.env.adopt_roles(['Anonymous', ]):
            self.assertRaises(Unauthorized, self.portal.restrictedTraverse,
                              '@@brasil.gov.portal-social')

    def test_configlet_install(self):
        ''' Validamos se o control panel foi registrado '''
        # Obtemos a ferramenta de painel de controle
        controlpanel = api.portal.get_tool('portal_controlpanel')
        # Listamos todas as acoes do painel de controle
        installed = [a.getAction(self)['id']
                     for a in controlpanel.listActions()]
        # Validamos que o painel de controle da barra esteja instalado
        self.assertTrue('social-config' in installed)

    def test_site_accounts(self):
        adapter = self.adapter
        adapter.accounts_info = []
        self.assertEqual(len(adapter.accounts_info), 0)

        # Vamos cadastrar uma conta no Twitter
        info = socialnetworks.SocialNetworksPair
        twitter = info(site='twitter', info='plone')
        adapter.accounts_info = [twitter, ]

        self.assertEqual(len(adapter.accounts_info), 1)
        self.assertEqual(adapter.accounts_info[0].site, 'twitter')
