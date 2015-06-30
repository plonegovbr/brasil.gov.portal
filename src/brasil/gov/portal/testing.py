# -*- coding: utf-8 -*-
from collective.transmogrifier.transmogrifier import configuration_registry
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Instala produtos
        z2.installProduct(app, 'Products.Doormat')
        z2.installProduct(app, 'Products.PloneFormGen')
        # Load ZCML
        import brasil.gov.portal
        self.loadZCML(package=brasil.gov.portal)

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        self.applyProfile(portal, 'brasil.gov.portal:default')
        portal.portal_workflow.setDefaultChain('simple_publication_workflow')

    def tearDown(self):
        super(Fixture, self).tearDown()
        configuration_registry.clear()

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
