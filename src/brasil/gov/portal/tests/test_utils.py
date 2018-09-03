# -*- coding: utf-8 -*-
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
