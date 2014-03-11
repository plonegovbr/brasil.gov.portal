# -*- coding: utf-8 -*-

from brasil.gov.portal.config import DEPS
from brasil.gov.portal.config import PROJECTNAME
from brasil.gov.portal.testing import INTEGRATION_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.browserlayer.utils import registered_layers
from Products.GenericSetup.upgrade import listUpgradeSteps

import unittest

PROFILE_ID = 'brasil.gov.portal:default'

DEPENDENCIES = [
    'brasil.gov.agenda',
    'brasil.gov.barra',
    'brasil.gov.tiles',
    'brasil.gov.vcge',
    'collective.cover',
    'collective.js.jqueryui',
    'collective.nitf',
    'collective.polls',
    'collective.upload',
    'plone.app.contenttypes',
    'plone.app.theming',
    'Products.Doormat',
    'Products.PloneFormGen',
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


class TestUpgrade(unittest.TestCase):
    """Ensure product upgrades works."""

    layer = INTEGRATION_TESTING

    profile = 'brasil.gov.portal:default'

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']
        self.st = self.portal['portal_setup']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_to1000_available(self):

        upgradeSteps = listUpgradeSteps(self.st,
                                        self.profile,
                                        '0.0')
        step = [step for step in upgradeSteps
                if (step[0]['dest'] == ('1000',))
                and (step[0]['source'] == ('0.0',))]
        self.assertEqual(len(step), 1)

    def test_to2000_available(self):

        upgradeSteps = listUpgradeSteps(self.st,
                                        self.profile,
                                        '1000')
        step = [step for step in upgradeSteps
                if (step[0]['dest'] == ('2000',))
                and (step[0]['source'] == ('1000',))]
        self.assertEqual(len(step), 1)

    def test_to3000_available(self):

        upgradeSteps = listUpgradeSteps(self.st,
                                        self.profile,
                                        '2000')
        step = [step for step in upgradeSteps
                if (step[0]['dest'] == ('3000',))
                and (step[0]['source'] == ('2000',))]
        self.assertEqual(len(step), 1)

    def test_to4000_available(self):

        upgradeSteps = listUpgradeSteps(self.st,
                                        self.profile,
                                        '3000')
        step = [step for step in upgradeSteps
                if (step[0]['dest'] == ('4000',))
                and (step[0]['source'] == ('3000',))]
        self.assertEqual(len(step), 1)

    def test_to5000_available(self):

        upgradeSteps = listUpgradeSteps(self.st,
                                        self.profile,
                                        '4000')
        step = [step for step in upgradeSteps
                if (step[0]['dest'] == ('5000',))
                and (step[0]['source'] == ('4000',))]
        self.assertEqual(len(step), 1)

    def test_5000_corrige_pastas(self):
        # Ajustamos as pastas para nao estarem ordenadas
        pastas = ['assuntos', 'imagens', 'sobre']
        for pasta_id in pastas:
            pasta_id = self.portal.invokeFactory('Folder', pasta_id)
            pasta = self.portal[pasta_id]
            pasta.setOrdering('unordered')
        # Setamos o profile para versao 4000
        self.st.setLastVersionForProfile(self.profile, u'4000')
        # Pegamos os upgrade steps
        upgradeSteps = listUpgradeSteps(self.st,
                                        self.profile,
                                        '4000')
        steps = [step for step in upgradeSteps
                 if (step[0]['dest'] == ('5000',))
                 and (step[0]['source'] == ('4000',))][0]
        # Os executamos
        for step in steps:
            step['step'].doStep(self.st)
        for pasta_id in pastas:
            pasta = self.portal[pasta_id]
            ordering = pasta.getOrdering()
            self.assertTrue(hasattr(ordering, 'ORDER_KEY'))
