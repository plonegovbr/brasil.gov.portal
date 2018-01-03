# -*- coding: utf-8 -*-
from brasil.gov.portal.logger import logger
from plone.app.contenttypes.content import Link


def link():
    def getRemoteUrl(self):
        return self.remoteUrl

    setattr(Link,
            'getRemoteUrl',
            getRemoteUrl)
    logger.warn('Patched Link content type')


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
    link()
