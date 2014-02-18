# -*- coding: utf-8 -*-

from brasil.gov.portal.testing import INITCONTENT_TESTING
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
        ids = ['acessibilidade', 'acesso-a-sistemas', 'area-imprensa',
               'assuntos', 'audios', 'contato', 'destaques', 'eventos',
               'home', 'imagens', 'links', 'links-destaques', 'menu-de-apoio',
               'noticias', 'pastas-com-exemplos-de-pecas', 'rodape', 'rss',
               'servicos', 'sobre', 'videos']
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

    def test_sobre_available(self):
        self.assertTrue('sobre' in self.portal.objectIds(),
                        u'Conheça este órgão')
        pasta = self.portal['sobre']
        self.assertEqual(u'Sobre', pasta.title,
                         u'Título não aplicado')

    def test_default_portlets(self):
        # Os portlets estao configurados corretamente?
        portal = self.portal
        # Coluna da esquerda
        coluna = '++contextportlets++plone.leftcolumn'
        mapping = portal.restrictedTraverse(coluna)
        self.assertEqual(len(mapping.keys()), 3)
        self.assertTrue('assuntos' in mapping.keys())
        self.assertTrue('sobre' in mapping.keys())
        self.assertTrue('apoio' in mapping.keys())

    def test_portlet_menu_apoio(self):
        portal = self.portal
        # Coluna da esquerda
        coluna = '++contextportlets++plone.leftcolumn'
        mapping = portal.restrictedTraverse(coluna)
        # Menu de Apoio
        self.assertEqual(mapping['apoio'].root, u'/menu-de-apoio')
        self.assertEqual(mapping['apoio'].name, u'')
        self.assertEqual(mapping['apoio'].currentFolderOnly, False)

    def test_portlet_assuntos(self):
        portal = self.portal
        # Coluna da esquerda
        coluna = '++contextportlets++plone.leftcolumn'
        mapping = portal.restrictedTraverse(coluna)
        # Assuntos
        self.assertEqual(mapping['assuntos'].root, u'/assuntos')
        self.assertEqual(mapping['assuntos'].name, u'Assuntos')
        self.assertEqual(mapping['assuntos'].currentFolderOnly, False)

    def test_portlet_sobre(self):
        portal = self.portal
        # Coluna da esquerda
        coluna = '++contextportlets++plone.leftcolumn'
        mapping = portal.restrictedTraverse(coluna)
        # Sobre
        self.assertEqual(mapping['sobre'].root,
                         u'/sobre')
        self.assertEqual(mapping['sobre'].name,
                         u'Sobre')
        self.assertEqual(mapping['sobre'].currentFolderOnly,
                         False)
