# -*- coding: utf-8 -*-
from brasil.gov.portal.interfaces import IBrasilGov
from collective.nitf.browser import Display_Macros as NitfCustomDisplayMacros
from five import grok

grok.templatedir('templates')


class Display_Macros(NitfCustomDisplayMacros):
    """Customize NITF view
    """
    grok.layer(IBrasilGov)
    grok.name('nitf_custom_displaymacros')
    grok.template('nitf_custom_displaymacros')
