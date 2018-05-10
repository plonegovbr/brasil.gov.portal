# -*- coding: utf-8 -*-
from brasil.gov.portal.browser.album.albuns import Pagination
from brasil.gov.portal.config import LOCAL_TIME_FORMAT
from brasil.gov.portal.config import TIME_FORMAT
from brasil.gov.portal.testing import INTEGRATION_TESTING
from DateTime import DateTime
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.testing.z2 import Browser
from plonetheme.sunburst.browser.interfaces import IThemeSpecific
from zope.interface import alsoProvides

import transaction
import unittest


class BaseViewTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.browser = Browser(self.layer['app'])
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        with api.env.adopt_roles(['Manager']):
            self.folder = api.content.create(self.portal, 'Folder', 'folder')


class PaginationTestCase(BaseViewTestCase):

    def setUp(self):
        super(PaginationTestCase, self).setUp()

    def _get_pagination(self, total_items=0, current_page=1):
        pagination = Pagination(self.folder,
                                self.request,
                                'Folder')
        pagination._calc_page_items(current_page)
        pagination._calc_total_items(total_items)

        return pagination

    def test_pagination(self):
        pagination = self._get_pagination()

        self.assertEqual(pagination.items_by_page, 9)
        self.assertEqual(pagination.items_by_line, 3)
        self.assertEqual(pagination.pages_visible, 7)

    def test_pagination_noitems(self):
        pagination = self._get_pagination()

        self.assertEqual(pagination.current_page, 1)
        self.assertEqual(pagination.first_item, 0)
        self.assertEqual(pagination.last_item, 9)
        self.assertEqual(pagination.total_items, 0)
        self.assertEqual(pagination.total_pages, 0)
        self.assertEqual(pagination.get_pagination(), [])

    def test_pagination_manyitems_begin(self):
        pagination = self._get_pagination(100)

        self.assertEqual(pagination.current_page, 1)
        self.assertEqual(pagination.first_item, 0)
        self.assertEqual(pagination.last_item, 9)
        self.assertEqual(pagination.total_items, 100)
        self.assertEqual(pagination.total_pages, 12)
        self.assertEqual(pagination.get_pagination(), PAGINATION_BEGIN)

    def test_pagination_manyitems_middle(self):
        pagination = self._get_pagination(100, 5)

        self.assertEqual(pagination.current_page, 5)
        self.assertEqual(pagination.first_item, 36)
        self.assertEqual(pagination.last_item, 45)
        self.assertEqual(pagination.total_items, 100)
        self.assertEqual(pagination.total_pages, 12)
        self.assertEqual(pagination.get_pagination(), PAGINATION_MIDDLE)

    def test_pagination_manyitems_end(self):
        pagination = self._get_pagination(100, 12)

        self.assertEqual(pagination.current_page, 12)
        self.assertEqual(pagination.first_item, 99)
        self.assertEqual(pagination.last_item, 108)
        self.assertEqual(pagination.total_items, 100)
        self.assertEqual(pagination.total_pages, 12)
        self.assertEqual(pagination.get_pagination(), PAGINATION_END)


class GaleriaDeAlbunsTestCase(BaseViewTestCase):

    def setUp(self):
        super(GaleriaDeAlbunsTestCase, self).setUp()
        alsoProvides(self.request, IThemeSpecific)
        self.view = api.content.get_view(u'galeria_de_albuns',
                                         self.folder,
                                         self.request)

    def test_album_total_images(self):
        with api.env.adopt_roles(['Manager']):
            gal_fotos = api.content.create(self.folder, 'Folder', 'gal_fotos')
            self.assertEqual(self.view.album_total_images(gal_fotos), 0)

            api.content.create(gal_fotos, 'Image', 'imagem')
            self.assertEqual(self.view.album_total_images(gal_fotos), 1)

            for i in xrange(3):
                api.content.create(gal_fotos, 'Image', 'imagem{0}'.format(i))
            self.assertEqual(self.view.album_total_images(gal_fotos), 4)

    def test_album_date(self):
        self.folder.setEffectiveDate(DateTime(2014, 1, 1, 0, 0))
        self.assertEqual(self.view.album_date(self.folder), u'Jan 01, 2014')

        self.folder.setEffectiveDate(DateTime(2013, 1, 31, 15, 38))
        self.assertEqual(self.view.album_date(self.folder), u'Jan 31, 2013')

        self.folder.setEffectiveDate(DateTime(2014, 1, 21, 15, 38))
        self.assertEqual(self.view.album_date(self.folder), u'Jan 21, 2014')

    def test_album_thumbnail(self):
        with api.env.adopt_roles(['Manager']):
            gal_fotos = api.content.create(self.folder, 'Folder', 'gal_fotos')
            image = api.content.create(gal_fotos, 'Image', 'imagem')
            image.setDescription('test_description')

        thumb_test = {
            'src': 'http://nohost/plone/folder/gal_fotos/imagem',
            'alt': 'test_description',
        }

        self.assertEqual(self.view.thumbnail(gal_fotos), thumb_test)


