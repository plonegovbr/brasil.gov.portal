# -*- coding: utf-8 -*-
"""Interfaces de views"""

from zope.interface import Interface


class IPortalSettingsView(Interface):
    """Marker interface"""

    def get_esconde_autor():
        """Retorna o valor da configuração esconde_autor."""

    def get_esconde_data():
        """Retorna o valor da configuração esconde_data."""
