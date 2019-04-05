# -*- coding: utf-8 -*-
""" Modulo que implementa o viewlet de servicos do Portal"""

from plone.app.layout.viewlets import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getMultiAdapter


class ServicosViewlet(ViewletBase):
    """ Viewlet de listagem de servicos
    """
    # Indica qual o template sera usado por este viewlet
    index = ViewPageTemplateFile('templates/servicos.pt')

    def update(self):
        """ Prepara/Atualiza os valores utilizados pelo Viewlet
        """
        super(ServicosViewlet, self).update()
        ps = getMultiAdapter(
            (self.context, self.request),
            name='plone_portal_state',
        )
        tools = getMultiAdapter(
            (self.context, self.request),
            name='plone_tools',
        )
        self.remote_url_utils = getMultiAdapter(
            (self.context, self.request),
            name='remote_url_utils',
        )
        portal = ps.portal()
        self._folder = 'servicos' in portal.objectIds() and portal['servicos']
        self._ct = tools.catalog()

    def available(self):
        return self._folder and True or False

    def servicos(self):
        folder_path = '/'.join(self._folder.getPhysicalPath())
        query = {
            'portal_type': ['Link'],
            'path': folder_path,
            'sort_on': 'getObjPositionInParent',
        }
        return [
            {
                'getId': l.getId,
                'Title': l.Title,
                'Description': l.Description,
                'getRemoteUrl': self.remote_url_utils.remote_url_transform(
                    l.getPath(),
                    l.getRemoteUrl,
                ),
            }
            for l in self._ct(query)
        ]
