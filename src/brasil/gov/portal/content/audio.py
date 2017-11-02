# -*- coding: utf-8 -*-
"""Audio content type and subscribers associated with it.

An Audio is a container of audio formats: MP3 (MPEGAudioFile) and
Vorbis (OGGAudioFile) and can only hold one file of each format,
that's is handled by a couple of subscribers.
"""
from brasil.gov.portal.content.audio_file import IMPEGAudioFile
from brasil.gov.portal.content.audio_file import IOGGAudioFile
from plone.dexterity.content import Container
from zope.interface import implements
from zope.interface import Interface


class IAudio(Interface):
    """An Audio (in fact a container of audio formats)."""


class Audio(Container):
    implements(IAudio)

    def return_ogg(self):
        """Return the Vorbis version of the audio."""
        sources = self.objectValues()
        for source in sources:
            if IOGGAudioFile.providedBy(source):
                return source

    def return_mp3(self):
        """Return the MP3 version of the audio."""
        sources = self.objectValues()
        for source in sources:
            if IMPEGAudioFile.providedBy(source):
                return source


def object_added(obj, event):
    """Remove further permission to add a file type after adding it."""
    parent = event.newParent
    if IAudio.providedBy(parent):
        if IMPEGAudioFile.providedBy(obj):
            permission = 'brasil.gov.portal: Add MPEG File'
        elif IOGGAudioFile.providedBy(obj):
            permission = 'brasil.gov.portal: Add OGG File'
        if permission:
            parent.manage_permission(permission, roles=[], acquire=0)


def object_removed(obj, event):
    """Grant permission to add a file type after removing it."""
    parent = event.oldParent
    if IAudio.providedBy(parent):
        if IMPEGAudioFile.providedBy(obj):
            permission = 'brasil.gov.portal: Add MPEG File'
        elif IOGGAudioFile.providedBy(obj):
            permission = 'brasil.gov.portal: Add OGG File'
        if permission:
            parent.manage_permission(permission, roles=[], acquire=1)
