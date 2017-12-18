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


def run():
    link()
