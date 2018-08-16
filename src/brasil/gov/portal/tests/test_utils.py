# -*- coding: utf-8 -*-
from brasil.gov.portal.utils import validate_background_image
from brasil.gov.portal.utils import validate_list_of_links
from zope.interface import Invalid

import unittest


class UtilsTestCase(unittest.TestCase):

    def test_validate_list_of_links_valid(self):
        self.assertTrue(validate_list_of_links([]))
        self.assertTrue(validate_list_of_links(['Title|http://example.org']))

    def test_validate_list_of_links_invalid(self):
        with self.assertRaises(Invalid):
            validate_list_of_links(['Title http://example.org'])
            validate_list_of_links(['Title||http://example.org'])
            validate_list_of_links(['Title|example.org'])
            validate_list_of_links(['Title'])
            validate_list_of_links(['http://example.org'])

    def test_validate_background_image_valid(self):
        self.assertTrue(validate_background_image(None))

    def test_validate_background_image_invalid(self):
        from brasil.gov.portal.tests.test_helper_view import IMAGEB64
        with self.assertRaises(Invalid):
            validate_background_image(IMAGEB64)
