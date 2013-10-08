# -*- coding: utf-8 -*-
from DateTime import DateTime
from plone.app.layout.viewlets.content import DocumentBylineViewlet
from Products.CMFPlone.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class NITFBylineViewlet(DocumentBylineViewlet):

    index = ViewPageTemplateFile("templates/nitf_byline.pt")

    def getMemberInfoByName(self, fullname):
        membership = getToolByName(self.context, 'portal_membership')
        members = membership.searchForMembers(name=fullname)
        if members:
            member = members[0].getUserId()  # we care only about the first
            return membership.getMemberInfo(member)

    def byline(self):
        member = self.getMemberInfoByName(self.context.byline)
        if member:
            return member['username']

    def author(self):
        return self.getMemberInfoByName(self.context.byline)

    def authorname(self):
        return self.context.byline

    def pub_date(self):
        """Return object effective date.

        Return None if publication date is switched off in global site settings
        or if Effective Date is not set on object.
        """
        if PLONE_VERSION >= '4.3':
            return super(NITFBylineViewlet, self).pub_date()  # use parent's method

        # compatibility for Plone < 4.3
        # check if we are allowed to display publication date
        properties = getToolByName(self.context, 'portal_properties')
        site_properties = getattr(properties, 'site_properties')
        if not site_properties.getProperty('displayPublicationDateInByline'):
            return None

        # check if we have Effective Date set
        date = self.context.EffectiveDate()
        if not date or date == 'None':
            return None

        return DateTime(date)
