# -*- coding: utf-8 -*-
from brasil.gov.portal.browser.content.external import ExternalContentView
from brasil.gov.portal.content.external import IExternalContent
from brasil.gov.portal.testing import INTEGRATION_TESTING
from plone import api
from plone.dexterity.interfaces import IDexterityFTI
from plone.dexterity.schema import SCHEMA_CACHE
from plone.namedfile.file import NamedBlobImage
from zope.component import createObject
from zope.component import queryUtility

import os
import unittest


class ExternalContentTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        with api.env.adopt_roles(['Manager']):
            self.folder = api.content.create(
                type='Folder',
                container=self.portal,
                id='test-folder',
            )
            # Invalidate schema cache
            SCHEMA_CACHE.invalidate('ExternalContent')
            self.content = api.content.create(
                type='ExternalContent',
                container=self.folder,
                id='external',
            )
            self.setup_content_data()

    def setup_content_data(self):
        path = os.path.dirname(__file__)
        image = open(os.path.join(path, 'files', 'image.jpg')).read()
        self.image = NamedBlobImage(image, 'image/jpeg', u'image.jpg')

    def test_adding(self):
        self.assertTrue(IExternalContent.providedBy(self.content))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='ExternalContent')
        self.assertNotEqual(None, fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='ExternalContent')
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(IExternalContent.providedBy(new_object))

    def test_image_tag(self):
        content = self.content
        # Sem imagem, sem tag
        self.assertEqual(content.tag(), '')
        # Adicionamos a imagem
        content.image = self.image
        self.assertIn('tileImage', content.tag())

    def test_image_thumb(self):
        content = self.content
        # Sem imagem, sem thumbnail
        self.assertEqual(content.image_thumb(), None)
        # Adicionamos a imagem
        content.image = self.image
        self.assertTrue(content.image_thumb())


class ExternalContentViewTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        with api.env.adopt_roles(['Manager']):
            self.content = api.content.create(
                container=self.portal,
                type='ExternalContent',
                id='external',
                remoteUrl='http://www.example.org/',
            )
            api.content.transition(self.content, 'publish')

    def test_view(self):
        view = self.content.restrictedTraverse('@@view')
        self.assertTrue(isinstance(view, ExternalContentView))

    def test_view_manager(self):
        with api.env.adopt_roles(['Manager']):
            view = self.content.restrictedTraverse('@@view')
            self.assertIn('The link address is', view())

        headers = self.content.REQUEST.response.headers
        self.assertNotIn('location', headers)

    def test_view_anonymous(self):
        with api.env.adopt_roles(['Anonymous']):
            view = self.content.restrictedTraverse('@@view')
            self.assertIsNone(view())

        headers = self.content.REQUEST.response.headers
        self.assertIn('location', headers)
        self.assertEqual(headers['location'], 'http://www.example.org/')
