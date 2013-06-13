# -*- coding: utf-8 -*-
""" Modulo que implementa o viewlet de logo do Portal"""
from plone.app.layout.viewlets.common import LogoViewlet as ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class LogoViewlet(ViewletBase):
    ''' Viewlet de redes sociais
    '''
    # Indica qual o template sera usado por este viewlet
    index = ViewPageTemplateFile('templates/logo.pt')

    def portal(self):
        ps = self.context.restrictedTraverse('@@plone_portal_state')
        portal = ps.portal()
        return portal

    def title(self):
        ''' Retorna o titulo do portal
        '''
        portal = self.portal()
        return getattr(portal, 'title', 'Portal Brasil')

    def title_1(self):
        ''' Retorna a primeira linha do titulo do portal
        '''
        portal = self.portal()
        return getattr(portal, 'title_1', 'Secretaria de')

    def title_2(self):
        ''' Retorna a primeira linha do titulo do portal
        '''
        portal = self.portal()
        return getattr(portal, 'title_2',
                       u'Comunicação Social')

    def title_2_class(self):
        ''' Definimos a classe a ser aplicada ao title_2
            com base no tamanho da string
        '''
        title_2 = self.title_2()
        return 'luongo' if len(title_2) > 22 else 'corto'

    def orgao(self):
        ''' Retorna o nome do orgao ao qual este portal
            esta vinculado
        '''
        portal = self.portal()
        return getattr(portal, 'orgao', '')

    def description(self):
        ''' Retorna uma breve descricao do portal
        '''
        portal = self.portal()
        return getattr(portal, 'description', '')
