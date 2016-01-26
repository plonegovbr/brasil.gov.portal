# -*- coding: utf-8 -*-
"""Customiza DocumentBylineViewlet do plone.app.layout."""

from plone.app.layout.viewlets.content import DocumentBylineViewlet as DBLV
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getMultiAdapter


class DocumentBylineViewlet(DBLV):
    """Customiza DocumentBylineViewlet do plone.app.layout, para considerar
    configurações do portal sobre esconder autor e esconder data de publicação.
    """
    index = ViewPageTemplateFile('templates/document_byline.pt')

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
