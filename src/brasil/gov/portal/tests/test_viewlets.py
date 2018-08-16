# -*- coding: utf-8 -*-
from brasil.gov.portal.browser.viewlets.content import DocumentBylineViewlet
from brasil.gov.portal.browser.viewlets.logo import LogoViewlet
from brasil.gov.portal.browser.viewlets.nitf_byline import NITFBylineViewlet
from brasil.gov.portal.browser.viewlets.redes import RedesSociaisViewlet
from brasil.gov.portal.browser.viewlets.servicos import ServicosViewlet
from brasil.gov.portal.testing import INTEGRATION_TESTING
from plone import api
from plone.app.layout.globals.interfaces import IViewView
from zope.interface import implementer

import unittest


def esconde_autor():
    """Seta a configuração esconde_autor para True"""
    record = \
        'brasil.gov.portal.controlpanel.portal.ISettingsPortal.esconde_autor'
    api.portal.set_registry_record(record, True)


def esconde_data():
    """Seta a configuração esconde_data para True"""
    record = \
        'brasil.gov.portal.controlpanel.portal.ISettingsPortal.esconde_data'
    api.portal.set_registry_record(record, True)


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
        with api.env.adopt_roles(['Manager']):
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


class ServicosViewletTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
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
                id='servico-1',
                title=u'Servico 1',
                remoteUrl=u'http://www.google.com',
            )
            api.content.create(
                type='Link',
                container=self.servicos,
                id='servico-2',
                title=u'Servico 2',
                remoteUrl=u'http://www.plone.org',
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

    def test_render(self):
        viewlet = self.viewlet()
        render = viewlet.render()
        self.assertIn(u'http://www.google.com', render)
        self.assertIn(u'http://www.plone.org', render)


class NITFBylineViewletTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        with api.env.adopt_roles(['Manager']):
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
                id='minha-noticia',
            )
            self.conteudo.byline = u'Machado de Assis'

    def viewlet(self):
        viewlet = NITFBylineViewlet(self.conteudo, self.request, None, None)
        viewlet.update()
        return viewlet

    def test_autor_inexistente(self):
        self.conteudo.byline = u'Erico Verissimo'
        viewlet = self.viewlet()
        self.assertFalse(viewlet.author_id)

    def test_autor_indefinido(self):
        viewlet = self.viewlet()
        original_search_member_by_name = viewlet.search_member_by_name
        viewlet.search_member_by_name = lambda x: {'username': 'mock_user'}

        # Assegura que 'search_member_by_name' é chamada para um autor qualquer
        self.conteudo.byline = u'Usuário Qualquer'
        self.assertEqual(viewlet.author_id, 'mock_user')

        # Assegura que 'search_member_by_name' NÃO é chamada sem um autor
        viewlet.search_member_by_name = original_search_member_by_name
        self.conteudo.byline = u''
        self.assertIsNone(viewlet.author_id)

    def test_byline(self):
        viewlet = self.viewlet()
        self.assertEqual(viewlet.author_id, 'machado')

    def test_author(self):
        viewlet = self.viewlet()
        author_data = viewlet.author()
        self.assertEqual(author_data.get('username'), 'machado')

    def test_authorname(self):
        viewlet = self.viewlet()
        self.assertEqual(viewlet.authorname(), u'Machado de Assis')

    def test_mostra_autor(self):
        """Testa se o método retorna configuração para esconder o autor."""
        viewlet = self.viewlet()
        self.assertTrue(viewlet.mostra_autor())
        esconde_autor()
        self.assertFalse(viewlet.mostra_autor())

    def test_mostra_data(self):
        """Testa se o método retorna configuração para esconder a data."""
        viewlet = self.viewlet()
        self.assertTrue(viewlet.mostra_data())
        esconde_data()
        self.assertFalse(viewlet.mostra_data())

    def test_esconde_autor(self):
        """Testa se o autor deixa de ser exibido se configuração para esconder
        o autor estiver marcada."""
        esconde_autor()
        viewlet = self.viewlet()
        render = viewlet.render()
        self.assertNotIn(self.conteudo.byline, render)

    def test_esconde_data(self):
        """Testa se a data deixa de ser exibida se configuração para esconder
        a data estiver marcada."""
        esconde_data()
        viewlet = self.viewlet()
        render = viewlet.render()
        modified = self.conteudo.ModificationDate()
        ano = modified[:4]
        dia = modified[8:10]
        self.assertNotIn(ano, render)
        self.assertNotIn(dia, render)


