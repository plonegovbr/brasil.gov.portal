# -*- coding: utf-8 -*-
from brasil.gov.portal.testing import INITCONTENT_TESTING
from plone import api
from plone.app.contenttypes.interfaces import IFolder
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.folder.default import DefaultOrdering
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes

import unittest


class InitContentTestCase(unittest.TestCase):

    layer = INITCONTENT_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.wt = self.portal.portal_workflow

    @unittest.expectedFailure
    def test_conteudos_publicados(self):
        ids = ['acessibilidade', 'acesso-a-sistemas', 'area-de-imprensa',
               'assuntos', 'audios', 'contato', 'destaques', 'eventos',
               'home', 'imagens', 'links', 'links-destaques',
               'menu-de-relevancia', 'noticias',
               'pastas-com-exemplos-de-pecas', 'rodape', 'rss', 'servicos',
               'acesso-a-informacao', 'videos']
        for oId in ids:
            o = self.portal[oId]
            self.assertEqual(self.wt.getInfoFor(o, 'review_state'),
                             'published')

    @unittest.expectedFailure
    def test_assuntos_available(self):
        self.assertTrue('assuntos' in self.portal.objectIds(),
                        u'Pasta Assuntos não disponível')
        pasta = self.portal['assuntos']
        self.assertEqual(u'Assuntos', pasta.title,
                         u'Título não aplicado')

    @unittest.expectedFailure
    def test_assuntos_ordering(self):
        pasta = self.portal['assuntos']
        ordering = pasta.getOrdering()
        oId = ordering.idsInOrder()[0]
        pasta.moveObjectsToBottom([oId])
        self.assertEqual(oId, pasta.objectIds()[-1],
                         u'Ordenação não aplicada')

    @unittest.expectedFailure
    def test_imagens_available(self):
        self.assertTrue('imagens' in self.portal.objectIds(),
                        u'Pasta Imagens não disponível')
        pasta = self.portal['imagens']
        self.assertEqual(u'Imagens', pasta.title,
                         u'Título não aplicado')

    @unittest.expectedFailure
    def test_imagens_constrains(self):
        pasta = self.portal['imagens']
        behavior = ISelectableConstrainTypes(pasta)
        types = ['Image']
        self.assertEqual(types, behavior.getImmediatelyAddableTypes())

    @unittest.expectedFailure
    def test_imagens_ordering(self):
        pasta = self.portal['imagens']
        ordering = pasta.getOrdering()
        oId = ordering.idsInOrder()[0]
        pasta.moveObjectsToBottom([oId])
        self.assertEqual(oId, pasta.objectIds()[-1],
                         u'Ordenação não aplicada')

    @unittest.expectedFailure
    def test_servicos_available(self):
        self.assertTrue('servicos' in self.portal.objectIds(),
                        u'Pasta Servicos não disponível')
        pasta = self.portal['servicos']
        self.assertEqual(u'Serviços', pasta.title,
                         u'Título não aplicado')

    @unittest.expectedFailure
    def test_servicos_constrains(self):
        pasta = self.portal['servicos']
        behavior = ISelectableConstrainTypes(pasta)
        types = ['Link']
        self.assertEqual(types, behavior.getImmediatelyAddableTypes())

    @unittest.expectedFailure
    def test_acesso_a_informacao_available(self):
        self.assertTrue('acesso-a-informacao' in self.portal.objectIds(),
                        u'Conheça este órgão')
        pasta = self.portal['acesso-a-informacao']
        self.assertEqual(u'Acesso à Informação', pasta.title,
                         u'Título não aplicado')

    @unittest.expectedFailure
    def test_acesso_a_informacao_ordering(self):
        pasta = self.portal['acesso-a-informacao']
        ordering = pasta.getOrdering()
        oId = ordering.idsInOrder()[0]
        pasta.moveObjectsToBottom([oId])
        self.assertEqual(oId, pasta.objectIds()[-1],
                         u'Ordenação não aplicada')

    def test_folders_in_root_are_plone_default_ordering(self):
        """
        Após a ordenação de pastas no upgradeStep 10600 complementando o 5000,
        para que todos os diretórios do root tenham a ordenação default do
        Plone, é preciso garantir esse comportamento em todos os diretórios.

        Esse teste hoje não retorna nada, é para garantir que, caso no futuro

        self.applyProfile(portal, 'brasil.gov.portal:initcontent')

        por exemplo seja utilizado em testing.py e que algum diretório criado
        na raiz dessa forma não tenha a ordenação padrão.
        """
        all_ordered = all([
            isinstance(self.portal[pasta_id].getOrdering(), DefaultOrdering)
            for pasta_id in self.portal.objectIds()
            if IFolder.providedBy(self.portal[pasta_id])
        ])
        self.assertTrue(all_ordered)

    @unittest.expectedFailure
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

    @unittest.expectedFailure
    def test_portlet_menu_de_relevancia(self):
        portal = self.portal
        # Coluna da esquerda
        coluna = '++contextportlets++plone.leftcolumn'
        mapping = portal.restrictedTraverse(coluna)
        # Menu de Relevancia
        self.assertEqual(mapping['relevancia'].root, u'/menu-de-relevancia')
        self.assertEqual(mapping['relevancia'].name, u'')
        self.assertEqual(mapping['relevancia'].currentFolderOnly, False)

    @unittest.expectedFailure
    def test_portlet_assuntos(self):
        portal = self.portal
        # Coluna da esquerda
        coluna = '++contextportlets++plone.leftcolumn'
        mapping = portal.restrictedTraverse(coluna)
        # Assuntos
        self.assertEqual(mapping['assuntos'].root, u'/assuntos')
        self.assertEqual(mapping['assuntos'].name, u'Assuntos')
        self.assertEqual(mapping['assuntos'].currentFolderOnly, False)

    @unittest.expectedFailure
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

    def test_portal_available(self):
        qi = api.portal.get_tool('portal_quickinstaller')
        installed = [p.get('id') for p in qi.listInstalledProducts()]
        p = 'brasil.gov.portal'
        self.assertIn(p, qi)
        self.assertIn(p, installed)

    @unittest.expectedFailure
    def test_eventos_available(self):
        """Testa se a pasta Eventos foi criada"""
        self.assertIn('eventos',
                      self.portal.objectIds(),
                      u'Pasta Eventos não disponível')
        folder = self.portal['eventos']
        self.assertEqual(u'Eventos', folder.title, u'Título não aplicado')

    @unittest.expectedFailure
    def test_eventos_created(self):
        """Testa se os eventos foram criados corretamente"""
        folder = self.portal['eventos']
        # As datas aqui tem 2 horas a mais por causa do timezone
        eventos = [{'id': 'evento-1',
                    'start': '2017-01-01 10:00:00',
                    'end': '2017-01-01 11:00:00'},
                   {'id': 'evento-2',
                    'start': '2017-01-05 11:00:00',
                    'end': '2017-01-06 12:00:00'},
                   {'id': 'evento-3',
                    'start': '2017-01-10 12:00:00',
                    'end': '2017-01-11 13:00:00'},
                   ]
        d_format = '%Y-%m-%d %H:%M:%S'
        for evento in eventos:
            obj_evento = folder[evento['id']]
            self.assertEqual(
                evento['start'], obj_evento.start.strftime(d_format))
            self.assertEqual(
                evento['end'], obj_evento.end.strftime(d_format))
            self.assertEqual('America/Sao_Paulo', obj_evento.timezone)
