# -*- coding: utf-8 -*-
""" Modulo que implementa o viewlet de conteudo relacionados do Portal """
from Acquisition import aq_inner
from Products.CMFPlone.utils import base_hasattr
from five import grok
from plone.app.layout.viewlets.interfaces import IBelowContentBody
from plone.app.relationfield.behavior import IRelatedItems
from plone.dexterity.interfaces import IDexterityContent


grok.templatedir('templates')


class RelatedItemsViewlet(grok.Viewlet):
    """Viewlet de itens relacionados para Dexterity
    """

    grok.viewletmanager(IBelowContentBody)
    grok.context(IDexterityContent)
    grok.order(100)

    def related(self):
        context = aq_inner(self.context)
        res = ()
        if base_hasattr(context, 'relatedItems'):
            related = context.relatedItems
        else:
            try:
                behavior = IRelatedItems(context)
                related = behavior.relatedItems
            except TypeError:
                return res
        tools = context.restrictedTraverse('@@plone_tools')
        catalog = tools.catalog()
        if related:
            related = [item.to_path for item in related if item.to_path]
            brains = catalog(path=related)
            if brains:
                # build a position dict by iterating over the items once
                positions = dict([(v, i) for (i, v) in enumerate(related)])
                # We need to keep the ordering intact
                res = list(brains)

                def _key(brain):
                    return positions.get(brain.UID, -1)
                res.sort(key=_key)
        return res
