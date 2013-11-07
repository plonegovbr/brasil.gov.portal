# -*- coding:utf-8 -*-
from brasil.gov.portal.content.audio_file import IMPEGAudioFile
from brasil.gov.portal.content.audio_file import IOGGAudioFile
from five import grok
from plone.dexterity.content import Container
from zope.lifecycleevent.interfaces import IObjectAddedEvent
from zope.lifecycleevent.interfaces import IObjectRemovedEvent
from zope.interface import implements
from zope.interface import Interface


class IAudio(Interface):
    ''' Representa um Audio '''


class Audio(Container):
    implements(IAudio)

    def return_ogg(self):
        sources = self.objectValues()
        for source in sources:
            if IOGGAudioFile.providedBy(source):
                return source

    def return_mp3(self):
        sources = self.objectValues()
        for source in sources:
            if IMPEGAudioFile.providedBy(source):
                return source

    def setCreators(self, creators):
        """Set creators to the object and repply to it's childs
        """
        super(Container, self).setCreators(creators)
        self.reindexObject()
        for brain in self.listFolderContents():
            brain.setCreators(creators)
            brain.reindexObject()


@grok.subscribe(IObjectAddedEvent)
def object_added(event, obj=None):
    if not obj:
        obj = event.object
    parent = event.newParent
    if IAudio.providedBy(parent):
        if IMPEGAudioFile.providedBy(obj):
            permission = 'brasil.gov.portal: Add MPEG File'
        elif IOGGAudioFile.providedBy(obj):
            permission = 'brasil.gov.portal: Add OGG File'
        if permission:
            parent.manage_permission(permission, roles=[], acquire=0)


@grok.subscribe(IObjectRemovedEvent)
def object_removed(event, obj=None):
    if not obj:
        obj = event.object
    parent = event.oldParent
    if IAudio.providedBy(parent):
        if IMPEGAudioFile.providedBy(obj):
            permission = 'brasil.gov.portal: Add MPEG File'
        elif IOGGAudioFile.providedBy(obj):
            permission = 'brasil.gov.portal: Add OGG File'
        if permission:
            parent.manage_permission(permission, roles=[], acquire=1)
