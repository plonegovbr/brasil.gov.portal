# -*- coding: utf-8 -*-
from brasil.gov.portal.testing import INTEGRATION_TESTING
from plone import api

import unittest


class ContentCentralViewTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        with api.env.adopt_roles(['Manager']):
            self.folder = api.content.create(self.portal, 'Folder', 'folder')
        self.view = self.folder.restrictedTraverse('centrais-de-conteudo')

    def test_action(self):
        action = 'centrais-de-conteudo'
        self.folder.setLayout(action)
        self.assertEqual(self.folder.getLayout(), action)

    def test_portlets_disabled(self):
        self.view.setup()
        self.assertIn('disable_plone.leftcolumn', self.request)
        self.assertIn('disable_plone.rightcolumn', self.request)

    def test_greenbar_authenticated(self):
        self.view.setup()
        self.assertNotIn('disable_border', self.request)

    def test_greenbar_anonymous(self):
        # XXX: api.env.adopt_roles(['Anonymous']) is not working here
        #      we are stuck at plone.api = 1.6
        from plone.app.testing import logout
        logout()
        view = self.folder.unrestrictedTraverse('centrais-de-conteudo')
        view.setup()
        self.assertIn('disable_border', self.request)

    def test_filter_types(self):
        self.assertEqual(
            self.view.filter_types([]),
            ['sc.embedder', 'Image', 'Audio', 'Infographic'])
        self.assertEqual(self.view.filter_types(['Image']), ['Image'])
        self.assertEqual(self.view.filter_types(['File']), [])

    def test_media(self):
        from collections import OrderedDict
        # Esse teste tem resultados diferentes se for executado manualmente ou
        # em conjunto com os demais testes com o uso de bin/test --all.
        # Isso ocorre porque os testes em test_audio_content_type.py usam
        # transaction.commit(), portanto, eles já existem quando esse teste é
        # executado quando se usa o bin/test --all.
        # ('test-folder-MPEG', 'test-folder-OGG')
        if 'test-folder-MPEG' in self.portal.objectIds():
            self.assertEqual(self.view.media(), OrderedDict([('Audio', u'Audio')]))
        else:
            self.assertEqual(self.view.media(), OrderedDict())

        api.content.create(self.folder, 'Image', 'foo')
        api.content.create(self.folder, 'File', 'bar')

        if 'test-folder-MPEG' in self.portal.objectIds():
            self.assertEqual(
                self.view.media(),
                OrderedDict([('Image', u'Image'), ('Audio', u'Audio')]))
        else:
            self.assertEqual(
                self.view.media(), OrderedDict([('Image', u'Image')]))

    # TODO: add more tests
