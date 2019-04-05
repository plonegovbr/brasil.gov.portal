# -*- coding: utf-8 -*-

from brasil.gov.portal.testing import INTEGRATION_TESTING
from collective.cover.controlpanel import ICoverSettings
from plone import api
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

import unittest


class ContentTypesTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.pt = self.portal['portal_types']

    def test_news_item_not_allowed(self):
        """ News Item should be not Globally Allowed
        """
        self.assertTrue('News Item' in self.pt.objectIds())
        type_info = self.pt['News Item']
        self.assertFalse(type_info.global_allow)

    def test_plone_app_contenttypes_installed(self):
        """ News Item should be not Globally Allowed
        """
        types = ['Collection',
                 'Document',
                 'Event',
                 'File',
                 'Folder',
                 'Image',
                 'Link',
                 'News Item']
        for t in types:
            self.assertTrue(t in self.pt.objectIds())
            type_info = self.pt['News Item']
            self.assertTrue('plone.app.contenttype' in type_info.klass)

    def test_cover_installed(self):
        self.assertTrue('collective.cover.content' in self.pt.objectIds())

    def test_cover_searchable_types(self):
        self.registry = getUtility(IRegistry)
        configs = self.registry.forInterface(ICoverSettings)
        searchable_content_types = configs.searchable_content_types
        types = [u'collective.nitf.content',
                 u'collective.polls.poll',
                 u'Collection',
                 u'FormFolder',
                 u'Image',
                 u'Document',
                 u'Link']
        for t in types:
            self.assertTrue(t in searchable_content_types)

    def test_cover_insert(self):
        with api.env.adopt_roles(roles=['Manager']):
            cover = api.content.create(
                container=self.portal,
                type='collective.cover.content',
                title='Cover Insert Test',
                template_layout='Destaques',
            )
        self.assertTrue(cover)

    def test_poll_installed(self):
        self.assertTrue('collective.polls.poll' in self.pt.objectIds())

    def test_content_behavior_related_items(self):
        types = ['Collection',
                 'Document',
                 'Event',
                 'File',
                 'Folder',
                 'Image']
        # NITF possui um campo proprio, por isto nao precisamos testar
        for t in types:
            fti = self.pt[t]
            self.assertTrue('plone.app.relationfield.behavior.IRelatedItems' in
                            fti.behaviors,
                            'Tipo %s nao permite conteudo relacionado' % t)

    def test_content_behavior_vcge(self):
        types = ['Collection',
                 'Document',
                 'Event',
                 'File',
                 'Folder',
                 'Image',
                 'Link',
                 'collective.nitf.content',
                 'collective.polls.poll']
        for t in types:
            fti = self.pt[t]
            self.assertTrue('brasil.gov.vcge.dx.behaviors.IVCGE' in
                            fti.behaviors,
                            'Tipo %s nao suporta o VCGE' % t)

    def test_link_patched(self):
        with api.env.adopt_roles(['Manager']):
            plone = api.content.create(
                type='Link',
                container=self.portal,
                id='plone_foundation',
                title=u'Plone Foundation',
            )
        plone.remoteUrl = 'http://plone.org/foundation'
        self.assertEqual(plone.getRemoteUrl(), plone.remoteUrl)

    def test_remote_url_utils(self):
        portal_url = self.portal['portal_url']()
        remote_url_utils = self.portal.restrictedTraverse('@@remote_url_utils')
        # no url
        path = ''
        url = ''
        final_url = remote_url_utils.remote_url_transform(path, url)
        self.assertEqual(final_url, url)
        # no path
        path = ''
        url = 'http://plone.org/foundation'
        final_url = remote_url_utils.remote_url_transform(path, url)
        self.assertEqual(final_url, url)
        # http or https
        path = '/plone/assuntos/editoria-a/link-externo'
        url = 'http://plone.org/foundation'
        final_url = remote_url_utils.remote_url_transform(path, url)
        self.assertEqual(final_url, url)
        # use schema
        path = '/plone/assuntos/editoria-a/link-mailto'
        url = 'mailto:username@domainname'
        final_url = remote_url_utils.remote_url_transform(path, url)
        self.assertEqual(final_url, url)
        # ./
        path = '/plone/assuntos/editoria-a/link-relative'
        url = './segundo-nivel'
        final_url = remote_url_utils.remote_url_transform(path, url)
        self.assertEqual(
            final_url,
            '{0}/assuntos/editoria-a/segundo-nivel'.format(portal_url),
        )
        # ../
        path = '/plone/assuntos/editoria-a/link-relative'
        url = '../editoria-b'
        final_url = remote_url_utils.remote_url_transform(path, url)
        self.assertEqual(
            final_url,
            '{0}/assuntos/editoria-b'.format(portal_url),
        )
        # ../../
        path = '/plone/assuntos/editoria-a/link-relative'
        url = '../../acesso-a-informacao/informacoes-classificadas'
        final_url = remote_url_utils.remote_url_transform(path, url)
        self.assertEqual(
            final_url,
            '{0}/acesso-a-informacao/informacoes-classificadas'.format(
                portal_url,
            ),
        )
        # /path/site
        path = '/plone/assuntos/editoria-a/link-internal'
        url = '/plone/acesso-a-informacao/informacoes-classificadas'
        final_url = remote_url_utils.remote_url_transform(path, url)
        self.assertEqual(
            final_url,
            '{0}/acesso-a-informacao/informacoes-classificadas'.format(
                portal_url,
            ),
        )
