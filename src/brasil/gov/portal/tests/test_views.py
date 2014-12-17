# -*- coding: utf-8 -*-
from DateTime import DateTime
from ZPublisher.tests.testHTTPRequest import TEST_ENVIRON
from ZPublisher.tests.testHTTPRequest import TEST_FILE_DATA
from brasil.gov.portal.browser.album.albuns import Pagination
from brasil.gov.portal.interfaces import IBrasilGov
from brasil.gov.portal.testing import INTEGRATION_TESTING
from plone import api
from plonetheme.sunburst.browser.interfaces import IThemeSpecific
from zope.interface import alsoProvides
from zope.interface import directlyProvides

import unittest


class BaseViewTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        directlyProvides(self.request, IBrasilGov)
        with api.env.adopt_roles(['Manager']):
            self.folder = api.content.create(self.portal, 'Folder', 'folder')


class MediaUploaderViewTestCase(BaseViewTestCase):

    # from ZPublisher.tests.testHTTPRequest import HTTPRequestTests
    def _getTargetClass(self):
        from ZPublisher.HTTPRequest import HTTPRequest
        return HTTPRequest

    # from ZPublisher.tests.testHTTPRequest import HTTPRequestTests
    def _get_response(self, response):
        from ZPublisher import NotFound
        if response is None:
            class _FauxResponse(object):
                _auth = None
                debug_mode = False
                errmsg = 'OK'

                def notFoundError(self, message):
                    raise(NotFound, message)

                def exception(self, *args, **kw):
                    pass
            response = _FauxResponse()
        return response

    # from ZPublisher.tests.testHTTPRequest import HTTPRequestTests
    def _makeOne(self, stdin=None, environ=None, response=None, clean=1):
        from StringIO import StringIO
        if stdin is None:
            stdin = StringIO()
        if environ is None:
            environ = {}
        if 'REQUEST_METHOD' not in environ:
            environ['REQUEST_METHOD'] = 'GET'
        if 'SERVER_NAME' not in environ:
            environ['SERVER_NAME'] = 'http://localhost'
        if 'SERVER_PORT' not in environ:
            environ['SERVER_PORT'] = '8080'
        response = self._get_response(response)
        return self._getTargetClass()(stdin, environ, response, clean)

    def setUp(self):
        super(MediaUploaderViewTestCase, self).setUp()
        alsoProvides(self.request, IThemeSpecific)
        self.view = api.content.get_view(u'media_uploader', self.portal, self.request)

        from StringIO import StringIO
        s = StringIO(TEST_FILE_DATA)
        req = self._makeOne(stdin=s, environ=TEST_ENVIRON.copy())
        req.processInputs()
        self.f = req.form.get('file')

    def test_upload(self):
        with api.env.adopt_roles(['Manager']):
            uploaded = self.view.upload([self.f],
                                        [u'test_title'],
                                        [u'test_description'],
                                        [u'test_rights'])[0]
        self.assertEqual(uploaded.Title(), u'test_title')
        self.assertEqual(uploaded.Description(), u'test_description')
        self.assertEqual(uploaded.Rights(), u'test_rights')


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
            'alt': 'test_description'
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
        self.view.update()

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
        'link': False
    },
    {
        'class': 'pagina',
        'content': '2',
        'href': '?pagina=2',
        'is_next': False,
        'is_prev': False,
        'link': True
    },
    {
        'class': 'pagina',
        'content': '3',
        'href': '?pagina=3',
        'is_next': False,
        'is_prev': False,
        'link': True
    },
    {
        'class': 'pagina',
        'content': '4',
        'href': '?pagina=4',
        'is_next': False,
        'is_prev': False,
        'link': True
    },
    {
        'class': 'pagina',
        'content': '5',
        'href': '?pagina=5',
        'is_next': False,
        'is_prev': False,
        'link': True
    },
    {
        'class': 'pagina',
        'content': '6',
        'href': '?pagina=6',
        'is_next': False,
        'is_prev': False,
        'link': True
    },
    {
        'class': 'pagina',
        'content': '7',
        'href': '?pagina=7',
        'is_next': False,
        'is_prev': False,
        'link': True
    },
    {
        'class': 'reticencias',
        'content': '...',
        'href': '',
        'is_next': False,
        'is_prev': False,
        'link': False
    },
    {
        'class': 'pagina',
        'content': '12',
        'href': '?pagina=12',
        'is_next': False,
        'is_prev': False,
        'link': True
    },
    {
        'class': 'proximo',
        'content': u'label_next',
        'href': '?pagina=2',
        'is_next': True,
        'is_prev': False,
        'link': True
    }
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
        'link': True
    },
    {
        'class': 'reticencias',
        'content': '...',
        'href': '',
        'is_next': False,
        'is_prev': False,
        'link': False
    },
    {
        'class': 'pagina',
        'content': '12',
        'href': '?pagina=12',
        'is_next': False,
        'is_prev': False,
        'link': True
    },
    {
        'class': 'proximo',
        'content': u'label_next',
        'href': '?pagina=6',
        'is_next': True,
        'is_prev': False,
        'link': True
    }
]

PAGINATION_END = [
    {
        'class': 'anterior',
        'content': u'label_previous',
        'href': '?pagina=11',
        'is_next': False,
        'is_prev': True,
        'link': True
    },
    {
        'class': 'pagina',
        'content': '1',
        'href': '?pagina=1',
        'is_next': False,
        'is_prev': False,
        'link': True
    },
    {
        'class': 'reticencias',
        'content': '...',
        'href': '',
        'is_next': False,
        'is_prev': False,
        'link': False
    },
    {
        'class': 'pagina',
        'content': '6',
        'href': '?pagina=6',
        'is_next': False,
        'is_prev': False,
        'link': True
    },
    {
        'class': 'pagina',
        'content': '7',
        'href': '?pagina=7',
        'is_next': False,
        'is_prev': False,
        'link': True
    },
    {
        'class': 'pagina',
        'content': '8',
        'href': '?pagina=8',
        'is_next': False,
        'is_prev': False,
        'link': True
    },
    {
        'class': 'pagina',
        'content': '9',
        'href': '?pagina=9',
        'is_next': False,
        'is_prev': False,
        'link': True
    },
    {
        'class': 'pagina',
        'content': '10',
        'href': '?pagina=10',
        'is_next': False,
        'is_prev': False,
        'link': True
    },
    {
        'class': 'pagina',
        'content': '11',
        'href': '?pagina=11',
        'is_next': False,
        'is_prev': False,
        'link': True
    },
    {
        'class': 'atual',
        'content': '12',
        'href': '?pagina=12',
        'is_next': False,
        'is_prev': False,
        'link': False
    },
]
