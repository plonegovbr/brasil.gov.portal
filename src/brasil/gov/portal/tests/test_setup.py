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

    def test_hidden_dependencies(self):
        packages = [p['id'] for p in self.qi.listInstallableProducts()]
        deps = set(DEPS)
        result = [p for p in deps if p in packages]
        self.assertFalse(result,
                         ("Estas dependencias nao estao ocultas: %s" %
                          ", ".join(result)))

    def test_installed(self):
        self.assertTrue(self.qi.isProductInstalled(PROJECTNAME),
                        '%s nao esta instalado' % PROJECTNAME)

    def test_installed_dependencies(self):
        expected = set(DEPENDENCIES)
        result = []
        for item in expected:
            profile_id = self.qi.getInstallProfile(item)['id']
            if self.st.getLastVersionForProfile(profile_id) == 'unknown':
                result.append(item)
        self.assertFalse(result,
                         ("Estas dependencias nao estao instaladas: %s" %
                          ", ".join(result)))
