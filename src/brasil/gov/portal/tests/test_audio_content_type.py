# -*- coding: utf-8 -*-
from AccessControl import getSecurityManager
from brasil.gov.portal.content.audio import IAudio
from brasil.gov.portal.content.audio_file import IMPEGAudioFile
from brasil.gov.portal.content.audio_file import IOGGAudioFile
from brasil.gov.portal.testing import INTEGRATION_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from plone.dexterity.schema import SCHEMA_CACHE
from plone.namedfile.file import NamedBlobFile
from zope.component import createObject
from zope.component import queryUtility
from zope.interface import Invalid

import os
import unittest2 as unittest


class AudioTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        # Invalidate schema cache
        SCHEMA_CACHE.invalidate('Audio')
        SCHEMA_CACHE.invalidate('MPEG Audio File')
        SCHEMA_CACHE.invalidate('OGG Audio File')
        self.folder = self.portal['test-folder']
        audio_id = self.folder.invokeFactory('Audio', 'my-audio')
        self.audio = self.folder[audio_id]
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
        oId = audio.invokeFactory('MPEG Audio File', 'file.mp3')
        mp3_file = audio[oId]
        mp3_file.file = self.mp3
        self.assertEqual(audio.return_mp3(), mp3_file)

    def test_return_ogg(self):
        audio = self.audio
        self.assertIsNone(audio.return_ogg())
        # Now we add an ogg file
        oId = audio.invokeFactory('OGG Audio File', 'file.ogg')
        ogg_file = audio[oId]
        ogg_file.file = self.ogg
        self.assertEqual(audio.return_ogg(), ogg_file)

    def test_mp3_add_permission(self):
        sm = getSecurityManager()
        permission = 'brasil.gov.portal: Add MPEG File'
        audio = self.audio
        self.assertTrue(sm.checkPermission(permission, audio))
        # Adicionamos um arquivo MP3
        oId = audio.invokeFactory('MPEG Audio File', 'file.mp3')
        mp3_file = audio[oId]
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
        oId = audio.invokeFactory('OGG Audio File', 'file.ogg')
        ogg_file = audio[oId]
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
        self.portal.invokeFactory('Folder', 'test-folder')
        # Invalidate schema cache
        SCHEMA_CACHE.invalidate('Audio')
        SCHEMA_CACHE.invalidate('MPEG Audio File')
        self.folder = self.portal['test-folder']
        audio_id = self.folder.invokeFactory('Audio', 'my-audio')
        self.audio = self.folder[audio_id]
        self.setup_content_data()
        self.audio.invokeFactory('MPEG Audio File', 'file.mp3')
        self.mp3_audio = self.audio['file.mp3']

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


class OGGAudioFileTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        # Invalidate schema cache
        SCHEMA_CACHE.invalidate('Audio')
        SCHEMA_CACHE.invalidate('OGG Audio File')
        self.folder = self.portal['test-folder']
        audio_id = self.folder.invokeFactory('Audio', 'my-audio')
        self.audio = self.folder[audio_id]
        self.setup_content_data()
        self.audio.invokeFactory('OGG Audio File', 'file.ogg')
        self.ogg_audio = self.audio['file.ogg']

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
