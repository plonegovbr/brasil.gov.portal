# -*- coding: utf-8 -*-
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
from plone.app.layout.viewlets.content import DocumentBylineViewlet
from plone.memoize import ram
from time import time


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
