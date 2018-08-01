# -*- coding: utf-8 -*-
from brasil.gov.portal.config import PROJECTNAME
from brasil.gov.portal.testing import INTEGRATION_TESTING
from plone.browserlayer.utils import registered_layers

import unittest


INSTALLED = {
    'brasil.gov.agenda',
    'brasil.gov.barra',
    # 'brasil.gov.portlets',
    'brasil.gov.tiles',
    'brasil.gov.vcge',
    'collective.cover',
    'collective.nitf',
    'collective.polls',
    # 'collective.upload',
    # 'Doormat',
    # 'plone.app.contenttypes',
    # 'plone.app.theming',
    'plone.restapi',
    # 'PloneFormGen',
    'PloneKeywordManager',
    'RedirectionTool',
    'sc.embedder',
    'sc.social.like',
    'webcouturier.dropdownmenu',
}

INSTALLABLE = {
    'collective.fingerpointing',
    'collective.lazysizes',
    'collective.liveblog',
    'Marshall',
    'plone.app.referenceablebehavior',
    'sc.photogallery',
}


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

    def test_installed(self):
        self.assertTrue(self.qi.isProductInstalled(PROJECTNAME))

    @unittest.expectedFailure
    def test_installed_dependencies(self):
        # XXX: this needs to be refactored as portal_quickinstaller
        #      is no longer the canonical way of getting reliable
        #      information on dependencies
        expected = INSTALLED
        actual = {
            p['id'] for p in self.qi.listInstalledProducts()
            if p['id'] != PROJECTNAME}
        # XXX: for some unknown reason portal_quickinstaller lists
        #      collective.portlet.calendar as installed
        actual = actual - {'collective.portlet.calendar'}
        self.assertEqual(
            expected, actual, 'Not installed: ' + ', '.join(actual - expected))

    @unittest.expectedFailure
    def test_installable_dependencies(self):
        # XXX: this needs to be refactored as portal_quickinstaller
        #      is no longer the canonical way of getting reliable
        #      information on dependencies
        expected = INSTALLABLE
        actual = {p['id'] for p in self.qi.listInstallableProducts()}
        self.assertEqual(
            expected, actual, 'Missing: ' + ', '.join(actual - expected))

    def test_add_infographic_permission(self):
        permission = 'brasil.gov.portal: Add Infographic'
        expected = ['Contributor', 'Manager', 'Owner', 'Site Administrator']
        roles = self.portal.rolesOfPermission(permission)
        roles = [r['name'] for r in roles if r['selected']]
        self.assertListEqual(roles, expected)

    def test_infographic_workflow(self):
        wftool = self.portal['portal_workflow']
        self.assertEqual(wftool.getChainForPortalType('Infographic'), ())

    def test_ultimo_upgrade_igual_metadata_xml_filesystem(self):
        """Testa se o número do último upgradeStep disponível é o mesmo
        do metadata.xml do profile.

        É também útil para garantir que para toda alteração feita no
        version do metadata.xml tenha um upgradeStep associado.
        """
        from Products.GenericSetup.upgrade import listUpgradeSteps
        profile_id = PROJECTNAME + ':default'
        upgrade_info = self.qi.upgradeInfo(PROJECTNAME)
        upgradeSteps = listUpgradeSteps(self.st, profile_id, '')
        upgrades = [upgrade[0]['dest'][0] for upgrade in upgradeSteps]
        last_upgrade = sorted(upgrades, key=int)[-1]
        self.assertEqual(upgrade_info['installedVersion'], last_upgrade)
