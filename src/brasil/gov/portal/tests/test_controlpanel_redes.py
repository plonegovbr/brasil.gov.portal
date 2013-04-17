# -*- coding: utf-8 -*-
from brasil.gov.portal.interfaces import IBrasilGov
from brasil.gov.portal.testing import INTEGRATION_TESTING
from plone.app.testing import logout
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter
from zope.interface import alsoProvides

import unittest2 as unittest


class ControlPanelTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        # Como nao eh um teste funcional, este objeto
        # REQUEST precisa ser anotado com o browser layer
        alsoProvides(self.portal.REQUEST, IBrasilGov)

    def test_controlpanel_view(self):
        ''' Validamos se o control panel esta acessivel '''
        view = getMultiAdapter((self.portal, self.portal.REQUEST),
                               name='brasil.gov.portal-social')
        view = view.__of__(self.portal)
        self.failUnless(view())

    def test_controlpanel_view_protected(self):
        ''' Acesso a view nao pode ser feito por usuario anonimo '''
        # Importamos a excecao esperada
        from AccessControl import Unauthorized
        # Deslogamos do portal
        logout()
        # Ao acessar a view como anonimo, a excecao e levantada
        self.assertRaises(Unauthorized, self.portal.restrictedTraverse,
                          '@@brasil.gov.portal-social')

    def test_configlet_install(self):
        ''' Validamos se o control panel foi registrado '''
        # Obtemos a ferramenta de painel de controle
        controlpanel = getToolByName(self.portal, 'portal_controlpanel')
        # Listamos todas as acoes do painel de controle
        installed = [a.getAction(self)['id']
                     for a in controlpanel.listActions()]
        # Validamos que o painel de controle da barra esteja instalado
        self.failUnless('social-config' in installed)
