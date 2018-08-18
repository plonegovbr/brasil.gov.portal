# -*- coding: utf-8 -*-
from brasil.gov.portal.testing import INTEGRATION_TESTING
from plone import api

import unittest


class ResultsFilterViewTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        with api.env.adopt_roles(['Manager']):
            self.collection = api.content.create(
                self.portal, 'Collection', 'collection')
        self.view = self.collection.restrictedTraverse('filtro-de-resultados')

    def test_action(self):
        action = 'filtro-de-resultados'
        self.collection.setLayout(action)
        self.assertEqual(self.collection.getLayout(), action)

    def test_portlets_disabled(self):
        self.view.setup()
        self.assertIn('disable_plone.leftcolumn', self.request)
        self.assertIn('disable_plone.rightcolumn', self.request)

    def test_greenbar_authenticated(self):
        self.view.setup()
        self.assertNotIn('disable_border', self.request)

    def test_greenbar_anonymous(self):
        # XXX: api.env.adopt_roles(['Anonymous']) is not working here
        #      we are stuck at plone.api = 1.6
        from plone.app.testing import logout
        logout()
        view = self.collection.unrestrictedTraverse('filtro-de-resultados')
        view.setup()
        self.assertIn('disable_border', self.request)

    # TODO: add more tests
