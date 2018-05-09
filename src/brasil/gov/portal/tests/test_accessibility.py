# -*- coding: utf-8 -*-
from brasil.gov.portal.browser.viewlets.servicos import ServicosViewlet
from brasil.gov.portal.controlpanel.site import SiteControlPanelAdapter
from brasil.gov.portal.testing import INTEGRATION_TESTING
from plone import api
from plone.app.layout.viewlets.common import SiteActionsViewlet
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.theming.utils import applyTheme
from plone.app.theming.utils import getTheme
from plone.testing.z2 import Browser
from Products.Five.browser import BrowserView as View
from zope.component import queryMultiAdapter
from zope.viewlet.interfaces import IViewletManager

import transaction
import unittest


class AccessibilityTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.request = self.layer['request']
        self.adapter = SiteControlPanelAdapter(self.portal)
        self.browser = Browser(self.layer['app'])
        self.ltool = self.portal.portal_languages
        supportedLanguages = ['en', 'es', 'pt-br']
        self.ltool.manage_setLanguageSettings(
            'pt-br', supportedLanguages, setUseCombinedLanguageCodes=True)
        transaction.commit()


class PortalLogoTestCase(AccessibilityTestCase):

    def portal_logo_tema_test(self, cor):
        """Testa se o portal logo está presente em todos os temas."""
        adapter = self.adapter
        adapter.site_title_1 = u'Portal'
        adapter.site_title_2 = u'Brasil'

        theme = getTheme(cor)
        applyTheme(theme)

        self.browser.open(self.portal.absolute_url())

        self.assertIn('<div id="portal-title"', self.browser.contents)

    def test_tema_amarelo(self):
        self.portal_logo_tema_test('amarelo')

    def test_tema_azul(self):
        self.portal_logo_tema_test('azul')

    def test_tema_branco(self):
        self.portal_logo_tema_test('branco')

    def test_tema_verde(self):
        self.portal_logo_tema_test('verde')


class AcessibilidadeViewletTestCase(AccessibilityTestCase):

    def test_viewlet_is_present(self):
        """Testa se a viewlet foi registrada corretamente."""
        request = self.request
        context = self.portal

        view = View(context, request)

        manager_name = 'plone.portaltop'

        manager = queryMultiAdapter((context, request, view), IViewletManager, manager_name, default=None)

        # Testa se o viewlet manager existe
        self.assertIsNotNone(manager)

        manager.update()

        my_viewlet = [v for v in manager.viewlets if v.__name__ == 'brasil.gov.portal.acessibilidade']

        # Testa se o viewlet existe
        self.assertEqual(len(my_viewlet), 1)

    def find_translated_anchor_test(self, cor, defaultLanguage):
        """ Verifica se os links acontent, anavigation e afooter estão presentes
            e traduzidos.
        """
        transaction.begin()

        supportedLanguages = ['en', 'es', 'pt-br']
        self.ltool.manage_setLanguageSettings(
            defaultLanguage, supportedLanguages, setUseCombinedLanguageCodes=True)

        transaction.commit()

        theme = getTheme(cor)
        applyTheme(theme)

        self.browser.open(self.portal.absolute_url())
        contents = self.browser.contents.decode('utf-8')

        if defaultLanguage == 'en':
            # Testa se a âncora para o conteúdo aparece.
            self.assertIn(
                u'<a name="acontent" id="acontent" class="anchor">content</a>',
                contents,
            )
            # Testa se a âncora para o menu aparece.
            self.assertIn(
                u'<a name="anavigation" id="anavigation" class="anchor">navigation</a>',
                contents,
            )
            # Testa se a âncora para o rodapé aparece.
            self.assertIn(
                u'<a name="afooter" id="afooter" class="anchor">footer</a>',
                contents,
            )
        elif defaultLanguage == 'es':
            # Testa se a âncora para o conteúdo aparece.
            self.assertIn(
                u'<a name="acontent" id="acontent" class="anchor">contenido</a>',
                contents,
            )
            # Testa se a âncora para o menu aparece.
            self.assertIn(
                u'<a name="anavigation" id="anavigation" class="anchor">navegación</a>',
                contents,
            )
            # Testa se a âncora para o rodapé aparece.
            self.assertIn(
                u'<a name="afooter" id="afooter" class="anchor">pie de página</a>',
                contents,
            )
        elif defaultLanguage == 'pt-br':
            # Testa se a âncora para o conteúdo aparece.
            self.assertIn(
                u'<a name="acontent" id="acontent" class="anchor">conteúdo</a>',
                contents,
            )
            # Testa se a âncora para o menu aparece.
            self.assertIn(
                u'<a name="anavigation" id="anavigation" class="anchor">menu</a>',
                contents,
            )
            # Testa se a âncora para o rodapé aparece.
            self.assertIn(
                u'<a name="afooter" id="afooter" class="anchor">rodapé</a>',
                contents,
            )

    def test_tema_amarelo(self):
        self.find_translated_anchor_test('amarelo', 'en')
        self.find_translated_anchor_test('amarelo', 'es')
        self.find_translated_anchor_test('amarelo', 'pt-bt')

    def test_tema_azul(self):
        self.find_translated_anchor_test('azul', 'en')
        self.find_translated_anchor_test('azul', 'es')
        self.find_translated_anchor_test('azul', 'pt-br')

    def test_tema_branco(self):
        self.find_translated_anchor_test('branco', 'en')
        self.find_translated_anchor_test('branco', 'es')
        self.find_translated_anchor_test('branco', 'pt-br')

    def test_tema_verde(self):
        self.find_translated_anchor_test('verde', 'en')
        self.find_translated_anchor_test('verde', 'es')
        self.find_translated_anchor_test('verde', 'pt-br')


