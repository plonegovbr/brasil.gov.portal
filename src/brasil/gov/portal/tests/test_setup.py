# -*- coding: utf-8 -*-
from brasil.gov.portal.config import DEPS
from brasil.gov.portal.config import HIDDEN_PROFILES
from brasil.gov.portal.config import PROJECTNAME
from brasil.gov.portal.config import SHOW_DEPS
from brasil.gov.portal.config import TINYMCE_JSON_FORMATS
from brasil.gov.portal.testing import INTEGRATION_TESTING
from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.folder.default import DefaultOrdering
from plone.browserlayer.utils import registered_layers
from Products.Five.browser import BrowserView as View
from Products.GenericSetup.upgrade import listUpgradeSteps
from Products.TinyMCE.interfaces.utility import ITinyMCE
from zope.component import getUtility
from zope.component import queryMultiAdapter
from zope.viewlet.interfaces import IViewletManager

import json
import unittest

PROFILE_ID = 'brasil.gov.portal:default'

DEPENDENCIES = [
    'brasil.gov.agenda',
    'brasil.gov.barra',
    'brasil.gov.portlets',
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

    def test_hidden_dependencies(self):
        packages = [p['id'] for p in self.qi.listInstallableProducts()]
        deps = set(DEPS)
        result = [p for p in deps if p in packages]
        self.assertFalse(result,
                         ('Estas dependencias nao estao ocultas: %s' %
                          ', '.join(result)))

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
                         ('Estas dependencias nao estao instaladas: %s' %
                          ', '.join(result)))


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
            source = (source,)

        step = [step for step in upgradeSteps
                if (step[0]['dest'] == (destination,)) and
                (step[0]['source'] == source)]
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
            source = (source,)
        steps = [step for step in upgradeSteps
                 if (step[0]['dest'] == (destination,)) and
                 (step[0]['source'] == source)][0]
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

    def _prepara_to10300(self):
        # Cria conteudo NITF
        noticia = api.content.create(
            type='collective.nitf.content',
            container=self.portal,
            id='uma-noticia',
            title=u'Uma notícia'
        )
        noticia.section = 'General'
        noticia.reindexObject(idxs=['section', ])
        # Deixa General como secao disponivel
        api.portal.set_registry_record(
            'collective.nitf.controlpanel.INITFSettings.available_sections',
            set([u'General', ])
        )
        # Deixa General como padrao
        api.portal.set_registry_record(
            'collective.nitf.controlpanel.INITFSettings.default_section',
            u'General'
        )

    def test_to10300_execution(self):
        self._prepara_to10300()
        controlpanel = api.portal.get_tool('portal_controlpanel')
        # Executa upgrade
        self.execute_upgrade(u'5000', u'10300')
        # Ao acessar a view como site administrator conseguimos acesso
        with api.env.adopt_roles(['Site Administrator', ]):
            # Listamos todas as acoes do painel de controle
            installed = [a['id'] for a in controlpanel.enumConfiglets(group='Products')]  # NOQA
            # Validamos que o painel de controle da barra esteja instalado
            self.assertTrue('social-config' in installed)
        # Ao acessar a view como anonimo, a excecao e levantada
        with api.env.adopt_roles(['Anonymous', ]):
            # Listamos todas as acoes do painel de controle
            installed = [a['id'] for a in controlpanel.enumConfiglets(group='Products')]  # NOQA
            # Validamos que o painel de controle da barra esteja instalado
            self.assertFalse('social-config' in installed)

        # Testamos se os pacotes estao instalados e disponiveis
        qi = api.portal.get_tool('portal_quickinstaller')
        installed = [p.get('id') for p in qi.listInstalledProducts()]
        for p in SHOW_DEPS:
            self.assertIn(p, qi)
            self.assertIn(p, installed)

        # Validamos secoes disponiveis
        available_sections = api.portal.get_registry_record(
            'collective.nitf.controlpanel.INITFSettings.available_sections',
        )
        self.assertNotIn('General', available_sections)
        self.assertIn(u'Notícias', available_sections)
        # Validamos secao default
        default_section = api.portal.get_registry_record(
            'collective.nitf.controlpanel.INITFSettings.default_section',
        )
        self.assertNotEqual('General', default_section)
        self.assertEqual(u'Notícias', default_section)
        # A substituicao deve ter sido feita
        ct = api.portal.get_tool('portal_catalog')
        results = ct.searchResults(section=u'Notícias')
        self.assertEqual(len(results), 1)

    def test_to10400_available(self):
        step = self.list_upgrades(u'10300', u'10400')
        self.assertEqual(len(step), 1)

    def test_to10400_execution(self):
        self.execute_upgrade(u'10300', u'10400')
        portal_css = api.portal.get_tool('portal_css')
        stylesheets_ids = portal_css.getResourceIds()
        resource_id = '++resource++brasil.gov.portal/css/main-print.css'
        self.assertTrue(resource_id in stylesheets_ids)
        self.assertTrue(portal_css.getResource(resource_id).getEnabled())

    def test_to10500_available(self):
        step = self.list_upgrades(u'10400', u'10500')
        self.assertEqual(len(step), 1)

    def test_to10500_execution(self):
        self.execute_upgrade(u'10400', u'10500')

    def test_to10600_available(self):
        step = self.list_upgrades(u'10500', u'10600')
        self.assertEqual(len(step), 1)

    def test_to10700_available(self):
        step = self.list_upgrades(u'10600', u'10700')
        self.assertEqual(len(step), 1)

    def _get_viewlets_from_manager(self, manager):
        """Returns all viewlets from a manager."""
        request = self.portal.REQUEST
        view = View(self.portal, request)
        manager = queryMultiAdapter(
            (self.portal, request, view),
            IViewletManager,
            manager,
            default=None
        )

        self.assertIsNotNone(manager)

        manager.update()

        return manager.viewlets

    def _get_available_viewlets_ids_from_manager(self, new_ids, from_manager):
        return [v for v in from_manager if v.__name__ in new_ids]

    def test_to10600_execution(self):
        # A action de Configuracoes do Site deve estar visivel para os testes
        pa = self.portal['portal_actions']
        if not pa['site_actions'].plone_setup.visible:
            pa['site_actions'].plone_setup.visible = True
        self.assertTrue(pa['site_actions'].plone_setup.visible)

        self.execute_upgrade(u'10500', u'10600')

        formats = json.loads(getUtility(ITinyMCE).formats)
        # Todas as chaves dos formatos precisam estar presentes na tool após
        # a execução do upgradeStep.
        all_formats = all(key in formats for key in TINYMCE_JSON_FORMATS)
        self.assertTrue(all_formats)

        # Check if the new viewlets are registered.
        new_viewlets_top = [u'brasil.gov.portal.acessibilidade']
        top_available = self._get_available_viewlets_ids_from_manager(
            new_viewlets_top,
            self._get_viewlets_from_manager('plone.portaltop')
        )
        self.assertEqual(len(top_available), len(new_viewlets_top))

        new_viewlets_footer = [u'plone.footer', u'brasil.gov.portal.topo']
        footer_available = self._get_available_viewlets_ids_from_manager(
            new_viewlets_footer,
            self._get_viewlets_from_manager('plone.portalfooter')
        )
        self.assertEqual(len(footer_available), len(new_viewlets_footer))
        configs = getattr(self.pp, 'brasil_gov', None)
        url_orgao = configs.getProperty('url_orgao')
        self.assertEqual(
            url_orgao,
            u'http://estruturaorganizacional.dados.gov.br/doc/' +
            'unidade-organizacional/26'
        )

        # A action de Configuracoes do Site deve ser desabilitada pelo
        # upgrade step.
        self.assertFalse(pa['site_actions'].plone_setup.visible)

    def test_to10700_execution(self):
        # Testa a ordenação das pastas na raiz: Preciso criar diretórios
        # antes de executar o upgradeStep, sem ordenação, para testar de
        # forma correta a ordenação em todos efetuada pelo upgradeStep.
        # Ajustamos as pastas para nao estarem ordenadas
        pastas = ['teste1', 'teste2', 'teste3', 'teste4', 'teste5']
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

        for pasta_id in pastas:
            pasta = self.portal[pasta_id]
            self.assertFalse(isinstance(pasta.getOrdering(), DefaultOrdering))

        self.st.setLastVersionForProfile('brasil.gov.tiles:default', '2000')
        self.assertEqual(
            len(self.st.listUpgrades('brasil.gov.tiles:default')),
            1
        )

        self.execute_upgrade(u'10600', u'10700')

        for pasta_id in pastas:
            pasta = self.portal[pasta_id]
            self.assertTrue(isinstance(pasta.getOrdering(), DefaultOrdering))

        self.assertEqual(
            len(self.st.listUpgrades('brasil.gov.tiles:default')),
            0
        )

    def test_upgrade_step_variavel_hidden_profiles_deps_brasil_gov_portal(self):  # NOQA
        """
        Testa se todos os upgradeSteps de brasil.gov.portal estão nas variáveis
        HIDDEN_PROFILES e DEPS. Outros pacotes podem ser adicionados em outros
        testes.
        """
        upgradeSteps = listUpgradeSteps(self.st, self.profile, '')
        upgrades = [upgrade[0]['dest'][0] for upgrade in upgradeSteps]

        upgrades_hidden_profiles = []
        upgrades_deps = []
        prefix = 'brasil.gov.portal.upgrades.v%s'
        profile = self.profile.split(':')[-1]
        for upgrade in upgrades:
            upgrades_deps.append(prefix % upgrade)
            upgrades_hidden_profiles.append(prefix % upgrade + ':' + profile)

        self.assertTrue(all(upgrade in HIDDEN_PROFILES
                            for upgrade in upgrades_hidden_profiles))

        self.assertTrue(all(upgrade in DEPS
                            for upgrade in upgrades_deps))

    def test_ultimo_upgrade_igual_metadata_xml_filesystem(self):
        """
        Testa se o número do último upgradeStep disponível é o mesmo do
        metadata.xml do profile.

        É também útil para garantir que para toda alteração feita no version
        do metadata.xml tenha um upgradeStep associado.

        Esse teste parte da premissa que o número dos upgradeSteps é sempre
        sequencial.
        """
        upgrade_info = self.qi.upgradeInfo(PROJECTNAME)
        upgradeSteps = listUpgradeSteps(self.st, self.profile, '')
        upgrades = [upgrade[0]['dest'][0] for upgrade in upgradeSteps]
        last_upgrade = sorted(upgrades, key=int)[-1]
        self.assertEqual(upgrade_info['installedVersion'],
                         last_upgrade)
