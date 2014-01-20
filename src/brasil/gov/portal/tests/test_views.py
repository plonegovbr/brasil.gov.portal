# -*- coding: utf-8 -*-

from brasil.gov.portal.interfaces import IBrasilGov
from brasil.gov.portal.testing import INTEGRATION_TESTING
from plone import api
from plonetheme.sunburst.browser.interfaces import IThemeSpecific
from zope.interface import alsoProvides
from zope.interface import directlyProvides
from ZPublisher.tests.testHTTPRequest import TEST_FILE_DATA
from ZPublisher.tests.testHTTPRequest import TEST_ENVIRON

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


class SearchTestCase(BaseViewTestCase):

    def setUp(self):
        super(SearchTestCase, self).setUp()
        self.view = api.content.get_view(u'busca', self.portal, self.request)

    def test_type_name(self):
        self.assertEqual(self.view.type_name('Folder'), 'Pasta/Álbum')
