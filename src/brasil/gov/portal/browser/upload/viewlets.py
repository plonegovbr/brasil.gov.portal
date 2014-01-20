# -*- coding: utf-8 -*-
from five import grok
from plone.app.layout.viewlets.interfaces import IHtmlHead
from zope.interface import Interface
from collective.upload import viewlets


grok.templatedir("templates")


class Tmpls(viewlets.Tmpls):
    grok.context(Interface)
    grok.name(u"collective.upload.tmpls")
    grok.require("cmf.AddPortalContent")
    grok.template("tmpls")
    grok.viewletmanager(IHtmlHead)
