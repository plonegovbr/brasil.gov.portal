# -*- coding:utf-8 -*-
from brasil.gov.portal.config import PROJECTNAME
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


def run():
    outputfilters()
