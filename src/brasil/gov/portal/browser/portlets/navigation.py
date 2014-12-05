# -*- coding: utf-8 -*-
from plone.app.portlets.portlets.navigation import Renderer as BaseRenderer
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class Renderer(BaseRenderer):

    def process_navigation(self, data):
        ''' '''
        portal_url = self.urltool()
        navroot_url = self.getNavRoot().absolute_url()
        for item in data:
            remoteUrl = item.get('getRemoteUrl', '')
            if '${portal_url}' in str(remoteUrl):
                item['getRemoteUrl'] = remoteUrl.replace('${portal_url}',
                                                         portal_url)
            elif '${portal_url}' in str(remoteUrl):
                item['getRemoteUrl'] = remoteUrl.replace(
                    '${navigation_root_url}', navroot_url)
        return data

    def createNavTree(self):
        data = self.getNavTree()

        bottomLevel = (self.data.bottomLevel or
                       self.properties.getProperty('bottomLevel', 0))
        if bottomLevel < 0:
            # Special case where navigation tree depth is negative
            # meaning that the admin does not want the listing to be displayed
            return self.recurse([], level=1, bottomLevel=bottomLevel)
        else:
            children = self.process_navigation(data.get('children', []))
            return self.recurse(children=children,
                                level=1,
                                bottomLevel=bottomLevel)

    recurse = ViewPageTemplateFile('templates/navigation_recurse.pt')
