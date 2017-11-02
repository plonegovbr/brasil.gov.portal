# -*- coding: utf-8 -*-
""" Modulo que implementa o viewlet de redes sociais do Portal"""
from brasil.gov.portal.config import REDES
from plone.app.layout.viewlets import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class RedesSociaisViewlet(ViewletBase):
    """ Viewlet de redes sociais
    """
    # Indica qual o template sera usado por este viewlet
    index = ViewPageTemplateFile('templates/redessociais.pt')

    redes = []

    def update(self):
        """ Prepara/Atualiza os valores utilizados pelo Viewlet
        """
        super(RedesSociaisViewlet, self).update()
        tools = self.context.restrictedTraverse('@@plone_tools')
        pp = tools.properties()
        configs = getattr(pp, 'brasil_gov', None)
        redes = {}
        for rede in REDES:
            redes[rede['id']] = rede
        if configs:
            data = configs.getProperty('social_networks', [])
            selected = []
            for item in data:
                k, v = item.split('|')
                rede_info = redes[k]
                selected.append({'site': k,
                                 'title': rede_info['title'],
                                 'info': v,
                                 'url': rede_info['url'] % v})
            self.redes = selected

    def available(self):
        return self.redes and True or False
