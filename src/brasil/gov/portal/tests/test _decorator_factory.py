# -*- coding: utf-8 -*-

from brasil.gov.portal.testing import INTEGRATION_TESTING
from plone import api

import unittest


class DecoratorFactoryTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        with api.env.adopt_roles(['Manager']):
            self.assuntos = api.content.create(
                type='Folder',
                container=self.portal,
                id='assuntos',
                title=u'Assuntos',
            )
            self.editoria_a = api.content.create(
                type='Folder',
                container=self.assuntos,
                id='editoria-a',
                title=u'Editoria A',
            )
            self.editoria_b = api.content.create(
                type='Folder',
                container=self.assuntos,
                id='editoria-b',
                title=u'Editoria B',
            )
            api.content.create(
                type='Link',
                container=self.editoria_a,
                id='link-google',
                title=u'Google',
                remoteUrl=u'http://www.google.com',
            )
            api.content.create(
                type='Link',
                container=self.editoria_a,
                id='link-email',
                title=u'Email',
                remoteUrl=u'mailto:mailadress@domain.com',
            )
            api.content.create(
                type='Link',
                container=self.editoria_a,
                id='link-relativo-1',
                title=u'Link Relativo 1',
                remoteUrl=u'./link-google',
            )
            api.content.create(
                type='Link',
                container=self.editoria_b,
                id='link-relativo-2',
                title=u'Link Relativo 2',
                remoteUrl=u'../editoria-a',
            )
            api.content.create(
                type='Link',
                container=self.editoria_b,
                id='link-portal-url',
                title=u'Link portal_url',
                remoteUrl=u'${portal_url}/assuntos/editoria-a',
            )
            api.content.create(
                type='Link',
                container=self.editoria_b,
                id='link-navigation-root-url',
                title=u'Link navigation_root_url',
                remoteUrl=u'${navigation_root_url}/assuntos/editoria-a',
            )

    def test_decorator_factory(self):
        portal_url = self.portal['portal_url']()
        view = self.editoria_a.restrictedTraverse('@@navtree_builder_view')
        items = view.navigationTree()
        children = items['children']
        for child in children:
            if child['id'] == 'assuntos':
                for child_a in child['children']:
                    if child_a['id'] == 'editoria-a':
                        for child_edit_a in child_a['children']:
                            if child_edit_a['id'] == 'link-google':
                                self.assertEqual(
                                    child_edit_a['getRemoteUrl'],
                                    u'http://www.google.com',
                                )
                            elif child_edit_a['id'] == 'link-email':
                                self.assertEqual(
                                    child_edit_a['getRemoteUrl'],
                                    u'mailto:mailadress@domain.com',
                                )
                            elif child_edit_a['id'] == 'link-relativo-1':
                                self.assertEqual(
                                    child_edit_a['getRemoteUrl'],
                                    u'{0}/assuntos/editoria-a/link-google'.format(portal_url),
                                )
        view = self.editoria_b.restrictedTraverse('@@navtree_builder_view')
        items = view.navigationTree()
        children = items['children']
        for child in children:
            if child['id'] == 'assuntos':
                for child_a in child['children']:
                    if child_a['id'] == 'editoria-b':
                        for child_edit_b in child_a['children']:
                            if child_edit_b['id'] == 'link-relativo-2':
                                self.assertEqual(
                                    child_edit_b['getRemoteUrl'],
                                    u'{0}/assuntos/editoria-a'.format(portal_url),
                                )
                            elif child_edit_b['id'] == 'link-portal-url':
                                self.assertEqual(
                                    child_edit_b['getRemoteUrl'],
                                    u'{0}/assuntos/editoria-a'.format(portal_url),
                                )
                            elif child_edit_b['id'] == 'link-navigation-root-url':
                                self.assertEqual(
                                    child_edit_b['getRemoteUrl'],
                                    u'{0}/assuntos/editoria-a'.format(portal_url),
                                )