class GaleriaDeFotosTestCase(BaseViewTestCase):

    def setUp(self):
        super(GaleriaDeFotosTestCase, self).setUp()
        alsoProvides(self.request, IThemeSpecific)
        self.view = api.content.get_view(u'galeria_de_fotos',
                                         self.folder,
                                         self.request)

    def test_view_items(self):
        with api.env.adopt_roles(['Manager']):
            image = api.content.create(self.folder, 'Image', 'imagem')
        self.view.setup()

        self.assertEqual(len(self.view.items), 1)
        self.assertEqual(self.view.items[0]['obj'], image)
        import Missing
        self.assertEqual(self.view.items[0]['size'], Missing.Value)


PAGINATION_BEGIN = [
    {
        'class': 'atual',
        'content': '1',
        'href': '?pagina=1',
        'is_next': False,
        'is_prev': False,
        'link': False,
    },
    {
        'class': 'pagina',
        'content': '2',
        'href': '?pagina=2',
        'is_next': False,
        'is_prev': False,
        'link': True,
    },
    {
        'class': 'pagina',
        'content': '3',
        'href': '?pagina=3',
        'is_next': False,
        'is_prev': False,
        'link': True,
    },
    {
        'class': 'pagina',
        'content': '4',
        'href': '?pagina=4',
        'is_next': False,
        'is_prev': False,
        'link': True,
    },
    {
        'class': 'pagina',
        'content': '5',
        'href': '?pagina=5',
        'is_next': False,
        'is_prev': False,
        'link': True,
    },
    {
        'class': 'pagina',
        'content': '6',
        'href': '?pagina=6',
        'is_next': False,
        'is_prev': False,
        'link': True,
    },
    {
        'class': 'pagina',
        'content': '7',
        'href': '?pagina=7',
        'is_next': False,
        'is_prev': False,
        'link': True,
    },
    {
        'class': 'reticencias',
        'content': '...',
        'href': '',
        'is_next': False,
        'is_prev': False,
        'link': False,
    },
    {
        'class': 'pagina',
        'content': '12',
        'href': '?pagina=12',
        'is_next': False,
        'is_prev': False,
        'link': True,
    },
    {
        'class': 'proximo',
        'content': u'label_next',
        'href': '?pagina=2',
        'is_next': True,
        'is_prev': False,
        'link': True,
    },
]

PAGINATION_MIDDLE = [
    {
        'class': 'anterior',
        'content': u'label_previous',
        'href': '?pagina=4',
        'is_next': False,
        'is_prev': True,
        'link': True},
    {
        'class': 'pagina',
        'content': '1',
        'href': '?pagina=1',
        'is_next': False,
        'is_prev': False,
        'link': True},
    {
        'class': 'pagina',
        'content': '2',
        'href': '?pagina=2',
        'is_next': False,
        'is_prev': False,
        'link': True},
    {
        'class': 'pagina',
        'content': '3',
        'href': '?pagina=3',
        'is_next': False,
        'is_prev': False,
        'link': True},
    {
        'class': 'pagina',
        'content': '4',
        'href': '?pagina=4',
        'is_next': False,
        'is_prev': False,
        'link': True},
    {
        'class': 'atual',
        'content': '5',
        'href': '?pagina=5',
        'is_next': False,
        'is_prev': False,
        'link': False},
    {
        'class': 'pagina',
        'content': '6',
        'href': '?pagina=6',
        'is_next': False,
        'is_prev': False,
        'link': True},
    {
        'class': 'pagina',
        'content': '7',
        'href': '?pagina=7',
        'is_next': False,
        'is_prev': False,
        'link': True,
    },
    {
        'class': 'reticencias',
        'content': '...',
        'href': '',
        'is_next': False,
        'is_prev': False,
        'link': False,
    },
    {
        'class': 'pagina',
        'content': '12',
        'href': '?pagina=12',
        'is_next': False,
        'is_prev': False,
        'link': True,
    },
    {
        'class': 'proximo',
        'content': u'label_next',
        'href': '?pagina=6',
        'is_next': True,
        'is_prev': False,
        'link': True,
    },
]

