# -*- coding: utf-8 -*-
from brasil.gov.portal.testing import INTEGRATION_TESTING
from plone import api

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
        self.assertEqual(steps, 4)

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
        title = u'Atualiza portal para versão 10803.'
        step = self._get_upgrade_step_by_title(title)
        self.assertIsNotNone(step)

        # simulate state on previous version
        properties = api.portal.get_tool('portal_properties').site_properties
        properties.icon_visibility = 'disabled'

        # execute upgrade step and verify changes were applied
        self._do_upgrade(step)
        self.assertEqual(properties.icon_visibility, 'authenticated')

    def test_tinymce_ancora_links_internos(self):
        title = u'Atualiza portal para versão 10803.'
        step = self._get_upgrade_step_by_title(title)
        self.assertIsNotNone(step)

        # Simula situação antiga:
        # https://github.com/plonegovbr/brasil.gov.portal/blob/502b98087450cc95ddeb277e09faffc59adbba0d/src/brasil/gov/portal/profiles/default/tinymce.xml#L23
        before_10803_anchor_selector = u''
        before_10803_containsanchors = [
            u'collective.nitf.content',
            u'Document',
            u'Event',
        ]

        portal_tinymce = api.portal.get_tool(name='portal_tinymce')
        portal_tinymce.containsanchors = u'\n'.join(before_10803_containsanchors)
        portal_tinymce.anchor_selector = before_10803_anchor_selector
        # Fim simulação antiga

        # execute upgrade step and verify changes were applied
        self._do_upgrade(step)

        is_10803_containsanchors = [
            u'ATRelativePathCriterion',
            u'Document',
            u'Document|text',
            u'Event',
            u'Event|text',
            u'collective.nitf.content',
            u'collective.nitf.content|text',
        ]
        is_10803_anchor_selector = [
            u'h2',
            u'h3',
            u'a[name]',
        ]

        self.assertEqual(
            portal_tinymce.containsanchors.split(),
            is_10803_containsanchors,
        )

        self.assertEqual(
            portal_tinymce.anchor_selector.split(','),
            is_10803_anchor_selector,
        )


class To10804TestCase(UpgradeBaseTestCase):

    from_ = '10803'
    to_ = '10804'

    def test_profile_version(self):
        version = self.setup.getLastVersionForProfile(self.profile_id)[0]
        self.assertEqual(version, self.from_)

    def test_registered_steps(self):
        steps = len(self.setup.listUpgrades(self.profile_id)[0])
        self.assertEqual(steps, 4)

    def test_css_upload_before_css_portlet_calendar(self):
        title = u'Altera ordem de arquivos css'
        step = self._get_upgrade_step_by_title(title)
        self.assertIsNotNone(step)

        portal_css = api.portal.get_tool('portal_css')
        upload_css_id = '++resource++collective.upload/upload.css'
        portlet_calendar_css_id = '++resource++calendar_styles/calendar.css'

        # Simula situação incorreta: css do upload depois do calendar.
        portal_css.moveResourceToTop(portlet_calendar_css_id)
        portal_css.moveResourceToBottom(upload_css_id)
        upload_pos = portal_css.getResourcePosition(upload_css_id)
        calendar_pos = portal_css.getResourcePosition(portlet_calendar_css_id)
        self.assertGreater(upload_pos, calendar_pos)

        # execute upgrade step and verify changes were applied
        self._do_upgrade(step)
        upload_pos = portal_css.getResourcePosition(upload_css_id)
        calendar_pos = portal_css.getResourcePosition(portlet_calendar_css_id)
        self.assertLess(upload_pos, calendar_pos)
