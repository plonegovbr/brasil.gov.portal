# -*- coding:utf-8 -*-
from Acquisition import aq_inner
from plone.app.layout.navigation.interfaces import INavigationQueryBuilder
from plone.app.layout.navigation.interfaces import INavtreeStrategy
from plone.app.layout.navigation.navtree import buildFolderTree as buildFolderTreeBase
from plone.app.layout.navigation.navtree import NavtreeStrategyBase
from plone.app.portlets.portlets.navigation import Renderer as BaseRenderer
from plone.memoize.instance import memoize
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getMultiAdapter
from zope.component.hooks import getSite


def buildFolderTree(context, obj=None, query={}, strategy=NavtreeStrategyBase()):
    """The navtree option is not getting the parents folder order respecting
       the folder order, so when we open the tree, the parent items order change.
       This is a quick fix of the order, but we should review the way navtree
       query option works, and if it is applicable to keep the same worder globally.
    """
    tree = buildFolderTreeBase(context, obj, query, strategy)
    # fix tree order
    if ('navtree' in query['path']):
        treeChildren = tree.copy()
        queryRoot = query
        del(queryRoot['path']['navtree'])
        queryRoot['path']['depth'] = 1
        portal = getSite()
        queryRoot['path']['query'] = (
            '/'.join(portal.getPhysicalPath()) +
            treeChildren['getURL'][len(portal.absolute_url()):]
        )
        treeRoot = buildFolderTreeBase(context, obj, queryRoot, strategy)
        tree['children'] = treeRoot['children']
        for i, child in enumerate(treeRoot['children']):
            for childOrig in treeChildren['children']:
                if (childOrig['UID'] == child['UID']):
                    tree['children'][i]['children'] = childOrig['children']
                    break
    # fix tree order
    return tree


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

    @memoize
    def getNavTree(self, _marker=None):
        """This method is the same as it's parent. I just took it here
           to redefine the scope of the call of buildFolderTree function
           with the tree order fix
        """
        if _marker is None:
            _marker = []
        context = aq_inner(self.context)
        queryBuilder = getMultiAdapter((context, self.data), INavigationQueryBuilder)
        strategy = getMultiAdapter((context, self.data), INavtreeStrategy)
        return buildFolderTree(context, obj=context, query=queryBuilder(), strategy=strategy)

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
