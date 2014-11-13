# -*- coding: utf-8 -*-

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import TitleViewlet as PloneTitleViewlet
from plone.memoize.view import memoize


class TitleViewlet(PloneTitleViewlet):
    """Customize Plone TitleViewlet
    """
    index = ViewPageTemplateFile('templates/title.pt')

    @property
    @memoize
    def page_title(self):
        '''
        Override default method to add the right page name (translated) for
        search and sitemap pages
        '''
        alternative_titles = {
            'busca': 'Busca',
            'mapadosite': 'Mapa do Site',
        }

        view_name = self.request.getURL()
        # get last item
        view_name = view_name.split('/')[-1]
        # take out browser view @@
        view_name = view_name.strip('@')
        # Take out get parameters
        view_name = view_name.split('?')[0]

        title = ''
        for k, v in alternative_titles.iteritems():
            if view_name == k:
                title = v
        if not(title):
            title = PloneTitleViewlet.page_title.fget(self)

        return title
