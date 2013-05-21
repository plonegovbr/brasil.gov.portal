# -*- coding: utf-8 -*-

from brasil.gov.portal.testing import INTEGRATION_TESTING
from collective.cover.controlpanel import ICoverSettings
from collective.nitf.controlpanel import INITFSettings
from collective.upload.interfaces import IUploadSettings
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

import unittest


class AddonsSettingsTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.registry = getUtility(IRegistry)
        self.nitf_settings = self.registry.forInterface(INITFSettings)
        self.wt = self.portal['portal_workflow']
        self.pm = self.portal['portal_membership']

    def test_collective_cover_settings(self):
        """ Searchable content types on cover.
        """
        settings = self.registry.forInterface(ICoverSettings)
        allowed_types = [
            u'collective.nitf.content',
            u'collective.polls.poll',
            u'Collection',
            u'FormFolder',
            u'Image',
            u'Document',
            u'Link'
        ]
        self.assertListEqual(settings.searchable_content_types, allowed_types)

    def test_collective_nitf_available_genres(self):
        """ Genres used portal wide.
        """
        available_genres = list(self.nitf_settings.available_genres)
        available_genres.sort()
        expected_genres = [
            u'Analysis',
            u'Archive material',
            u'Current',
            u'Exclusive',
            u'From the Scene',
            u'Interview',
            u'Obituary',
            u'Opinion',
            u'Polls and Surveys',
            u'Press Release',
            u'Profile',
            u'Retrospective',
            u'Review',
            u'Special Report',
            u'Summary',
            u'Wrap',
        ]
        self.assertListEqual(available_genres, expected_genres)

    def test_collective_nitf_available_sections(self):
        """ News sections defined.
        """
        available_sections = list(self.nitf_settings.available_sections)
        available_sections.sort()
        expected = [
            u'General',
        ]
        self.assertListEqual(available_sections, expected)

    def test_collective_nitf_default_section(self):
        self.assertEqual(self.nitf_settings.default_section, u'General')

    def test_collective_upload_settings(self):
        """ Images uploaded must be smaller than 1024x1024.
        """
        settings = self.registry.forInterface(IUploadSettings)
        self.assertEqual(settings.resize_max_width, 1024)
        self.assertEqual(settings.resize_max_height, 1024)
        self.assertEqual(settings.upload_extensions,
                         u'gif, jpeg, jpg, png, pdf, doc, txt, docx')

    def test_sc_social_likes_settings(self):
        likes = self.portal['portal_properties'].sc_social_likes_properties
        enabled_portal_types = list(likes.enabled_portal_types)
        enabled_portal_types.sort()
        types_expected = [
            'Audio',
            'Collection',
            'Document',
            'Event',
            'FormFolder',
            'Image',
            'collective.cover.content',
            'collective.nitf.content',
            'collective.polls.poll',
        ]
        self.assertListEqual(enabled_portal_types, types_expected)