PAGINATION_END = [
    {
        'class': 'anterior',
        'content': u'label_previous',
        'href': '?pagina=11',
        'is_next': False,
        'is_prev': True,
        'link': True,
    },
    {
        'class': 'pagina',
        'content': '1',
        'href': '?pagina=1',
        'is_next': False,
        'is_prev': False,
        'link': True,
    },
    {
        'class': 'reticencias',
        'content': '...',
        'href': '',
        'is_next': False,
        'is_prev': False,
        'link': False,
    },
    {
        'class': 'pagina',
        'content': '6',
        'href': '?pagina=6',
        'is_next': False,
        'is_prev': False,
        'link': True,
    },
    {
        'class': 'pagina',
        'content': '7',
        'href': '?pagina=7',
        'is_next': False,
        'is_prev': False,
        'link': True,
    },
    {
        'class': 'pagina',
        'content': '8',
        'href': '?pagina=8',
        'is_next': False,
        'is_prev': False,
        'link': True,
    },
    {
        'class': 'pagina',
        'content': '9',
        'href': '?pagina=9',
        'is_next': False,
        'is_prev': False,
        'link': True,
    },
    {
        'class': 'pagina',
        'content': '10',
        'href': '?pagina=10',
        'is_next': False,
        'is_prev': False,
        'link': True,
    },
    {
        'class': 'pagina',
        'content': '11',
        'href': '?pagina=11',
        'is_next': False,
        'is_prev': False,
        'link': True,
    },
    {
        'class': 'atual',
        'content': '12',
        'href': '?pagina=12',
        'is_next': False,
        'is_prev': False,
        'link': False,
    },
]


class SummaryViewTestCase(BaseViewTestCase):

    def login_browser(self):
        """Autentica usuário de teste no browser"""
        setRoles(self.portal, TEST_USER_ID, ['Site Administrator'])
        self.browser.handleErrors = False
        basic_auth = 'Basic {0}'.format(
            '{0}:{1}'.format(TEST_USER_NAME, TEST_USER_PASSWORD))
        self.browser.addHeader('Authorization', basic_auth)

    def test_data_nao_pode_ser_1969_por_padrao_de_itens_criados(self):
        with api.env.adopt_roles(['Manager']):
            obj = api.content.create(
                type='collective.nitf.content',
                container=self.portal['folder'],
                id='noticia',
                title='noticia',
            )
            # Necessário para poder visualizar os objetos criados nos testes
            # unitários em self.browser.
            transaction.commit()
            # Curioso que na template preciso fazer
            # obj.EffectiveDate() mas não preciso obj.modified() e obj.effective()
            # (só obj.modified já volta o valor) mas aqui no Python preciso disso.
            item_date = obj.modified() if obj.EffectiveDate() == 'None' else obj.effective()
            # XXX: Deveria usar o toLocalizedTime, que também é usado na template
            # em listing_summary, mas não descobri, como, no código python sem
            # renderizar na template, vir traduzido. Portanto, comparo os formatos
            # renderizados na template com uso de strftime.
            date = item_date.strftime(LOCAL_TIME_FORMAT)
            time = item_date.strftime(TIME_FORMAT)
        self.login_browser()
        self.browser.open('{0}/{1}'.format(self.folder.absolute_url(), 'summary_view'))
        # Como será comparada uma string em html, removeremos todos os espaços
        # para evitar problemas e complicações na comparação.
        contents_no_spaces = ''.join(self.browser.contents.split())
        # Deve conter a data do objeto criado, assim como a hora.
        self.assertIn(
            '<iclass="icon-day"></i>{0}</span><spanclass="summary-view-icon"><iclass="icon-hour"></i>{1}'.format(date, time),
            contents_no_spaces)
        # Não deve conter a data de 1969 padrão.
        self.assertNotIn('<iclass="icon-day"></i>31/12/1969', contents_no_spaces)