class SiteActionsViewletTestCase(AccessibilityTestCase):

    def setUp(self):
        super(SiteActionsViewletTestCase, self).setUp()
        self.viewlet = SiteActionsViewlet(self.portal, self.request, None, None)
        self.viewlet.update()

    def test_render(self):
        """Teste do template da viewlet."""

        # Testa se os links foram gerados sem o atributo title.
        url_portal = self.portal.absolute_url()
        self.browser.open(url_portal)
        self.assertIn(
            '<a href="{0}/acessibilidade" accesskey="5">'.format(url_portal),
            self.browser.contents,
        )
        self.assertIn('<a href="#" accesskey="6">', self.browser.contents)
        self.assertIn(
            '<a href="{0}/mapadosite" accesskey="7">'.format(url_portal),
            self.browser.contents,
        )


class ServicosViewletTestCase(AccessibilityTestCase):

    def test_render_title(self):
        """Teste para identificar se o atributo title está presente."""

        with api.env.adopt_roles(['Manager']):
            self.servicos = api.content.create(
                type='Folder',
                container=self.portal,
                id='servicos',
                title=u'Servicos',
            )
            api.content.create(
                type='Link',
                container=self.servicos,
                id='servico',
                title=u'Servico',
                description=u'Descricao',
            )
        self.viewlet = ServicosViewlet(self.portal, self.request, None, None)
        self.viewlet.update()

        # Testa se o link foi gerado com a descrição no atributo title.
        self.assertIn('title', self.viewlet.render())

    def test_render_not_title(self):
        """Teste para identificar se o atributo title está presente."""

        with api.env.adopt_roles(['Manager']):
            self.servicos = api.content.create(
                type='Folder',
                container=self.portal,
                id='servicos',
                title=u'Servicos',
            )
            api.content.create(
                type='Link',
                container=self.servicos,
                id='servico',
                title=u'Servico',
            )
        self.viewlet = ServicosViewlet(self.portal, self.request, None, None)
        self.viewlet.update()

        # Testa se o link foi gerado sem o atributo title.
        self.assertNotIn('title', self.viewlet.render())
