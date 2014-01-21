# -*- coding: utf-8 -*-

from brasil.gov.portal.config import DEPS
from brasil.gov.portal.config import PROJECTNAME
from brasil.gov.portal.testing import INTEGRATION_TESTING
from plone.browserlayer.utils import registered_layers

import unittest

PROFILE_ID = 'brasil.gov.portal:default'

DEPENDENCIES = [
    'brasil.gov.temas',
    'collective.cover',
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
        self.st = self.portal['portal_setup']

    def test_browser_layer(self):
        layers = [l.getName() for l in registered_layers()]
        self.assertTrue('IBrasilGov' in layers,
                        'add-on layer was not installed')

    def test_gs_version(self):
        setup = self.st
        self.assertEqual(setup.getLastVersionForProfile(PROFILE_ID),
                         (u'5000',),
                         '%s version mismatch' % PROJECTNAME)

    @unittest.expectedFailure
    def test_hidden_dependencies(self):
        packages = set([p['id'] for p in self.qi.listInstallableProducts()] +
                       [p[0] for p in self.qi.items()])
        deps = set(DEPS)
        result = [p for p in deps if p in packages]
        self.assertFalse(result,
                         ("These dependencies are not hidden: %s" %
                          ", ".join(result)))

    @unittest.expectedFailure
    def test_installed(self):
        self.assertTrue(self.qi.isProductInstalled(PROJECTNAME),
                        '%s not installed' % PROJECTNAME)

    @unittest.expectedFailure
    def test_dependencies_installed(self):
        expected = set(DEPENDENCIES)
        installed = set(name for name, product in self.qi.items()
                        if product.isInstalled())
        result = sorted(expected - installed)

        self.assertFalse(result,
                         ("These dependencies are not installed: %s" %
                          ", ".join(result)))
