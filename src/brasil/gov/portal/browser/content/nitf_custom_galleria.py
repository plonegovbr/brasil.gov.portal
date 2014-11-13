# -*- coding: utf-8 -*-
from brasil.gov.portal.interfaces import IBrasilGov
from collective.nitf.browser import Nitf_Galleria as NitfCustomGalleria
from five import grok

grok.templatedir('templates')


class Nitf_Galleria(NitfCustomGalleria):
    """Customize NITF view
    """
    grok.layer(IBrasilGov)
    grok.name('nitf_custom_galleria')
    grok.template('nitf_custom_galleria')
