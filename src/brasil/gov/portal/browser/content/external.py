# -*- coding: utf-8 -*-
from brasil.gov.portal.content.external import IExternalContent
from five import grok
from plone import api

grok.templatedir('templates')


class ExternalContentView(grok.View):
    grok.context(IExternalContent)
    grok.name('view')

    def update(self):
        """Redireciona usuarios sem poder de edicao para o conteudo externo"""
        context = self.context
        mtool = api.portal.get_tool('portal_membership')

        can_edit = mtool.checkPermission('Modify portal content', context)

        if not can_edit:
            url = context.remoteUrl
            return context.REQUEST.RESPONSE.redirect(url)
