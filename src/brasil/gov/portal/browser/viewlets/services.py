# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from plone.app.layout.viewlets import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getMultiAdapter


class ServicesViewlet(ViewletBase):
    index = ViewPageTemplateFile('templates/services.pt')

    def update(self):
        super(ServicesViewlet, self).update()

        context = aq_inner(self.context)
        portal_services_view = getMultiAdapter((context, self.request), name='plone_context_state')
        self.portal_services = portal_services_view.actions('portal_services')
