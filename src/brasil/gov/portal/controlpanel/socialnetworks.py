# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.interfaces import IPloneSiteRoot
from brasil.gov.portal import _ as _
from brasil.gov.portal.config import REDES
from plone.app.controlpanel.form import ControlPanelForm
from zope import schema
from zope.component import adapts
from zope.formlib.form import FormFields
from zope.formlib.objectwidget import ObjectWidget
from zope.formlib.sequencewidget import ListSequenceWidget
from zope.formlib.widget import CustomWidgetFactory
from zope.interface import Interface
from zope.interface import implements
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


networks = SimpleVocabulary(
    [SimpleTerm(value=rede['id'], title=_(rede['title']))
     for rede in REDES]
)


class ISocialNetworksPair(Interface):
    site = schema.Choice(title=_(u'Site'),
                         description=_(
                             _(u'help_social_network'),
                             default=u'Escolha a rede a ser cadastrada'),
                         required=True,
                         vocabulary=networks)

    info = schema.TextLine(title=u'Identificador')


class SocialNetworksPair:
    implements(ISocialNetworksPair)

    def __init__(self, site='', info=''):
        self.site = site
        self.info = info


class ISocialNetworksSchema(Interface):

    accounts_info = schema.List(
        title=_(u'Social Network'),
        default=[],
        value_type=schema.Object(ISocialNetworksPair, title=u'Rede'),
        required=False)


sn_widget = CustomWidgetFactory(ObjectWidget,
                                SocialNetworksPair)
accounts_widget = CustomWidgetFactory(ListSequenceWidget,
                                      subwidget=sn_widget)


class SocialNetworksPanelAdapter(SchemaAdapterBase):
    ''' Adapter para a raiz do site Plone suportar o schema
        de configuracao da barra de identidade
        Esta classe implementa uma maneira da raiz do site armazenar
        as configuracoes que serao geridas pelo painel de controle
    '''

    adapts(IPloneSiteRoot)
    implements(ISocialNetworksSchema)

    def __init__(self, context):
        super(SocialNetworksPanelAdapter, self).__init__(context)
        # Obtem a tool portal_properties
        self.pp = getToolByName(context, 'portal_properties')
        # Define que o contexto a ser utilizado para o schema IBarraConfSchema
        # sera a property sheet brasil_gov
        self.context = getattr(self.pp, 'brasil_gov', None)

    @apply
    def accounts_info():
        def get(self):
            accounts = []
            configs = self.context
            if configs:
                data = configs.getProperty('social_networks', [])
                for item in data:
                    k, v = item.split('|')
                    accounts.append(SocialNetworksPair(k, v))
                return accounts

        def set(self, value):
            accounts = []
            configs = self.context
            if configs:
                for ta in value:
                    if not ta.site:
                        continue
                    accounts.append('%s|%s' % (ta.site, ta.info))
                configs.manage_changeProperties(social_networks=accounts)
        return property(get, set)


class SocialNetworksControlPanel(ControlPanelForm):
    ''' Implementacao do painel de controle da Barra de Identidade '''
    # Define quais serao os campos a serem exibidos (IBarraConfSchema)
    form_fields = FormFields(ISocialNetworksSchema)
    form_fields['accounts_info'].custom_widget = accounts_widget

    # Define o titulo deste painel de controle
    label = _(u'.gov.br: Social Network')
    # Define a descricao deste painel de controle
    description = _(u'Identity Bar behavior Configuration')
    # Define o titulo do formulario deste painel de controle
    form_name = _(u'Visual and functional Configuration')