class DocumentBylineViewletTestCase(unittest.TestCase):
    """Testes da viewlet customizada DocumentBylineViewlet."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        """Cria uma página para testes."""
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        with api.env.adopt_roles(['Manager']):
            self.conteudo = api.content.create(
                type='Document',
                container=self.portal,
                id='minha-pagina',
            )

    def viewlet(self):
        """Retorna a viewlet DocumentBylineViewlet."""
        viewlet = DocumentBylineViewlet(self.conteudo,
                                        self.request,
                                        None,
                                        None)

        @implementer(IViewView)
        class Parent(object):
            """Classe que simula um parent. Para que a viewlet
            DocumentBylineViewletTestCase exiba o histórico, é necessário que
            o seu __parent__ implemente a interface IViewView"""

        viewlet.__parent__ = Parent()
        viewlet.update()
        return viewlet

    def test_mostra_autor(self):
        """Testa se o método retorna configuração para esconder o autor."""
        viewlet = self.viewlet()
        self.assertTrue(viewlet.mostra_autor())
        esconde_autor()
        self.assertFalse(viewlet.mostra_autor())

    def test_mostra_data(self):
        """Testa se o método retorna configuração para esconder a data."""
        viewlet = self.viewlet()
        self.assertTrue(viewlet.mostra_data())
        esconde_data()
        self.assertFalse(viewlet.mostra_data())

    def test_esconde_autor(self):
        """Testa se o autor deixa de ser exibido se configuração para esconder
        o autor estiver marcada."""
        esconde_autor()
        viewlet = self.viewlet()
        render = viewlet.render()
        self.assertNotIn(self.conteudo.Creator(), render)

    def test_esconde_data(self):
        """Testa se a data deixa de ser exibida se configuração para esconder
        a data estiver marcada."""
        esconde_data()
        viewlet = self.viewlet()
        render = viewlet.render()
        modified = self.conteudo.ModificationDate()
        ano = modified[:4]
        dia = modified[8:10]
        self.assertNotIn(ano, render)
        self.assertNotIn(dia, render)

    def test_exibe_tracos(self):
        """Confirma que a viewlet não está exibindo dois traços, quando a data
        não é exibida ou quando nem a data nem o autor são exibidos.

        Para que esse teste seja efetivo, é necessário que a
        viewlet exiba o histórico, pois um dos traços vem do histórico. Para
        que o hitórico seja exibido, o teste tem que ser feito com usuário
        Manager e o atributo __parent__ da viewlet tem implementar a interface
        IViewView. Ver método 'viewlet'"""
        with api.env.adopt_roles(['Manager']):
            esconde_data()
            viewlet = self.viewlet()
            render = viewlet.render()
            self.assertEqual(render.count(u'—'), 1)
            esconde_autor()
            render = viewlet.render()
            self.assertEqual(render.count(u'—'), 0)


class SearchBoxViewletTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    @staticmethod
    def set_expandable_header(value):
        from brasil.gov.portal.controlpanel.portal import ISettingsPortal
        name = ISettingsPortal.__identifier__ + '.expandable_header'
        api.portal.set_registry_record(name, value=value)

    @staticmethod
    def set_image(value):
        from brasil.gov.portal.controlpanel.portal import ISettingsPortal
        name = ISettingsPortal.__identifier__ + '.background_image'
        api.portal.set_registry_record(name, value=value)

    def test_no_expandable_header(self):
        rendered = self.portal()
        self.assertNotIn('expandable-header', rendered)
        self.assertNotIn('@@searchbox-background-image', rendered)
        self.assertNotIn('search-suggestions', rendered)

    def test_expandable_header(self):
        self.set_expandable_header(True)
        rendered = self.portal()
        self.assertIn('expandable-header', rendered)
        self.assertNotIn('@@searchbox-background-image', rendered)
        self.assertIn('search-suggestions', rendered)

        from brasil.gov.portal.tests.test_helper_view import IMAGEB64
        self.set_image(IMAGEB64)
        rendered = self.portal()
        self.assertIn('@@searchbox-background-image', rendered)
