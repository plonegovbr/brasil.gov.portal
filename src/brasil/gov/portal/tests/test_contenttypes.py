# -*- coding: utf-8 -*-

from brasil.gov.portal.testing import INTEGRATION_TESTING
from collective.cover.controlpanel import ICoverSettings
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

import unittest


class ContentTypesTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.pt = self.portal['portal_types']

    def test_news_item_not_allowed(self):
        """ News Item should be not Globally Allowed
        """
        self.assertTrue('News Item' in self.pt.objectIds())
        type_info = self.pt['News Item']
        self.assertFalse(type_info.global_allow)

    def test_plone_app_contenttypes_installed(self):
        """ News Item should be not Globally Allowed
        """
        types = ['Collection',
                 'Document',
                 'Event',
                 'File',
                 'Folder',
                 'Image',
                 'Link',
                 'News Item']
        for t in types:
            self.assertTrue(t in self.pt.objectIds())
            type_info = self.pt['News Item']
            self.assertTrue('plone.app.contenttype' in type_info.klass)

    def test_cover_installed(self):
        self.assertTrue('collective.cover.content' in self.pt.objectIds())

    def test_cover_searchable_types(self):
        self.registry = getUtility(IRegistry)
        configs = self.registry.forInterface(ICoverSettings)
        searchable_content_types = configs.searchable_content_types
        types = [u'collective.nitf.content',
                 u'collective.polls.poll',
                 u'Collection',
                 u'FormFolder',
                 u'Image',
                 u'Document',
                 u'Link']
        for t in types:
            self.assertTrue(t in searchable_content_types)

    def test_poll_installed(self):
        self.assertTrue('collective.polls.poll' in self.pt.objectIds())
