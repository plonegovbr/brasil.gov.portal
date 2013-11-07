# -*- coding:utf-8 -*-
from brasil.gov.portal.config import PROJECTNAME
from collective.z3cform.widgets.multicontent_search_widget import (
    MultiContentSearchFieldWidget
)
from plone.app.contenttypes.content import Link
from plone.app.relationfield.behavior import IRelatedItems
from plone.app.workflow.browser.sharing import SharingView
from plone.autoform.interfaces import WIDGETS_KEY
from plone.outputfilters.filters import resolveuid_and_caption as base

from Products.PloneFormGen.content.form import FormFolder
from collective.nitf.content import NITF
from Products.Doormat.content.DoormatColumn import DoormatColumn
from Products.Doormat.content.DoormatSection import DoormatSection
from Products.Doormat.content.Doormat import Doormat

FOLDERISH_CLASSES = [
    FormFolder,
    NITF,
    DoormatColumn,
    DoormatSection,
    Doormat
]


import logging

logger = logging.getLogger(PROJECTNAME)


def outputfilters():
    def patched_call(self, data):
        ''' Patch original __call__ '''
        data = data.replace('/>', ' />')
        return self.__orig_call__(data)

    setattr(base.ResolveUIDAndCaptionFilter,
            '__orig_call__',
            base.ResolveUIDAndCaptionFilter.__call__)

    setattr(base.ResolveUIDAndCaptionFilter,
            '__call__',
            patched_call)
    logger.info('Patched ResolveUIDAndCaptionFilter')


def link():
    def getRemoteUrl(self):
        return self.remoteUrl

    setattr(Link,
            'getRemoteUrl',
            getRemoteUrl)
    logger.info('Patched Link content type')


def related_items_widget():
    IRelatedItems.setTaggedValue(
        WIDGETS_KEY,
        {'relatedItems': MultiContentSearchFieldWidget}
    )
    logger.info('Patched Related Items widget')


def sharing():
    def updateSharingInfo(self, search_term=''):
        data = self._updateSharingInfo(search_term)
        self.request.response.setHeader('Content-Type',
                                        'application/json;charset=utf-8')
        return data

    setattr(SharingView,
            '_updateSharingInfo',
            SharingView.updateSharingInfo)
    setattr(SharingView,
            'updateSharingInfo',
            updateSharingInfo)
    logger.info('Patched sharing tab')


def repplyCreatorToChilds():
    """Change behaviour of folderish objects to repply creators to its childs
       since some of these objects don't have option to change childs creators
    """

    def setCreators(self, creators):
        """Set creators to the object and repply to it's childs
        """
        self._setCreators(creators)
        self.reindexObject()
        for brain in self.listFolderContents():
            brain.setCreators(creators)
            brain.reindexObject()

    for cls in FOLDERISH_CLASSES:
        setattr(cls,
                '_setCreators',
                cls.setCreators)
        setattr(cls,
                'setCreators',
                setCreators)
        logger.info('Patched setCreator of {0}'.format(cls.__name__))


def run():
    outputfilters()
    link()
    related_items_widget()
    sharing()
    repplyCreatorToChilds()
