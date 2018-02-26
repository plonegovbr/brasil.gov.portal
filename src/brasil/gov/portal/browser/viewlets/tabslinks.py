# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from plone.app.layout.viewlets import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getMultiAdapter


class TabsLinksViewlet(ViewletBase):
    index = ViewPageTemplateFile('templates/tabslinks.pt')

    def update(self):
        context = aq_inner(self.context)
        portal_tabs_view = getMultiAdapter((context, self.request), name='portal_tabs_view')
        self.portal_tabs = portal_tabs_view.topLevelTabs(category='portal_tabs_links')
