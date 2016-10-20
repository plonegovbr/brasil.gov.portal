# -*- coding: utf-8 -*-
# noqa em bbb devido a
# F401 'bbb' imported but unused
from brasil.gov.portal import bbb  # noqa
from brasil.gov.portal import patches
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('brasil.gov.portal')


patches.run()
