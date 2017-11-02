# -*- coding: utf-8 -*-
from plone import api
from plone.app.layout.viewlets import ViewletBase
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class PortalHeadViewlet(ViewletBase):
    index = ViewPageTemplateFile('templates/portal_head.pt')

    def update(self):
        """Prepara/Atualiza os valores utilizados pelo Viewlet"""
        super(PortalHeadViewlet, self).update()
        # Disponibiliza uma variavel site_url que retorna a raiz do
        # site Plone. No template ela pode ser chamada como view/site_url
        portal = api.portal.get()
        self.pprop = getToolByName(portal, 'portal_properties')
        configs = getattr(self.pprop, 'brasil_gov', None)
        self.url_orgao = configs.getProperty('url_orgao', u'')
