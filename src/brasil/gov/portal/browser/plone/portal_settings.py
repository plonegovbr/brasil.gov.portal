# -*- coding: utf-8 -*-
"""Views"""

from brasil.gov.portal.browser.plone.interfaces import IPortalSettingsView
from plone import api
from Products.Five import BrowserView
from zope.interface import implements


class PortalSettingsView(BrowserView):
    """View para obter configurações do portal."""
    implements(IPortalSettingsView)

    def get_esconde_autor(self):
        """Retorna o valor da configuração esconde_autor."""
        record = 'brasil.gov.portal.controlpanel.portal.ISettingsPortal.' \
                 'esconde_autor'
        return api.portal.get_registry_record(record)

    def get_esconde_data(self):
        """Retorna o valor da configuração esconde_data."""
        record = 'brasil.gov.portal.controlpanel.portal.ISettingsPortal.' \
                 'esconde_data'
        return api.portal.get_registry_record(record)
