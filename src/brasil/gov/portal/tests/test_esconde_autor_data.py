# -*- coding: utf-8 -*-
"""Testes da funcionalidade de esconder autor e data."""
from brasil.gov.portal.config import LOCAL_TIME_FORMAT
from brasil.gov.portal.testing import FUNCTIONAL_TESTING
from brasil.gov.portal.tests.test_viewlets import esconde_autor
from brasil.gov.portal.tests.test_viewlets import esconde_data
from DateTime import DateTime
from plone import api
from plone.testing.z2 import Browser
from zope.component import getMultiAdapter

import transaction
import unittest


ID_OBJ = 'objeto'
ID_PAGINA = 'pagina'


class EscondeAutorDataFunctionalTestCase(unittest.TestCase):
    """Testa a funcionalidade de esconder autor e data em templates que não
    utilizam a viewlet documentbyline."""

    layer = FUNCTIONAL_TESTING

    def setUp(self):
        """Configura testes funcionais antes de cada teste."""
        self.portal = self.layer['portal']
        self.wt = api.portal.get_tool('portal_workflow')
        self.pas_member = getMultiAdapter((self.portal, self.portal.REQUEST),
                                          name='pas_member')
        self.portal_url = self.portal.absolute_url()
        esconde_autor()
        esconde_data()
        self.browser = Browser(self.layer['app'])
        transaction.commit()

    def cria_conteudo(self, container, tipo, id_obj, title):
        """Cria e publica um conteúdo, retornando o objeto criado."""
        with api.env.adopt_roles(['Manager']):
            obj = api.content.create(
                type=tipo,
                container=container,
                id=id_obj,
                title=title,
            )
            self.wt.doActionFor(obj, 'publish')
            effective = DateTime()
            obj.setEffectiveDate(effective)
            obj.reindexObject()
        return obj

    def cria_pasta(self):
        """Cria uma pasta com uma página dentro, retornando a página."""
        pasta = self.cria_conteudo(self.portal, 'Folder', ID_OBJ, u'Pasta')
        pagina = self.cria_conteudo(pasta, 'Document', ID_PAGINA, u'Pagina')
        transaction.commit()
        return pagina

    def cria_colecao(self):
        """Cria uma coleção de páginas. Também cria uma página para alimentar
        a coleção e retorna essa página."""
        colecao = self.cria_conteudo(self.portal,
                                     'Collection',
                                     ID_OBJ,
                                     u'Coleção')
        colecao.sort_on = u'effective'
        colecao.query = [
            {'i': u'portal_type',
             'o': u'plone.app.querystring.operation.selection.is',
             'v': [u'Document'],
             },
            {'i': u'review_state',
             'o': u'plone.app.querystring.operation.selection.is',
             'v': [u'published'],
             },
        ]
        pagina = self.cria_conteudo(self.portal,
                                    'Document',
                                    ID_PAGINA,
                                    u'Pagina')
        transaction.commit()
        return pagina

    def base_teste_data(self, obj, contents):
        """Testa que a data de publicação e a data de modificação não aparecem
         na página."""
        datas = (obj.effective(), obj.modified())
        for data in datas:
            self.assertNotEqual('None', data)
            self.assertNotIn(data.strftime(LOCAL_TIME_FORMAT), contents)
        self.assertNotIn('última', contents)
        self.assertNotIn('Modificado', contents)

    def base_teste_autor(self, obj, contents):
        """Testa que o autor não aparece na página."""
        creator = obj.Creator()
        autor = self.pas_member.info(creator)
        # Testa nome
        self.assertNotIn('{0}<'.format(autor['name_or_id']), contents)
        self.assertNotIn('{0},'.format(autor['name_or_id']), contents)
        # Testa creator
        self.assertNotIn('{0}<'.format(creator), contents)
        self.assertNotIn('{0},'.format(creator), contents)

    def base_teste_esconde_autor_data(self, template, obj):
        """Teste base para template em pasta ou coleção."""
        self.browser.open('{0}/{1}/{2}'.format(self.portal.absolute_url(),
                                               ID_OBJ,
                                               template))
        contents = self.browser.contents
        self.assertIn('Pagina', contents)
        # testa esconde autor
        self.base_teste_autor(obj, contents)
        # testa esconde data
        self.base_teste_data(obj, contents)

    def base_teste_esconde_autor_data_root(self, template, obj):
        """Teste base para template no root do portal."""
        self.browser.open('{0}/{1}'.format(self.portal.absolute_url(),
                                           template))
        contents = self.browser.contents
        self.assertIn('Pagina', contents)
        # testa esconde autor
        self.base_teste_autor(obj, contents)
        # testa esconde data
        self.base_teste_data(obj, contents)

    def test_collection_summary_view(self):
        """Testa se o autor e a data são escondidos no summary_view da
        Coleção."""
        obj = self.cria_colecao()
        self.base_teste_esconde_autor_data('summary_view', obj)

    def test_pasta_summary_view(self):
        """Testa se o autor e a data são escondidos no summary_view de
        Pastas."""
        obj = self.cria_pasta()
        self.base_teste_esconde_autor_data('summary_view', obj)

    def test_busca(self):
        """Testa se o autor e a data são escondidos na página resultado de
        busca."""
        obj = self.cria_pasta()
        self.base_teste_esconde_autor_data('@@busca?SearchableText=Pagina',
                                           obj)

    def test_listing_view(self):
        """Testa se o autor e a data são escondidos no listing_view."""
        obj = self.cria_pasta()
        self.base_teste_esconde_autor_data('listing_view', obj)

    def test_collection_listing_view(self):
        """Testa se o autor e a data são escondidos no listing_view da
        Coleção."""
        obj = self.cria_colecao()
        self.base_teste_esconde_autor_data('listing_view', obj)

    def test_pasta_tabular_view(self):
        """Testa se o autor e a data são escondidos no tabular_view da
        Pasta."""
        obj = self.cria_pasta()
        self.base_teste_esconde_autor_data('tabular_view', obj)

    def test_recently_modified(self):
        """Testa se o autor e a data são escondidos no recently_modified."""
        obj = self.cria_pasta()
        self.base_teste_esconde_autor_data_root('recently_modified', obj)

    def test_recently_published(self):
        """Testa se o autor e a data são escondidos no recently_published."""
        obj = self.cria_pasta()
        self.base_teste_esconde_autor_data_root('recently_published', obj)
