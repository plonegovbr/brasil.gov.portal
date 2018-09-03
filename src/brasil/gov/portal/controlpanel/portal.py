# -*- coding: utf-8 -*-
"""Configuration configlet for IDG.

It currently includes privacy and header options.

In the future this configlet should list all IDG options if possible to
avoid having too many configlets.
"""
from brasil.gov.portal import _
from brasil.gov.portal.utils import validate_list_of_links
from plone.app.registry.browser import controlpanel
from plone.autoform import directives as form
from plone.formwidget.namedfile.widget import NamedImageFieldWidget
from plone.supermodel import model
from zope import schema


class ISettingsPortal(model.Schema):
    """Campos do formulário de configuração do Portal Padrão."""

    # TODO: do we still need esconde_autor and esconde_data fields?
    esconde_autor = schema.Bool(
        title=_(u'Hides author'),
        description=_(u'Hide information about who created an item.'),
        default=False,
        required=False)

    esconde_data = schema.Bool(
        title=_(u'Hides publication date'),
        description=_(
            u'Hide information about when an item has been published.'),
        default=False,
        required=False)

    model.fieldset(
        'header',
        label=u'Header',
        fields=[
            'expandable_header',
            'background_image',
            'featured_news',
            'more_news',
            'featured_services',
            'more_services',
            'top_subjects',
        ],
    )

    expandable_header = schema.Bool(
        title=_(u'Use expandable header?'),
        description=_(
            u'help_expandable_header',
            default=u'If enabled, an expandable header will be used instead of the default. '  # noqa: E501
                    u'A list of search sugestions and hot topics will also be shown, if available.'),  # noqa: E501
        default=False,
    )

    form.widget('background_image', NamedImageFieldWidget)
    background_image = schema.ASCII(
        title=_(u'title_background_image', default=u'Background image'),
        description=_(
            u'help_background_image',
            default=u'This image will be used as background of the header. '
                    u'Should be 1440px width and 605px height.',
        ),
        required=False,
    )

    form.widget('featured_news', cols=25, rows=10)
    featured_news = schema.Tuple(
        title=_(u'Notícias em destaque'),
        description=_(
            u'help_featured_news',
            default=_(u'You must use "Title|http://example.org" format to fill each line.')),  # noqa: E501
        required=False,
        default=(),
        value_type=schema.TextLine(),
        constraint=validate_list_of_links,
    )

    more_news = schema.URI(
        title=_(u'Mais notícias'),
        required=False,
    )

    form.widget('featured_services', cols=25, rows=10)
    featured_services = schema.Tuple(
        title=_(u'Serviços em destaque'),
        description=_(
            u'help_featured_services',
            default=_(u'You must use "Title|http://example.org" format to fill each line.')),  # noqa: E501
        required=False,
        default=(),
        value_type=schema.TextLine(),
        constraint=validate_list_of_links,
    )

    more_services = schema.URI(
        title=_(u'Mais serviços'),
        required=False,
    )

    form.widget('top_subjects', cols=25, rows=10)
    top_subjects = schema.Tuple(
        title=_(u'Assuntos em alta'),
        description=_(
            u'help_top_subjects',
            default=_(u'You must use "Title|http://example.org" format to fill each line.')),  # noqa: E501
        required=False,
        default=(),
        value_type=schema.TextLine(),
        constraint=validate_list_of_links,
    )


class PortalEditForm(controlpanel.RegistryEditForm):
    """Formulário de configuração do Portal Padrão."""
    schema = ISettingsPortal
    label = _(u'e-Government Digital Identity Settings')
    description = _(u'Settings for e-Government Digital Identity.')


class PortalControlPanel(controlpanel.ControlPanelFormWrapper):
    """Página de configuração do Portal Padrão"""
    form = PortalEditForm
