# -*- coding: utf-8 -*-
from brasil.gov.portal.browser.viewlets.servicos import ServicosViewlet

from brasil.gov.portal.controlpanel.site import SiteControlPanelAdapter
from brasil.gov.portal.interfaces import IBrasilGov
from brasil.gov.portal.testing import INTEGRATION_TESTING
from plone import api
from plone.app.layout.viewlets.common import SiteActionsViewlet
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.app.theming.utils import applyTheme
from plone.app.theming.utils import getTheme
from plone.testing.z2 import Browser
from zope.interface import alsoProvides

import unittest


class AccessibilityTestCase(unittest.TestCase):

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


class PortalLogoTestCase(AccessibilityTestCase):
    def base_test(self, cor):
        """Teste base dos temas"""
        adapter = self.adapter
        adapter.site_title_1 = u'Portal'
        adapter.site_title_2 = u'Brasil'

        theme = getTheme(cor)
        applyTheme(theme)

        self.browser.open(self.portal.absolute_url())

        # Testa se a âncora para o conteúdo aparece.
        self.assertIn(
            '<div id="portal-title"',
            self.browser.contents
        )

    def test_tema_amarelo(self):
        self.base_test('amarelo')

    def test_tema_azul(self):
        self.base_test('azul')

    def test_tema_branco(self):
        self.base_test('branco')

    def test_tema_verde(self):
        self.base_test('verde')


class SiteActionsViewletTestCase(AccessibilityTestCase):

    def setUp(self):
        super(SiteActionsViewletTestCase, self).setUp()
        self.viewlet = SiteActionsViewlet(self.portal, self.request, None, None)
        self.viewlet.update()

    def test_render(self):
        """Teste do template da viewlet"""

        # Testa se os links foram gerados sem o atributo title.
        url_portal = self.portal.absolute_url()
        self.browser.open(url_portal)
        self.assertIn('<a href="{0}/acessibilidade" accesskey="5">Acessibilidade</a>'.format(
                      url_portal), self.browser.contents)
        self.assertIn('<a href="#" accesskey="6">Alto Contraste</a>', self.browser.contents)
        self.assertIn('<a href="{0}/mapadosite" accesskey="7">Mapa do Site</a>'.format(
                      url_portal), self.browser.contents)


class ServicosViewletTestCase(AccessibilityTestCase):

    def test_render_title(self):
        """Teste para identificar se o atributo title está presente"""

        with api.env.adopt_roles(['Manager', ]):
            self.servicos = api.content.create(
                type='Folder',
                container=self.portal,
                id='servicos',
                title=u'Servicos'
            )
            api.content.create(
                type='Link',
                container=self.servicos,
                id='servico',
                title=u'Servico',
                description=u'Descricao'
            )
        self.viewlet = ServicosViewlet(self.portal, self.request, None, None)
        self.viewlet.update()

        # Testa se o link foi gerado com a descrição no atributo title.
        self.assertIn('title', self.viewlet.render())

    def test_render_not_title(self):
        """Teste para identificar se o atributo title está presente"""

        with api.env.adopt_roles(['Manager', ]):
            self.servicos = api.content.create(
                type='Folder',
                container=self.portal,
                id='servicos',
                title=u'Servicos'
            )
            api.content.create(
                type='Link',
                container=self.servicos,
                id='servico',
                title=u'Servico'
            )
        self.viewlet = ServicosViewlet(self.portal, self.request, None, None)
        self.viewlet.update()

        # Testa se o link foi gerado sem o atributo title.
        self.assertNotIn('title', self.viewlet.render())
