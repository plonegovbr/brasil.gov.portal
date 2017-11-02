# -*- coding: utf-8 -*-
from plone import api
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class ExternalContentView(BrowserView):
    """Redireciona usuarios sem poder de edicao para o conteudo externo."""

    index = ViewPageTemplateFile('templates/externalcontentview.pt')

    def setup(self):
        mtool = api.portal.get_tool('portal_membership')
        self.can_edit = mtool.checkPermission('Modify portal content', self.context)

    def render(self):
        return self.index()

    def __call__(self):
        self.setup()

        if self.can_edit:
            return self.render()
        else:
            self.request.RESPONSE.redirect(self.context.remoteUrl)
