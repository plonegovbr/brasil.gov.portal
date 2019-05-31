# -*- coding: utf-8 -*-
from brasil.gov.portal.content.infographic import IInfographic
from brasil.gov.portal.testing import INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.dexterity.interfaces import IDexterityFTI
from plone.testing.z2 import Browser
from zope.component import createObject
from zope.component import queryUtility

import transaction
import unittest


class InfographicTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.browser = Browser(self.layer['app'])

    def _create_infographic(self):
        with api.env.adopt_roles(['Manager']):
            self.infographic = api.content.create(
                self.portal, 'Infographic', 'infographic',
            )

    def _login_browser(self):
        """Autentica usuário de teste no browser"""
        setRoles(self.portal, TEST_USER_ID, ['Site Administrator'])
        self.browser.handleErrors = False
        basic_auth = 'Basic {0}'.format(
            '{0}:{1}'.format(TEST_USER_NAME, TEST_USER_PASSWORD),
        )
        self.browser.addHeader('Authorization', basic_auth)
        transaction.commit()

    def test_adding(self):
        self._create_infographic()
        self.assertTrue(IInfographic.providedBy(self.infographic))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='Infographic')
        self.assertIsNotNone(fti)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='Infographic')
        schema = fti.lookupSchema()
        self.assertEqual(schema.getName(), 'plone_0_Infographic')

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='Infographic')
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(IInfographic.providedBy(new_object))

    def test_exclude_from_navigation_behavior(self):
        from plone.app.dexterity.behaviors.exclfromnav import IExcludeFromNavigation

        self._create_infographic()
        self.assertTrue(IExcludeFromNavigation.providedBy(self.infographic))

    def test_edit_link_folder_contents(self):
        """https://github.com/plonegovbr/brasil.gov.portal/issues/578"""
        with api.env.adopt_roles(['Manager']):
            api.content.create(self.portal, 'Infographic', 'infographic-XX')
            # Necessário para poder visualizar os objetos criados nos testes
            # unitários em self.browser.
            transaction.commit()

        self._login_browser()
        self.browser.open(
            '{0}/folder_contents'.format(self.portal.absolute_url()))
        self.assertIn('infographic-XX/view', self.browser.contents)
