# -*- coding: utf-8 -*-

from brasil.gov.portal.config import PROJECTNAME
from brasil.gov.portal.testing import INTEGRATION_TESTING

import unittest

DEPENDENCIES = [
    #'brasil.gov.temas',
    'collective.cover',
    'collective.googleanalytics',
    'collective.nitf',
    'collective.polls',
    'collective.upload',
    'sc.embedder',
    'sc.social.like',
]


class InstallTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']

    def test_installed(self):
        self.assertTrue(self.qi.isProductInstalled(PROJECTNAME),
                        '%s not installed' % PROJECTNAME)

    def test_dependencies_installed(self):
        expected = set(DEPENDENCIES)
        installed = set(name for name, product in self.qi.items()
                        if product.isInstalled())
        result = sorted(expected - installed)

        self.assertFalse(result,
            "These dependencies are not installed: " + ", ".join(result))
