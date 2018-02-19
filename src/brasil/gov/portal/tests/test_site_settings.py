# -*- coding: utf-8 -*-
from brasil.gov.portal.config import LOCAL_TIME_FORMAT
from brasil.gov.portal.testing import INTEGRATION_TESTING

import unittest


class SiteSettingsTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_localTimeFormat(self):
        site_properties = self.portal['portal_properties'].site_properties
        self.assertEqual(site_properties.localTimeFormat, LOCAL_TIME_FORMAT,
                         'Time format not set')

    def test_allowed_combined_language_code(self):
        self.lang = getattr(self.portal, 'portal_languages')
        self.assertTrue(self.lang.use_combined_language_codes == 1,
                        'Combined language code not supported')

    def test_language_settings(self):
        languages = self.portal['portal_languages']
        self.assertEqual(languages.use_combined_language_codes, 1,
                         'Combined language code not supported')

        self.assertEqual(languages.getDefaultLanguage(), 'pt-br',
                         'Language not set')

    def test_action_site_actions_plone_setup_disabled(self):
        pc = self.portal['portal_actions']
        site_actions = pc['site_actions']
        self.assertFalse(site_actions.plone_setup.visible)
