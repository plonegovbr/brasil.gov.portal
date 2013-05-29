# -*- coding: utf-8 -*-

from brasil.gov.portal.testing import INTEGRATION_TESTING
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes

import unittest


class InitContentTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        profile = 'profile-brasil.gov.portal:initcontent'
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        wf = self.portal.portal_workflow
        wf.setDefaultChain('simple_publication_workflow')
        types = ('Document', 'Folder', 'Link', 'Topic', 'News Item')
        wf.setChainForPortalTypes(types, '(Default)')
        self.st = self.portal.portal_setup
        self.st.runAllImportStepsFromProfile(profile)
        self.wt = self.portal.portal_workflow

    def test_assuntos_available(self):
        self.assertTrue('assuntos' in self.portal.objectIds(),
                        u'Pasta Assuntos não disponível')
        pasta = self.portal['assuntos']
        self.assertEqual(u'Assuntos', pasta.title,
                         u'Título não aplicado')
        self.assertEqual(self.wt.getInfoFor(pasta, 'review_state'),
                         'published')

    def test_imagens_available(self):
        self.assertTrue('imagens' in self.portal.objectIds(),
                        u'Pasta Imagens não disponível')
        pasta = self.portal['imagens']
        self.assertEqual(u'Imagens', pasta.title,
                         u'Título não aplicado')
        self.assertEqual(self.wt.getInfoFor(pasta, 'review_state'),
                         'published')

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
        self.assertEqual(self.wt.getInfoFor(pasta, 'review_state'),
                         'published')

    def test_servicos_constrains(self):
        pasta = self.portal['servicos']
        behavior = ISelectableConstrainTypes(pasta)
        types = ['Link']
        self.assertEqual(types, behavior.getImmediatelyAddableTypes())

    def test_acesso_available(self):
        self.assertTrue('acesso-a-informacao' in self.portal.objectIds(),
                        u'Pasta Acesso à Informação não disponível')
        pasta = self.portal['acesso-a-informacao']
        self.assertEqual(u'Acesso à informação', pasta.title,
                         u'Título não aplicado')
        self.assertEqual(self.wt.getInfoFor(pasta, 'review_state'),
                         'published')

    def test_default_portlets(self):
        # Os portlets estao configurados corretamente?
        portal = self.portal
        # Coluna da esquerda
        coluna = '++contextportlets++plone.leftcolumn'
        mapping = portal.restrictedTraverse(coluna)
        self.assertEqual(len(mapping.keys()), 3)
        self.assertTrue('assuntos' in mapping.keys())
        self.assertTrue('acesso-a-informacao' in mapping.keys())
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

    def test_portlet_acesso(self):
        portal = self.portal
        # Coluna da esquerda
        coluna = '++contextportlets++plone.leftcolumn'
        mapping = portal.restrictedTraverse(coluna)
        # Sobre
        self.assertEqual(mapping['acesso-a-informacao'].root,
                         u'/acesso-a-informacao')
        self.assertEqual(mapping['acesso-a-informacao'].name,
                         u'Acesso à Informação')
        self.assertEqual(mapping['acesso-a-informacao'].currentFolderOnly,
                         False)
