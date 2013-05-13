# -*- coding: utf-8 -*-
""" Modulo que implementa o viewlet de destaques do Portal """
from collective.cover.content import ICover
from five import grok
from plone.app.layout.viewlets.interfaces import IPortalHeader
from zope.component import getMultiAdapter
from zope.interface import Interface


FEATURES_ID = 'destaques'
grok.templatedir('templates')


class Destaques_Viewlet(grok.Viewlet):
    """Viewlet que lista destaques do site
    """

    grok.viewletmanager(IPortalHeader)
    grok.context(Interface)
    grok.order(100)

    def editable(self):
        ''' Validamos se o destaques eh editavel
        '''
        destaques = getattr(self.portal, FEATURES_ID, None)
        if destaques:
            context_state = getMultiAdapter((destaques, self.request),
                                            name=u'plone_context_state')
            return context_state.is_editable()

    def available(self):
        ''' Exibiremos ou nao este viewlet
        '''
        context = self.context
        portal_state = getMultiAdapter((context, self.request),
                                       name=u'plone_portal_state')
        self.portal = portal_state.portal()
        self.portal_url = portal_state.portal_url()
        self.destaques = getattr(self.portal, FEATURES_ID, None)
        if self.destaques:
            return ICover.providedBy(self.destaques)
        else:
            return False
