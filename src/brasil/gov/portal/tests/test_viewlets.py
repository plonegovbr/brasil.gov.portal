# -*- coding: utf-8 -*-
from brasil.gov.portal.browser.viewlets.destaques import Destaques_Viewlet
from brasil.gov.portal.browser.viewlets.logo import LogoViewlet
from brasil.gov.portal.browser.viewlets.nitf_byline import NITFBylineViewlet
from brasil.gov.portal.browser.viewlets.redes import RedesSociaisViewlet
from brasil.gov.portal.browser.viewlets.related import RelatedItemsViewlet
from brasil.gov.portal.browser.viewlets.servicos import ServicosViewlet
from brasil.gov.portal.testing import INTEGRATION_TESTING
from plone import api
from plone.app.testing import logout
from z3c.relationfield import RelationValue
from zope.component import getUtility
from zope.intid.interfaces import IIntIds

import unittest


class DestaquesViewletTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        with api.env.adopt_roles(['Manager', ]):
            self.destaques = api.content.create(
                type='collective.cover.content',
                container=self.portal,
                id='destaques',
                title=u'Destaques'
            )

    def viewlet(self, context=None):
        context = context or self.portal
        viewlet = Destaques_Viewlet(context, self.request, None, None)
        viewlet.update()
        return viewlet

    def test_available(self):
        viewlet = self.viewlet()
        self.assertTrue(viewlet.available())

    def test_not_available_on_folder(self):
        with api.env.adopt_roles(['Manager', ]):
            api.content.create(
                type='Folder',
                container=self.portal,
                id='pasta',
                title=u'Uma pasta'
            )
        viewlet = self.viewlet(self.portal['pasta'])
        self.assertFalse(viewlet.available())

    def test_not_available(self):
        with api.env.adopt_roles(['Manager', ]):
            # Apagamos a capa de destaques
            api.content.delete(obj=self.portal['destaques'])
        viewlet = self.viewlet()
        self.assertFalse(viewlet.available())

    def test_available_for_different_content_type(self):
        with api.env.adopt_roles(['Manager', ]):
            # Apagamos a capa de destaques
            api.content.delete(obj=self.portal['destaques'])
            # Colocamos uma pasta no mesmo lugar
            pasta = api.content.create(
                type='Folder',
                container=self.portal,
                id='destaques',
                title=u'Uma pasta com destaques'
            )
        viewlet = self.viewlet()
        # O Viewlet deve detectar o problema e nao exibir nada
        self.assertEqual(pasta.portal_type, 'Folder')
        self.assertFalse(viewlet.available())

    def test_editable(self):
        viewlet = self.viewlet()
        self.assertTrue(viewlet.editable())

    def test_not_editable_by_anonymous(self):
        logout()
        viewlet = self.viewlet()
        self.assertFalse(viewlet.editable())

    def test_portal_url(self):
        logout()
        viewlet = self.viewlet()
        self.assertEqual(viewlet.portal_url,
                         self.portal.portal_url())


class LogoViewletTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.portal.title = u'Portal Brasil'
        self.portal.title_1 = u'Portal'
        self.portal.title_2 = u'Brasil'
        self.portal.orgao = u'Presidencia da República'
        self.portal.description = u'O portal do Brasil'

    def viewlet(self):
        viewlet = LogoViewlet(self.portal, self.request, None, None)
        viewlet.update()
        return viewlet

    def test_title(self):
        expected = self.portal.title
        viewlet = self.viewlet()
        self.assertEqual(viewlet.title(), expected)

    def test_title_1(self):
        expected = self.portal.title_1
        viewlet = self.viewlet()
        self.assertEqual(viewlet.title_1(), expected)

    def test_title_2(self):
        expected = self.portal.title_2
        viewlet = self.viewlet()
        self.assertEqual(viewlet.title_2(), expected)

    def test_title_2_class(self):
        # texto curto
        self.portal.title_2 = u'Brasil'
        viewlet = self.viewlet()
        self.assertEqual(viewlet.title_2_class(), 'corto')
        # texto longo
        self.portal.title_2 = u'Desenvolvimento Social e Combate à Fome'
        viewlet = self.viewlet()
        self.assertEqual(viewlet.title_2_class(), 'luongo')

    def test_orgao(self):
        expected = self.portal.orgao
        viewlet = self.viewlet()
        self.assertEqual(viewlet.orgao(), expected)

    def test_description(self):
        expected = self.portal.description
        viewlet = self.viewlet()
        self.assertEqual(viewlet.description(), expected)

    def test_portal(self):
        expected = self.portal
        viewlet = self.viewlet()
        self.assertEqual(viewlet.portal(), expected)


class RedesViewletTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        with api.env.adopt_roles(['Manager', ]):
            self.sheet = self.portal.portal_properties.brasil_gov
            self.sheet.manage_changeProperties(social_networks=[
                'twitter|twitter',
            ])

    def viewlet(self):
        viewlet = RedesSociaisViewlet(self.portal, self.request, None, None)
        viewlet.update()
        return viewlet

    def test_available(self):
        viewlet = self.viewlet()
        self.assertTrue(viewlet.available())

    def test_not_available(self):
        # Removemos a configuracao de redes sociais
        self.sheet.manage_changeProperties(social_networks=[])
        viewlet = self.viewlet()
        self.assertFalse(viewlet.available())

    def test_redes(self):
        viewlet = self.viewlet()
        redes = viewlet.redes
        self.assertEqual(len(redes), 1)
        self.assertEqual(redes[0]['site'], 'twitter')


class RelatedViewletTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        intids = getUtility(IIntIds)
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        with api.env.adopt_roles(['Manager', ]):
            self.link = api.content.create(
                type='Link',
                container=self.portal,
                id='servico-1',
                title=u'Servico'
            )
            to_id = intids.getId(self.link)
            self.artigo = api.content.create(
                type='collective.nitf.content',
                container=self.portal,
                id='artigo',
                title=u'Artigo'
            )
            self.artigo.relatedItems = [RelationValue(to_id), ]

    def viewlet(self, context=None):
        if not context:
            context = self.artigo
        viewlet = RelatedItemsViewlet(context, self.request, None, None)
        viewlet.update()
        return viewlet

    def test_related(self):
        viewlet = self.viewlet()
        self.assertEqual(len(viewlet.related()), 1)

    def test_related_on_type_without_behavior(self):
        with api.env.adopt_roles(['Manager', ]):
            audio = api.content.create(
                type='Audio',
                container=self.portal,
                id='audio',
                title=u'Audio'
            )
            audio_file = api.content.create(
                type='MPEG Audio File',
                container=audio,
                id='file.mp3',
            )
        viewlet = self.viewlet(audio_file)
        self.assertEqual(len(viewlet.related()), 0)


class ServicosViewletTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
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
                id='servico-1',
                title=u'Servico 1'
            )
            api.content.create(
                type='Link',
                container=self.servicos,
                id='servico-2',
                title=u'Servico 2'
            )

    def viewlet(self):
        viewlet = ServicosViewlet(self.portal, self.request, None, None)
        viewlet.update()
        return viewlet

    def test_available(self):
        viewlet = self.viewlet()
        self.assertTrue(viewlet.available())

    def test_not_available(self):
        # Apagamos a pasta servicos
        api.content.delete(obj=self.portal['servicos'])
        viewlet = self.viewlet()
        self.assertFalse(viewlet.available())

    def test_servicos(self):
        viewlet = self.viewlet()
        servicos = viewlet.servicos()
        self.assertEqual(len(servicos), 2)
        self.assertEqual(servicos[0].Title, u'Servico 1')
        self.assertEqual(servicos[1].Title, u'Servico 2')


class NITFBylineViewletTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        with api.env.adopt_roles(['Manager', ]):
            properties = dict(
                fullname='Machado de Assis',
                location='Cosme Velho',
            )
            api.user.create(
                username='machado',
                email='machado@brasil.gov.br',
                properties=properties,
            )

            self.conteudo = api.content.create(
                type='collective.nitf.content',
                container=self.portal,
                id='minha-noticia'
            )
            self.conteudo.byline = u'Machado de Assis'

    def viewlet(self):
        viewlet = NITFBylineViewlet(self.conteudo, self.request, None, None)
        viewlet.update()
        return viewlet

    def test_autor_inexistente(self):
        self.conteudo.byline = u'Erico Verissimo'
        viewlet = self.viewlet()
        self.assertFalse(viewlet.byline())

    def test_byline(self):
        viewlet = self.viewlet()
        self.assertEqual(viewlet.byline(), 'machado')

    def test_author(self):
        viewlet = self.viewlet()
        author_data = viewlet.author()
        self.assertEqual(author_data.get('username'), 'machado')

    def test_authorname(self):
        viewlet = self.viewlet()
        self.assertEqual(viewlet.authorname(), u'Machado de Assis')
