# -*- coding: utf-8 -*-

from brasil.gov.portal.config import DEPS
from brasil.gov.portal.config import PROJECTNAME
from brasil.gov.portal.testing import INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.browserlayer.utils import registered_layers
from Products.GenericSetup.upgrade import listUpgradeSteps

import unittest

PROFILE_ID = 'brasil.gov.portal:default'

DEPENDENCIES = [
    'brasil.gov.agenda',
    'brasil.gov.barra',
    'brasil.gov.tiles',
    'brasil.gov.vcge',
    'collective.cover',
    'collective.js.jqueryui',
    'collective.nitf',
    'collective.polls',
    'collective.upload',
    'plone.app.contenttypes',
    'plone.app.theming',
    'Products.Doormat',
    'Products.PloneFormGen',
    'sc.embedder',
    'sc.social.like',
]


class InstallTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']
        self.st = self.portal['portal_setup']

    def test_browser_layer(self):
        layers = [l.getName() for l in registered_layers()]
        self.assertTrue('IBrasilGov' in layers,
                        'add-on layer was not installed')

    def test_gs_version(self):
        setup = self.st
        self.assertEqual(setup.getLastVersionForProfile(PROFILE_ID),
                         (u'5000',),
                         '%s version mismatch' % PROJECTNAME)

    def test_hidden_dependencies(self):
        packages = [p['id'] for p in self.qi.listInstallableProducts()]
        deps = set(DEPS)
        result = [p for p in deps if p in packages]
        self.assertFalse(result,
                         ("Estas dependencias nao estao ocultas: %s" %
                          ", ".join(result)))

    def test_installed(self):
        self.assertTrue(self.qi.isProductInstalled(PROJECTNAME),
                        '%s nao esta instalado' % PROJECTNAME)

    def test_installed_dependencies(self):
        expected = set(DEPENDENCIES)
        result = []
        for item in expected:
            profile_id = self.qi.getInstallProfile(item)['id']
            if self.st.getLastVersionForProfile(profile_id) == 'unknown':
                result.append(item)
        self.assertFalse(result,
                         ("Estas dependencias nao estao instaladas: %s" %
                          ", ".join(result)))


class TestUpgrade(unittest.TestCase):
    """Ensure product upgrades works."""

    layer = INTEGRATION_TESTING

    profile = 'brasil.gov.portal:default'

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']
        self.st = self.portal['portal_setup']
        self.pp = self.portal['portal_properties']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def list_upgrades(self, source, destination):
        upgradeSteps = listUpgradeSteps(self.st,
                                        self.profile,
                                        source)
        if source == '0':
            source = (source, '0')
        else:
            source = (source, )

        step = [step for step in upgradeSteps
                if (step[0]['dest'] == (destination,))
                and (step[0]['source'] == source)]
        return step

    def execute_upgrade(self, source, destination):
        # Setamos o profile para versao source
        self.st.setLastVersionForProfile(self.profile, source)
        # Pegamos os upgrade steps
        upgradeSteps = listUpgradeSteps(self.st,
                                        self.profile,
                                        source)
        if source == '0':
            source = (source, '0')
        else:
            source = (source, )
        steps = [step for step in upgradeSteps
                 if (step[0]['dest'] == (destination,))
                 and (step[0]['source'] == source)][0]
        # Os executamos
        for step in steps:
            step['step'].doStep(self.st)

    def test_to1000_available(self):
        step = self.list_upgrades(u'0', u'1000')
        self.assertEqual(len(step), 1)

    def test_to1000_execution(self):
        # Executa upgrade
        self.execute_upgrade(u'0', u'1000')

    def test_to2000_available(self):
        step = self.list_upgrades(u'1000', u'2000')
        self.assertEqual(len(step), 1)

    def test_to2000_execution(self):
        # Executa upgrade
        self.execute_upgrade(u'1000', u'2000')
        record = api.portal.get_registry_record(
            'collective.cover.controlpanel.ICoverSettings.available_tiles'
        )
        self.assertIn(
            'banner_rotativo',
            record
        )

    def test_to3000_available(self):
        step = self.list_upgrades(u'2000', u'3000')
        self.assertEqual(len(step), 1)

    def test_to3000_execution(self):
        # Executa upgrade
        self.execute_upgrade(u'2000', u'3000')
        record = api.portal.get_registry_record(
            'collective.cover.controlpanel.ICoverSettings.styles'
        )
        self.assertIn(
            'Verde Esporte|verde',
            record
        )

    def test_to4000_available(self):
        step = self.list_upgrades(u'3000', u'4000')
        self.assertEqual(len(step), 1)

    def test_to4000_execution(self):
        # Executa upgrade
        self.execute_upgrade(u'3000', u'4000')
        self.assertTrue(
            self.pp.site_properties.displayPublicationDateInByline
        )

    def test_to5000_available(self):
        step = self.list_upgrades(u'4000', u'5000')
        self.assertEqual(len(step), 1)

    def test_5000_corrige_pastas(self):
        # Ajustamos as pastas para nao estarem ordenadas
        pastas = ['assuntos', 'imagens', ]
        for pasta_id in pastas:
            pasta = api.content.create(
                type='Folder',
                container=self.portal,
                id=pasta_id
            )
            pasta.setOrdering('unordered')
            conteudo = api.content.create(
                type='Folder',
                container=pasta,
                id='sub_{0}'.format(pasta_id)
            )
            conteudo.setOrdering('unordered')

        # Executa upgrade
        self.execute_upgrade(u'4000', u'5000')

        for pasta_id in pastas:
            pasta = self.portal[pasta_id]
            ordering = pasta.getOrdering()
            self.assertTrue(hasattr(ordering, 'ORDER_KEY'))

    def test_to10300_available(self):
        step = self.list_upgrades(u'5000', u'10300')
        self.assertEqual(len(step), 1)

    def test_to10300_execution(self):
        controlpanel = api.portal.get_tool('portal_controlpanel')
        # Executa upgrade
        self.execute_upgrade(u'5000', u'10300')
        # Ao acessar a view como site administrator conseguimos acesso
        with api.env.adopt_roles(['Site Administrator', ]):
            # Listamos todas as acoes do painel de controle
            installed = [a['id'] for a in controlpanel.enumConfiglets(group='Products')]
            # Validamos que o painel de controle da barra esteja instalado
            self.failUnless('social-config' in installed)
        # Ao acessar a view como anonimo, a excecao e levantada
        with api.env.adopt_roles(['Anonymous', ]):
            # Listamos todas as acoes do painel de controle
            installed = [a['id'] for a in controlpanel.enumConfiglets(group='Products')]
            # Validamos que o painel de controle da barra esteja instalado
            self.failIf('social-config' in installed)
