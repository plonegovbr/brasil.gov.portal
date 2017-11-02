# -*- coding: utf-8 -*-
from collective.transmogrifier.transmogrifier import configuration_registry
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import os
import shutil
import tempfile


# FIXME: workaround for https://github.com/plone/plone.app.testing/issues/39
autoform = ('plone.autoform', {'loadZCML': True})
tinymce = ('Products.TinyMCE', {'loadZCML': True})
products = list(PLONE_FIXTURE.products)
products.insert(products.index(tinymce), autoform)
PLONE_FIXTURE.products = tuple(products)


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUp(self):
        """Copy all files used in tests to the temporary directory."""
        super(Fixture, self).setUp()
        tempdir = tempfile.gettempdir()
        path = os.path.join(os.path.dirname(__file__), 'tests', 'files')
        for i in os.listdir(path):
            shutil.copy(os.path.join(path, i), tempdir)

    def setUpZope(self, app, configurationContext):
        # Instala produtos
        z2.installProduct(app, 'Products.Doormat')
        z2.installProduct(app, 'Products.PloneFormGen')
        # Load ZCML
        import brasil.gov.portal
        self.loadZCML(package=brasil.gov.portal)
        # Install products that use an old-style initialize() function
        # https://github.com/plone/plone.app.event/issues/81#issuecomment-23930996
        z2.installProduct(app, 'Products.DateRecurringIndex')

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        self.applyProfile(portal, 'brasil.gov.portal:default')
        portal.portal_workflow.setDefaultChain('simple_publication_workflow')

    def tearDown(self):
        super(Fixture, self).tearDown()
        configuration_registry.clear()

    def tearDownZope(self, app):
        # Uninstall products installed above
        # https://github.com/plone/plone.app.event/issues/81#issuecomment-23930996
        z2.uninstallProduct(app, 'Products.DateRecurringIndex')


FIXTURE = Fixture()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name='brasil.gov.portal:Integration',
)
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,),
    name='brasil.gov.portal:Functional',
)


class InitContentFixture(Fixture):

    def setUpPloneSite(self, portal):
        super(InitContentFixture, self).setUpPloneSite(portal)
        self.applyProfile(portal, 'brasil.gov.portal:initcontent')
        portal.title = 'Portal Brasil'
        portal.description = u'Secretaria de Comunicação Social'
        wf = portal.portal_workflow
        wf.setDefaultChain('simple_publication_workflow')
        types = ('Document', 'Folder', 'Link', 'Topic', 'News Item')
        wf.setChainForPortalTypes(types, '(Default)')


INITCONTENT_FIXTURE = InitContentFixture()

INITCONTENT_TESTING = IntegrationTesting(
    bases=(INITCONTENT_FIXTURE,),
    name='brasil.gov.portal:InitContent',
)


class AcceptanceFixture(Fixture):

    def setUpPloneSite(self, portal):
        super(AcceptanceFixture, self).setUpPloneSite(portal)
        self.applyProfile(portal, 'brasil.gov.portal:initcontent')
        portal.title = 'Portal Brasil'
        portal.description = u'Secretaria de Comunicação Social'


ACCEPTANCE_FIXTURE = AcceptanceFixture()

ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(AUTOLOGIN_LIBRARY_FIXTURE,
           ACCEPTANCE_FIXTURE,
           z2.ZSERVER_FIXTURE),
    name='brasil.gov.portal:Acceptance',
)
