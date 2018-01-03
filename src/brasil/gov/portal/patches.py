# -*- coding: utf-8 -*-
from brasil.gov.portal.logger import logger
from plone.app.contenttypes.content import Link
from plone.outputfilters.filters import resolveuid_and_caption as base


def outputfilters():
    def patched_call(self, data):
        """ Patch original __call__ """
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


# XXXX: this patch should be removed when this is fixed:
#       https://github.com/zopefoundation/z3c.form/pull/76
def deselect(self):
    selecteditems = []
    notselecteditems = []
    for selecteditem in self.selectedItems:
        selecteditems.append(selecteditem['value'])
    for item in self.items:
        if not item['value'] in selecteditems:
            notselecteditems.append(item)
    return notselecteditems


def run():
    outputfilters()
    link()
