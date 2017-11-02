# -*- coding: utf-8 -*-
from brasil.gov.portal import bbb  # noqa: F401
from brasil.gov.portal import patches
from zope.i18nmessageid import MessageFactory


_ = MessageFactory('brasil.gov.portal')


patches.run()
