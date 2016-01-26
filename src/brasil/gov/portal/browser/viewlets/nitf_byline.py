# -*- coding: utf-8 -*-
from plone import api
from plone.app.layout.viewlets.content import DocumentBylineViewlet
from plone.memoize import ram
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from time import time
from zope.component import getMultiAdapter


class NITFBylineViewlet(DocumentBylineViewlet):

    index = ViewPageTemplateFile('templates/nitf_byline.pt')

    @ram.cache(lambda method, self, fullname: (time() // 60, fullname))
    def getMemberInfoByName(self, fullname):
        mt = api.portal.get_tool('portal_membership')
        members = mt.searchForMembers(name=fullname)
        if members:
            member = members[0].getUserId()  # we care only about the first
            return mt.getMemberInfo(member)

    def byline(self):
        member = self.getMemberInfoByName(self.context.byline)
        if member:
            return member['username']

    def author(self):
        return self.getMemberInfoByName(self.context.byline)

    def authorname(self):
        return self.context.byline

    def mostra_autor(self):
        """Verifica se a configuração do portal pede para mostrar o autor."""
        portal_settings = getMultiAdapter((self.context, self.context.REQUEST),
                                          name='portal_settings')
        return not portal_settings.get_esconde_autor()

    def mostra_data(self):
        """Verifica se a configuração do portal pede para mostrar a data."""
        portal_settings = getMultiAdapter((self.context, self.context.REQUEST),
                                          name='portal_settings')
        return not portal_settings.get_esconde_data()
