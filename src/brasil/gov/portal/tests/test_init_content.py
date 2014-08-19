# -*- coding: utf-8 -*-
from brasil.gov.portal.config import SHOW_DEPS
from brasil.gov.portal.testing import INITCONTENT_TESTING
from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes

import unittest


class InitContentTestCase(unittest.TestCase):

    layer = INITCONTENT_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.wt = self.portal.portal_workflow

    def test_conteudos_publicados(self):
        ids = ['acessibilidade', 'acesso-a-sistemas', 'area-de-imprensa',
               'assuntos', 'audios', 'contato', 'destaques', 'eventos',
               'home', 'imagens', 'links', 'links-destaques', 'menu-de-relevancia',
               'noticias', 'pastas-com-exemplos-de-pecas', 'rodape', 'rss',
               'servicos', 'acesso-a-informacao', 'videos']
        for oId in ids:
            o = self.portal[oId]
            self.assertEqual(self.wt.getInfoFor(o, 'review_state'),
                             'published')

    def test_assuntos_available(self):
        self.assertTrue('assuntos' in self.portal.objectIds(),
                        u'Pasta Assuntos não disponível')
        pasta = self.portal['assuntos']
        self.assertEqual(u'Assuntos', pasta.title,
                         u'Título não aplicado')

    def test_assuntos_ordering(self):
        pasta = self.portal['assuntos']
        ordering = pasta.getOrdering()
        oId = ordering.idsInOrder()[0]
        pasta.moveObjectsToBottom([oId])
        self.assertEqual(oId, pasta.objectIds()[-1],
                         u'Ordenação não aplicada')

    def test_imagens_available(self):
        self.assertTrue('imagens' in self.portal.objectIds(),
                        u'Pasta Imagens não disponível')
        pasta = self.portal['imagens']
        self.assertEqual(u'Imagens', pasta.title,
                         u'Título não aplicado')

    def test_imagens_constrains(self):
        pasta = self.portal['imagens']
        behavior = ISelectableConstrainTypes(pasta)
        types = ['Image']
        self.assertEqual(types, behavior.getImmediatelyAddableTypes())

    def test_imagens_ordering(self):
        pasta = self.portal['imagens']
        ordering = pasta.getOrdering()
        oId = ordering.idsInOrder()[0]
        pasta.moveObjectsToBottom([oId])
        self.assertEqual(oId, pasta.objectIds()[-1],
                         u'Ordenação não aplicada')

    def test_servicos_available(self):
        self.assertTrue('servicos' in self.portal.objectIds(),
                        u'Pasta Servicos não disponível')
        pasta = self.portal['servicos']
        self.assertEqual(u'Serviços', pasta.title,
                         u'Título não aplicado')

    def test_servicos_constrains(self):
        pasta = self.portal['servicos']
        behavior = ISelectableConstrainTypes(pasta)
        types = ['Link']
        self.assertEqual(types, behavior.getImmediatelyAddableTypes())

    def test_acesso_a_informacao_available(self):
        self.assertTrue('acesso-a-informacao' in self.portal.objectIds(),
                        u'Conheça este órgão')
        pasta = self.portal['acesso-a-informacao']
        self.assertEqual(u'Acesso à Informação', pasta.title,
                         u'Título não aplicado')

    def test_acesso_a_informacao_ordering(self):
        pasta = self.portal['acesso-a-informacao']
        ordering = pasta.getOrdering()
        oId = ordering.idsInOrder()[0]
        pasta.moveObjectsToBottom([oId])
        self.assertEqual(oId, pasta.objectIds()[-1],
                         u'Ordenação não aplicada')

    def test_default_portlets(self):
        # Os portlets estao configurados corretamente?
        portal = self.portal
        # Coluna da esquerda
        coluna = '++contextportlets++plone.leftcolumn'
        mapping = portal.restrictedTraverse(coluna)
        self.assertEqual(len(mapping.keys()), 3)
        self.assertTrue('assuntos' in mapping.keys())
        self.assertTrue('acesso-a-informacao' in mapping.keys())
        self.assertTrue('relevancia' in mapping.keys())

    def test_portlet_menu_de_relevancia(self):
        portal = self.portal
        # Coluna da esquerda
        coluna = '++contextportlets++plone.leftcolumn'
        mapping = portal.restrictedTraverse(coluna)
        # Menu de Relevancia
        self.assertEqual(mapping['relevancia'].root, u'/menu-de-relevancia')
        self.assertEqual(mapping['relevancia'].name, u'')
        self.assertEqual(mapping['relevancia'].currentFolderOnly, False)

    def test_portlet_assuntos(self):
        portal = self.portal
        # Coluna da esquerda
        coluna = '++contextportlets++plone.leftcolumn'
        mapping = portal.restrictedTraverse(coluna)
        # Assuntos
        self.assertEqual(mapping['assuntos'].root, u'/assuntos')
        self.assertEqual(mapping['assuntos'].name, u'Assuntos')
        self.assertEqual(mapping['assuntos'].currentFolderOnly, False)

    def test_portlet_acesso_a_informacao(self):
        portal = self.portal
        # Coluna da esquerda
        coluna = '++contextportlets++plone.leftcolumn'
        mapping = portal.restrictedTraverse(coluna)
        # acesso-a-informacao
        self.assertEqual(mapping['acesso-a-informacao'].root,
                         u'/acesso-a-informacao')
        self.assertEqual(mapping['acesso-a-informacao'].name,
                         u'Acesso à Informação')
        self.assertEqual(mapping['acesso-a-informacao'].currentFolderOnly,
                         False)

    def test_doormat_view(self):
        from brasil.gov.portal.browser.content.doormat import DoormatView
        portal = self.portal
        request = self.layer['request']
        view = DoormatView(portal['rodape'], request)
        data = view.getDoormatData()
        # Teste se a troca de {portal_url} e {navigation_root_url}
        # esta sendo realizada
        self.assertEqual(
            data[0]['column_sections'][0]['section_links'][1]['link_url'],
            'http://nohost/plone/assuntos/lorem-ipsum'
        )

    def test_portal_available(self):
        qi = api.portal.get_tool('portal_quickinstaller')
        installed = [p.get('id') for p in qi.listInstalledProducts()]
        p = 'brasil.gov.portal'
        self.assertIn(p, qi)
        self.assertIn(p, installed)

    def test_installed_packages(self):
        qi = api.portal.get_tool('portal_quickinstaller')
        installed = [p.get('id') for p in qi.listInstalledProducts()]
        for p in SHOW_DEPS:
            self.assertIn(p, qi)
            self.assertIn(p, installed)
