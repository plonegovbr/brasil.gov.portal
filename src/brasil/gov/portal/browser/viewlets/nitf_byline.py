# -*- coding: utf-8 -*-
from collective.nitf.browser import NITFBylineViewlet as CollectiveNITFBylineViewlet
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getMultiAdapter


class NITFBylineViewlet(CollectiveNITFBylineViewlet):

    index = ViewPageTemplateFile('templates/nitf_byline.pt')

    def mostra_autor(self):
        """Verifica se a configuração do portal pede para mostrar o autor."""
        portal_settings = getMultiAdapter((self.context, self.context.REQUEST),
                                          name='portal_settings')
        return not portal_settings.get_esconde_autor()

    def mostra_data(self):
        """Verifica se a configuração do portal pede para mostrar a data."""
        portal_settings = getMultiAdapter((self.context, self.context.REQUEST),
                                          name='portal_settings')
        return not portal_settings.get_esconde_data()
