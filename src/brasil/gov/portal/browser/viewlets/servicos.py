# -*- coding: utf-8 -*-
""" Modulo que implementa o viewlet de servicos do Portal"""
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import ViewletBase


class ServicosViewlet(ViewletBase):
    ''' Viewlet de listagem de servicos
    '''
    # Indica qual o template sera usado por este viewlet
    index = ViewPageTemplateFile('templates/servicos.pt')

    def update(self):
        ''' Prepara/Atualiza os valores utilizados pelo Viewlet
        '''
        super(ServicosViewlet, self).update()
        ps = self.context.restrictedTraverse('@@plone_portal_state')
        tools = self.context.restrictedTraverse('@@plone_tools')
        portal = ps.portal()
        self._folder = 'servicos' in portal.objectIds() and portal['servicos']
        self._ct = tools.catalog()

    def available(self):
        return self._folder and True or False

    def servicos(self):
        ct = self._ct
        folder_path = '/'.join(self._folder.getPhysicalPath())
        portal_types = ['Link', ]
        results = ct.searchResults(portal_type=portal_types,
                                   path=folder_path,
                                   sort_on='getObjPositionInParent')
        return results
