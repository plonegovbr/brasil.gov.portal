# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from plone.app.layout.viewlets import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getMultiAdapter


class ServicesViewlet(ViewletBase):
    index = ViewPageTemplateFile('templates/services.pt')

    def update(self):
        context = aq_inner(self.context)
        portal_services_view = getMultiAdapter((context, self.request), name='portal_tabs_view')
        self.portal_tabs = portal_services_view.topLevelTabs(category='portal_services')
