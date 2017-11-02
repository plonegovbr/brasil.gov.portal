# -*- coding: utf-8 -*-
from brasil.gov.portal import _
from plone.dexterity.content import Item
from plone.directives import form
from plone.indexer.decorator import indexer
from plone.namedfile.field import NamedBlobFile
from plone.rfc822.interfaces import IPrimaryFieldInfo
from plone.supermodel import model
from zope.interface import implements
from zope.interface import Invalid


OGGTYPES = [
    'audio/ogg',
    'audio/x-ogg',
]

MPEGTYPES = [
    'audio/mp3',
    'audio/mpeg',
    'audio/x-mp3',
    'audio/x-mpeg',
]


def validate_mimetype(value, audiotypes):
    if value.contentType not in audiotypes:
        raise Invalid(_(u'File format not supported'))
    return True


def validate_mpeg(value):
    return validate_mimetype(value, MPEGTYPES)


def validate_ogg(value):
    return validate_mimetype(value, OGGTYPES)


class IMPEGAudioFile(form.Schema):
    """ Representa um Arquivo de Audio MPEG"""

    model.primary('file')
    file = NamedBlobFile(title=_(u'File'),
                         description=_(u'Please upload a audio file.'),
                         required=True,
                         constraint=validate_mpeg)


class IOGGAudioFile(form.Schema):
    """ Representa um Arquivo de Audio OGG"""

    model.primary('file')
    file = NamedBlobFile(title=_(u'File'),
                         description=_(u'Please upload a audio file.'),
                         required=True,
                         constraint=validate_ogg)


class AudioFile(Item):

    @property
    def content_type(self):
        """ Retorna o mimetype do conteudo """
        file = self.file
        if file:
            return file.contentType


class MPEGAudioFile(AudioFile):
    implements(IMPEGAudioFile)


class OGGAudioFile(AudioFile):
    implements(IOGGAudioFile)


@indexer(IMPEGAudioFile)
@indexer(IOGGAudioFile)
def getObjSize_file(obj):
    primary_field_info = IPrimaryFieldInfo(obj)
    return obj.getObjSize(None, primary_field_info.value.size)
