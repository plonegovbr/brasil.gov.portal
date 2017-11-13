# -*- coding: utf-8 -*-
from brasil.gov.portal.testing import INTEGRATION_TESTING
from plone import api

import transaction
import unittest


class UpgradeBaseTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING
    profile_id = u'brasil.gov.portal:default'

    def setUp(self):
        self.portal = self.layer['portal']
        self.setup = self.portal['portal_setup']
        self.setup.setLastVersionForProfile(self.profile_id, self.from_)

    def _get_upgrade_step_by_title(self, title):
        """Return the upgrade step that matches the title specified."""
        self.setup.setLastVersionForProfile(self.profile_id, self.from_)
        upgrades = self.setup.listUpgrades(self.profile_id)
        steps = [s for s in upgrades[0] if s['title'] == title]
        return steps[0] if steps else None

    def _do_upgrade(self, step):
        """Execute an upgrade step."""
        request = self.layer['request']
        request.form['profile_id'] = self.profile_id
        request.form['upgrades'] = [step['id']]
        self.setup.manage_doUpgrades(request=request)


class To10803TestCase(UpgradeBaseTestCase):

    from_ = '10802'
    to_ = '10803'

    def test_profile_version(self):
        version = self.setup.getLastVersionForProfile(self.profile_id)[0]
        self.assertEqual(version, self.from_)

    def test_registered_steps(self):
        steps = len(self.setup.listUpgrades(self.profile_id)[0])
        self.assertEqual(steps, 5)

    def test_install_redirection_tool(self):
        title = u'Install Products.RedirectionTool'
        step = self._get_upgrade_step_by_title(title)
        self.assertIsNotNone(step)

        # simulate (partially) state on previous version
        addon = 'RedirectionTool'
        qi = api.portal.get_tool('portal_quickinstaller')
        with api.env.adopt_roles(['Manager']):
            qi.uninstallProducts([addon])
        self.assertFalse(qi.isProductInstalled(addon))

        # execute upgrade step and verify changes were applied
        self._do_upgrade(step)
        self.assertTrue(qi.isProductInstalled(addon))

    def test_install_restapi(self):
        title = u'Install plone.restapi'
        step = self._get_upgrade_step_by_title(title)
        self.assertIsNotNone(step)

        # simulate state on previous version
        addon = 'plone.restapi'
        qi = api.portal.get_tool('portal_quickinstaller')
        with api.env.adopt_roles(['Manager']):
            qi.uninstallProducts([addon])
        self.assertFalse(qi.isProductInstalled(addon))

        # execute upgrade step and verify changes were applied
        self._do_upgrade(step)
        self.assertTrue(qi.isProductInstalled(addon))

    def test_uninstall_widgets(self):
        title = u'Uninstall collective.z3cform.widgets'
        step = self._get_upgrade_step_by_title(title)
        self.assertIsNotNone(step)

        # simulate (partially) state on previous version
        addon = 'collective.z3cform.widgets'
        qi = api.portal.get_tool('portal_quickinstaller')
        with api.env.adopt_roles(['Manager']):
            qi.installProducts([addon])
        self.assertTrue(qi.isProductInstalled(addon))

        # execute upgrade step and verify changes were applied
        self._do_upgrade(step)
        from collective.z3cform.widgets.interfaces import ILayer
        from plone.browserlayer.utils import registered_layers
        self.assertFalse(qi.isProductInstalled(addon))
        self.assertFalse(qi.isProductInstallable(addon))
        self.assertNotIn(ILayer, registered_layers())

    def test_icon_visibility(self):
        title = u'Habilita os ícones dos conteúdos para os usuários auteticados.'
        step = self._get_upgrade_step_by_title(title)
        self.assertIsNotNone(step)
        self.properties = api.portal.get_tool('portal_properties').site_properties

        # simulate state on previous version
        self.properties.icon_visibility = 'disabled'
        transaction.commit()

        # execute upgrade step and verify changes were applied
        self._do_upgrade(step)
        self.assertEqual(self.properties.icon_visibility, 'authenticated')
