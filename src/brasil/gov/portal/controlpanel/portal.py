# -*- coding: utf-8 -*-
"""View de configuração do Portal Padrão."""

from brasil.gov.portal import _
from plone.app.registry.browser import controlpanel
from plone.directives import form
from zope.schema import Bool


class ISettingsPortal(form.Schema):
    """Campos do formulário de configuração do Portal Padrão."""
    esconde_autor = Bool(
        title=_(u'Hides author'),
        description=_(u'Hide information about who created an item.'),
        default=False,
        required=False)

    esconde_data = Bool(
        title=_(u'Hides publication date'),
        description=_(
            u'Hide information about when an item has been published.'),
        default=False,
        required=False)


class PortalEditForm(controlpanel.RegistryEditForm):
    """Formulário de configuração do Portal Padrão."""
    schema = ISettingsPortal
    label = _(u'e-Government Digital Identity Settings')
    description = _(u'Settings for e-Government Digital Identity.')


class PortalControlPanel(controlpanel.ControlPanelFormWrapper):
    """Página de configuração do Portal Padrão"""
    form = PortalEditForm
