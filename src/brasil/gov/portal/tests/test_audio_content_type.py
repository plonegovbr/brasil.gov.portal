# -*- coding: utf-8 -*-
from AccessControl import getSecurityManager
from brasil.gov.portal.browser.content.audio import AudioView
from brasil.gov.portal.content.audio import IAudio
from brasil.gov.portal.content.audio_file import IMPEGAudioFile
from brasil.gov.portal.content.audio_file import IOGGAudioFile
from brasil.gov.portal.testing import INTEGRATION_TESTING
from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.dexterity.interfaces import IDexterityFTI
from plone.dexterity.schema import SCHEMA_CACHE
from plone.namedfile.file import NamedBlobFile
from zope.component import createObject
from zope.component import queryUtility
from zope.interface import Invalid

import os
import unittest


class AudioTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        # Invalidate schema cache
        SCHEMA_CACHE.invalidate('Audio')
        SCHEMA_CACHE.invalidate('MPEG Audio File')
        SCHEMA_CACHE.invalidate('OGG Audio File')
        self.folder = api.content.create(
            type='Folder',
            container=self.portal,
            id='test-folder'
        )
        self.audio = api.content.create(
            type='Audio',
            container=self.folder,
            id='my-audio'
        )
        self.setup_content_data()

    def setup_content_data(self):
        path = os.path.dirname(__file__)
        mp3_audio = open(os.path.join(path, 'files', 'file.mp3')).read()
        ogg_audio = open(os.path.join(path, 'files', 'file.ogg')).read()
        self.mp3 = NamedBlobFile(mp3_audio, 'audio/mp3', u'file.mp3')
        self.ogg = NamedBlobFile(ogg_audio, 'audio/ogg', u'file.ogg')

    def test_adding(self):
        self.assertTrue(IAudio.providedBy(self.audio))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='Audio')
        self.assertNotEqual(None, fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='Audio')
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(IAudio.providedBy(new_object))

    def test_return_mp3(self):
        audio = self.audio
        self.assertIsNone(audio.return_mp3())
        # Now we add an mp3 file
        mp3_file = api.content.create(
            type='MPEG Audio File',
            container=audio,
            id='file.mp3'
        )
        mp3_file.file = self.mp3
        self.assertEqual(audio.return_mp3(), mp3_file)

    def test_return_ogg(self):
        audio = self.audio
        self.assertIsNone(audio.return_ogg())
        # Now we add an ogg file
        ogg_file = api.content.create(
            type='OGG Audio File',
            container=audio,
            id='file.ogg'
        )
        self.assertEqual(audio.return_ogg(), ogg_file)

    def test_mp3_add_permission(self):
        sm = getSecurityManager()
        permission = 'brasil.gov.portal: Add MPEG File'
        audio = self.audio
        self.assertTrue(sm.checkPermission(permission, audio))
        # Adicionamos um arquivo MP3
        mp3_file = api.content.create(
            type='MPEG Audio File',
            container=audio,
            id='file.mp3'
        )
        mp3_file.file = self.mp3
        self.assertFalse(sm.checkPermission(permission, audio))
        # Removendo o arquivo, a permissao volta a ser dada
        audio.manage_delObjects(['file.mp3'])
        self.assertTrue(sm.checkPermission(permission, audio))

    def test_ogg_add_permission(self):
        sm = getSecurityManager()
        permission = 'brasil.gov.portal: Add OGG File'
        audio = self.audio
        self.assertTrue(sm.checkPermission(permission, audio))
        # Adicionamos um arquivo OGG
        ogg_file = api.content.create(
            type='OGG Audio File',
            container=audio,
            id='file.ogg'
        )
        ogg_file.file = self.ogg
        self.assertFalse(sm.checkPermission(permission, audio))
        # Removendo o arquivo, a permissao volta a ser dada
        audio.manage_delObjects(['file.ogg'])
        self.assertTrue(sm.checkPermission(permission, audio))


class MPEGAudioFileTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        # Invalidate schema cache
        SCHEMA_CACHE.invalidate('Audio')
        SCHEMA_CACHE.invalidate('MPEG Audio File')
        self.folder = api.content.create(
            type='Folder',
            container=self.portal,
            id='test-folder'
        )
        self.audio = api.content.create(
            type='Audio',
            container=self.folder,
            id='my-audio'
        )
        self.setup_content_data()
        self.mp3_audio = api.content.create(
            type='MPEG Audio File',
            container=self.audio,
            id='file.mp3'
        )
        self.mp3_audio.file = self.mp3
        self.mp3_audio.reindexObject()

    def setup_content_data(self):
        path = os.path.dirname(__file__)
        mp3_audio = open(os.path.join(path, 'files', 'file.mp3')).read()
        ogg_audio = open(os.path.join(path, 'files', 'file.ogg')).read()
        self.mp3 = NamedBlobFile(mp3_audio, 'audio/mp3', u'file.mp3')
        self.ogg = NamedBlobFile(ogg_audio, 'audio/ogg', u'file.ogg')

    def test_adding(self):
        self.assertTrue(IMPEGAudioFile.providedBy(self.mp3_audio))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='MPEG Audio File')
        self.assertNotEqual(None, fti)

    def test_validate_mpeg(self):
        from brasil.gov.portal.content.audio_file import validate_mpeg
        self.assertTrue(validate_mpeg(self.mp3))
        self.assertRaises(Invalid, validate_mpeg, self.ogg)

    def test_file_content_type(self):
        self.assertEqual(self.mp3_audio.content_type, 'audio/mp3')


class OGGAudioFileTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        # Invalidate schema cache
        SCHEMA_CACHE.invalidate('Audio')
        SCHEMA_CACHE.invalidate('OGG Audio File')
        self.folder = api.content.create(
            type='Folder',
            container=self.portal,
            id='test-folder'
        )
        self.audio = api.content.create(
            type='Audio',
            container=self.folder,
            id='my-audio'
        )
        self.setup_content_data()
        self.ogg_audio = api.content.create(
            type='OGG Audio File',
            container=self.audio,
            id='file.ogg'
        )
        self.ogg_audio.file = self.ogg
        self.ogg_audio.reindexObject()

    def setup_content_data(self):
        path = os.path.dirname(__file__)
        mp3_audio = open(os.path.join(path, 'files', 'file.mp3')).read()
        ogg_audio = open(os.path.join(path, 'files', 'file.ogg')).read()
        self.mp3 = NamedBlobFile(mp3_audio, 'audio/mp3', u'file.mp3')
        self.ogg = NamedBlobFile(ogg_audio, 'audio/ogg', u'file.ogg')

    def test_adding(self):
        self.assertTrue(IOGGAudioFile.providedBy(self.ogg_audio))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='OGG Audio File')
        self.assertNotEqual(None, fti)

    def test_validate_ogg(self):
        from brasil.gov.portal.content.audio_file import validate_ogg
        self.assertTrue(validate_ogg(self.ogg))
        self.assertRaises(Invalid, validate_ogg, self.mp3)

    def test_file_content_type(self):
        self.assertEqual(self.ogg_audio.content_type, 'audio/ogg')


class AudioViewTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        # Invalidate schema cache
        SCHEMA_CACHE.invalidate('Audio')
        SCHEMA_CACHE.invalidate('MPEG Audio File')
        SCHEMA_CACHE.invalidate('OGG Audio File')
        self.folder = api.content.create(
            type='Folder',
            container=self.portal,
            id='test-folder'
        )
        self.audio = api.content.create(
            type='Audio',
            container=self.folder,
            id='my-audio'
        )
        self.setup_content_data()

    def setup_content_data(self):
        audio = self.audio
        path = os.path.dirname(__file__)
        mp3_audio = open(os.path.join(path, 'files', 'file.mp3')).read()
        audio.invokeFactory('MPEG Audio File', 'file.mp3')
        audio['file.mp3'].file = NamedBlobFile(mp3_audio,
                                               'audio/mp3',
                                               u'file.mp3')
        ogg_audio = open(os.path.join(path, 'files', 'file.ogg')).read()
        audio.invokeFactory('OGG Audio File', 'file.ogg')
        audio['file.ogg'].file = NamedBlobFile(ogg_audio,
                                               'audio/ogg',
                                               u'file.ogg')

    def test_view(self):
        view = self.audio.restrictedTraverse('@@view')
        self.assertTrue(isinstance(view, AudioView))

    def test_sources(self):
        view = self.audio.restrictedTraverse('@@view')
        self.assertEqual(len(view.sources()), 2)

    def test_downloads(self):
        view = self.audio.restrictedTraverse('@@view')
        downloads = view.downloads()
        self.assertEqual(len(downloads), 2)
