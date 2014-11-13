# -*- coding: utf-8 -*-
from brasil.gov.portal.config import PROJECTNAME
from collective.z3cform.widgets.multicontent_search_widget import MultiContentSearchFieldWidget
from plone.app.contenttypes.content import Link
from plone.app.relationfield.behavior import IRelatedItems
from plone.autoform.interfaces import WIDGETS_KEY
from plone.outputfilters.filters import resolveuid_and_caption as base


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


def run():
    outputfilters()
    link()
    related_items_widget()
