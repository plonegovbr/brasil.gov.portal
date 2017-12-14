# -*- coding: utf-8 -*-
from brasil.gov.portal.testing import INTEGRATION_TESTING
from plone import api
from plone.app.viewletmanager.interfaces import IViewletSettingsStorage
from zope.component import queryUtility

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


class To10804TestCase(UpgradeBaseTestCase):

    from_ = '10803'
    to_ = '10804'

    def test_profile_version(self):
        version = self.setup.getLastVersionForProfile(self.profile_id)[0]
        self.assertEqual(version, self.from_)

    def test_registered_steps(self):
        steps = len(self.setup.listUpgrades(self.profile_id)[0])
        self.assertEqual(steps, 3)

    def test_remove_styles(self):
        # address also an issue with Setup permission
        title = u'Move styles to brasil.gov.temas package'
        step = self._get_upgrade_step_by_title(title)
        self.assertIsNotNone(step)

        # simulate state on previous version
        from brasil.gov.portal.upgrades.v10804 import STYLES
        css_tool = api.portal.get_tool('portal_css')
        for css in STYLES:
            css_tool.registerResource(id=css)
            self.assertIn(css, css_tool.getResourceIds())

        # run the upgrade step to validate the update
        self._do_upgrade(step)
        for css in STYLES:
            self.assertNotIn(css, css_tool.getResourceIds())

    def test_show_global_sections(self):
        # address also an issue with Setup permission
        title = u'Show back global_sections viewlet'
        step = self._get_upgrade_step_by_title(title)
        self.assertIsNotNone(step)

        # simulate state on previous version
        storage = queryUtility(IViewletSettingsStorage)
        manager = u'plone.portalheader'
        skinname = u'Plone Default'
        hidden = (u'plone.global_sections',)
        storage.setHidden(manager, skinname, hidden)

        # run the upgrade step to validate the update
        self._do_upgrade(step)
        hidden = storage.getHidden(manager, skinname)
        self.assertEqual(hidden, ())

    def test_remove_nitf_customizations(self):
        # check if the upgrade step is registered
        title = u'Remove collective.nitf customizations'
        step = self._get_upgrade_step_by_title(title)
        self.assertIsNotNone(step)

        custom_view = 'nitf_custom_view'
        types_tool = api.portal.get_tool('portal_types')
        nitf = types_tool['collective.nitf.content']

        # simulate state on previous version
        nitf.view_methods += tuple(custom_view)
        nitf.default_view_fallback = False

        with api.env.adopt_roles(['Manager']):
            self.n1 = api.content.create(
                self.portal, 'collective.nitf.content', 'n1')
            self.n2 = api.content.create(
                self.portal, 'collective.nitf.content', 'n2')
        self.n1.setLayout(custom_view)
        self.n2.setLayout(custom_view)
        self.assertEqual(self.n1.getLayout(), custom_view)
        self.assertEqual(self.n2.getLayout(), custom_view)

        # run the upgrade step to validate the update
        self._do_upgrade(step)

        self.assertNotIn(custom_view, nitf.view_methods)
        self.assertTrue(nitf.default_view_fallback)
        self.assertEqual(self.n1.getLayout(), 'view')
        self.assertEqual(self.n2.getLayout(), 'view')
