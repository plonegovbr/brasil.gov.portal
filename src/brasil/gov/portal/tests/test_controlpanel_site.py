# -*- coding: utf-8 -*-
from brasil.gov.portal.controlpanel.site import SiteControlPanelAdapter
from brasil.gov.portal.testing import INTEGRATION_TESTING
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import getMultiAdapter

import unittest


class SiteControlPanelTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Document', 'my-document')
        self.doc = self.portal['my-document']
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.request = self.layer['request']
        self.adapter = SiteControlPanelAdapter(self.portal)

    def test_controlpanel_view(self):
        """ Validamos se o control panel esta acessivel """
        view = getMultiAdapter((self.portal, self.portal.REQUEST),
                               name='site-controlpanel')
        view = view.__of__(self.portal)
        self.assertTrue(view())

    def test_controlpanel_view_protected(self):
        """ Acesso a view nao pode ser feito por usuario anonimo """
        # Importamos a excecao esperada
        from AccessControl import Unauthorized
        # Deslogamos do portal
        logout()
        # Ao acessar a view como anonimo, a excecao e levantada
        self.assertRaises(Unauthorized,
                          self.portal.restrictedTraverse,
                          '@@site-controlpanel')

    def test_configlet_install(self):
        """ Validamos se o control panel foi registrado """
        # Obtemos a ferramenta de painel de controle
        controlpanel = self.portal.portal_controlpanel
        # Listamos todas as acoes do painel de controle
        installed = [a.getAction(self)['id']
                     for a in controlpanel.listActions()]
        # Validamos que o painel de controle do site esteja instalado
        installed = [a.getAction(self)['id']
                     for a in controlpanel.listActions()]
        self.assertTrue('PloneReconfig' in installed)

    def test_title(self):
        """ Alterar site_title_1 e site_title_2 gera site_title """
        portal = self.portal
        adapter = self.adapter
        adapter.site_title_1 = u'Portal'
        adapter.site_title_2 = u'Brasil'
        self.assertEqual(adapter.site_title, u'Portal Brasil')
        self.assertEqual(adapter.site_title, portal.title)

        # Setar o title manualmente nao tem efeito
        adapter.site_title = u'Portal Rio Grande'
        self.assertNotEqual(adapter.site_title, u'Portal Rio Grande')

    def test_orgao(self):
        portal = self.portal
        adapter = self.adapter
        adapter.site_orgao = u'Presidencia da Republica'
        self.assertEqual(adapter.site_orgao, portal.orgao)

    def test_url_orgao(self):
        portal = self.portal
        configs = getattr(portal.portal_properties, 'brasil_gov')
        url_orgao = configs.getProperty('url_orgao')
        adapter = self.adapter
        adapter.url_orgao = u''
        self.assertEqual(adapter.url_orgao, url_orgao)

    def test_description(self):
        portal = self.portal
        adapter = self.adapter
        adapter.site_description = u'Portal dos Brasileiros'
        self.assertEqual(adapter.site_description, portal.description)

        adapter.site_description = None
        self.assertEqual(adapter.site_description, '')

    def test_dc_metatags(self):
        from plone.app.layout.viewlets import common
        viewlet = common.DublinCoreViewlet(self.portal,
                                           self.request,
                                           None,
                                           None)
        adapter = self.adapter
        adapter.exposeDCMetaTags = True
        self.assertTrue(adapter.exposeDCMetaTags)
        # Atualiza viewlet
        viewlet.update()
        metatags = viewlet.metatags
        self.assertEqual(len(metatags), 7)
        # Desabilitamos as metatags dublincore
        adapter.exposeDCMetaTags = False
        self.assertFalse(adapter.exposeDCMetaTags)
        # Atualiza viewlet
        viewlet.update()
        metatags = viewlet.metatags
        self.assertEqual(len(metatags), 1)

    def test_enable_sitemap(self):
        from zope.publisher.interfaces import NotFound
        sitemap = getMultiAdapter((self.portal, self.request),
                                  name='sitemap.xml.gz')
        adapter = self.adapter

        # Desabilitamos o sitemap
        adapter.enable_sitemap = False
        # Recebemos um 404
        self.assertRaises(NotFound, sitemap)

        # Habilitamos o sitemap
        adapter.enable_sitemap = True
        self.assertTrue('sitemap.xml' in sitemap())

    def test_webstats_js(self):
        from plone.app.layout.analytics import view
        viewlet = view.AnalyticsViewlet(self.portal,
                                        self.request,
                                        None,
                                        None)
        viewlet.update()
        render = viewlet.render()
        self.assertEqual(len(render), 0)

        adapter = self.adapter
        # Definimos o codigo do analytics
        adapter.webstats_js = '<script>var foo="bar";</script>'

        viewlet.update()
        render = viewlet.render()
        self.assertEqual(len(render), len(adapter.webstats_js))

        # Passando None temos como retorno uma string vazia
        adapter.webstats_js = None
        self.assertEqual(adapter.webstats_js, '')

    def test_display_pub_date_in_byline(self):
        from DateTime import DateTime
        from plone.app.layout.viewlets import content
        # Definimos a data de publicacao de um conteudo
        effective = DateTime()
        doc = self.doc
        doc.effective_date = effective

        viewlet = content.DocumentBylineViewlet(doc,
                                                self.request,
                                                None,
                                                None)
        viewlet.update()
        # Por padrao exibimos a data de publicacao
        self.assertEqual(viewlet.pub_date(), DateTime(effective.ISO8601()))

        adapter = self.adapter
        # Desativamos a exibicao da data de publicacao
        adapter.display_pub_date_in_byline = False
        # Viewlet nao exibe a data
        self.assertEqual(viewlet.pub_date(), None)
