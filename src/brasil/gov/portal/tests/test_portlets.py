from brasil.gov.portal.browser.portlets import navigation
from brasil.gov.portal.testing import INTEGRATION_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletRenderer
from zope.component import getMultiAdapter
from zope.component import getUtility

import unittest


class NavigationTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.populateSite()

    def renderer(self,
                 context=None,
                 request=None,
                 view=None,
                 manager=None,
                 assignment=None):
        context = context or self.portal
        request = request or self.app.REQUEST
        view = view or self.portal.restrictedTraverse('@@plone')
        manager = manager or getUtility(IPortletManager,
                                        name='plone.leftcolumn',
                                        context=self.portal)
        assignment = assignment or navigation.Assignment(topLevel=0)

        return getMultiAdapter((context,
                                request,
                                view,
                                manager,
                                assignment),
                               IPortletRenderer)

    def populateSite(self):
        self.setRoles(['Manager'])
        if 'Members' in self.portal:
            self.portal._delObject('Members')
            self.folder = None
        if 'news' in self.portal:
            self.portal._delObject('news')
        if 'events' in self.portal:
            self.portal._delObject('events')
        if 'front-page' in self.portal:
            self.portal._delObject('front-page')
        self.portal.invokeFactory('Document', 'doc1')
        self.portal.invokeFactory('Document', 'doc2')
        self.portal.invokeFactory('Document', 'doc3')
        self.portal.invokeFactory('Folder', 'folder1')
        self.portal.invokeFactory('Link', 'link1')
        self.portal.link1.setRemoteUrl('http://plone.org')
        self.portal.link1.reindexObject()
        folder1 = getattr(self.portal, 'folder1')
        folder1.invokeFactory('Document', 'doc11')
        folder1.invokeFactory('Document', 'doc12')
        folder1.invokeFactory('Document', 'doc13')
        self.portal.invokeFactory('Folder', 'folder2')
        folder2 = getattr(self.portal, 'folder2')
        folder2.invokeFactory('Document', 'doc21')
        folder2.invokeFactory('Document', 'doc22')
        folder2.invokeFactory('Document', 'doc23')
        folder2.invokeFactory('File', 'file21')
        self.setRoles(['Member'])

    def testRootItensOrder(self):
        viewRoot = self.renderer(self.portal)
        treeRoot = viewRoot.getNavTree()
        self.failUnless(treeRoot)

        viewChildren = self.renderer(self.portal.folder2)
        treeChildren = viewChildren.getNavTree()
        self.failUnless(treeChildren)

        treeRootUIDs = [i['UID'] for i in treeRoot['children']]
        treeChildrenUIDs = [i['UID'] for i in treeChildren['children']]
        self.assertEqual(treeRootUIDs, treeChildrenUIDs)
