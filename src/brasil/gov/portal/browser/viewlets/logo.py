# -*- coding: utf-8 -*-
""" Modulo que implementa o viewlet de logo do Portal"""
from plone.app.layout.viewlets.common import LogoViewlet as ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class LogoViewlet(ViewletBase):
    ''' Viewlet de redes sociais
    '''
    # Indica qual o template sera usado por este viewlet
    index = ViewPageTemplateFile('templates/logo.pt')
