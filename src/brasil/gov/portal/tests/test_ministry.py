# -*- coding: utf-8 -*-
from brasil.gov.portal.content.ministry import IMinistry
from brasil.gov.portal.testing import INTEGRATION_TESTING
from plone import api
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest


class IMinistryTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        with api.env.adopt_roles(['Manager']):
            self.ministry = api.content.create(
                self.portal, 'Ministry', 'ministry')

    def test_adding(self):
        self.assertTrue(IMinistry.providedBy(self.ministry))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='Ministry')
        self.assertIsNotNone(fti)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='Ministry')
        schema = fti.lookupSchema()
        self.assertEqual(schema.getName(), 'plone_0_Ministry')

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='Ministry')
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(IMinistry.providedBy(new_object))

    def test_exclude_from_navigation_behavior(self):
        from plone.app.dexterity.behaviors.exclfromnav import IExcludeFromNavigation
        self.assertTrue(IExcludeFromNavigation.providedBy(self.ministry))
