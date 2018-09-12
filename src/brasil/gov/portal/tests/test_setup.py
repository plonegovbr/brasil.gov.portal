# -*- coding: utf-8 -*-
from brasil.gov.agenda.config import PROJECTNAME as AGENDAPROJECTNAME
from brasil.gov.portal.config import DEPS
from brasil.gov.portal.config import HIDDEN_PROFILES
from brasil.gov.portal.config import PROJECTNAME
from brasil.gov.portal.config import SHOW_DEPS
from brasil.gov.portal.config import TINYMCE_JSON_FORMATS
from brasil.gov.portal.controlpanel.portal import ISettingsPortal
from brasil.gov.portal.setuphandlers import _instala_pacote
from brasil.gov.portal.testing import INTEGRATION_TESTING
from brasil.gov.portal.tests.test_portal_properties import SELECTABLE_VIEWS
from brasil.gov.portal.upgrades.v10700.handler import atualiza_produtos_terceiros
from collective.cover.controlpanel import ICoverSettings
from distutils.version import LooseVersion
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.browserlayer.utils import registered_layers
from plone.folder.default import DefaultOrdering
from plone.registry.interfaces import IRegistry
from Products.Five.browser import BrowserView as View
from Products.GenericSetup.tool import UNKNOWN
from Products.GenericSetup.upgrade import listUpgradeSteps
from Products.TinyMCE.interfaces.utility import ITinyMCE
from zope.component import getUtility
from zope.component import queryMultiAdapter
from zope.viewlet.interfaces import IViewletManager

import json
import unittest


PROFILE_ID = 'brasil.gov.portal:default'
AGENDAPROFILE = '{0}:default'.format(AGENDAPROJECTNAME)

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
    'Products.RedirectionTool',
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
        self.pc = self.portal['portal_controlpanel']
        self.qi = self.portal['portal_quickinstaller']
        self.st = self.portal['portal_setup']
        self.pp = self.portal['portal_properties']
        self.pt = self.portal['portal_types']
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

    def desinstala_agenda(self):
        """Desinstala produto brasil.gov.agenda mas 'marca como instalado'.
        Isso é para simular a situação em que o upgrade 10300 marcava o
        brasil.gov.agenda como instalado mas não instalava o seu profile. Ver:
        https://github.com/plonegovbr/brasil.gov.portal/issues/154#issuecomment-78988918
        """
        self.qi.uninstallProducts(products=[AGENDAPROJECTNAME])
        # Marca como instalado. Isso não instala o profile.
        _instala_pacote(self.qi, AGENDAPROJECTNAME)

        # Quando marcamos o produto como instalado, mesmo quando instalamos
        # ele pelo quickinstaller, ele não instala o profile.
        self.qi.installProduct(AGENDAPROJECTNAME)
        self.assertEqual(
            self.st.getLastVersionForProfile(AGENDAPROFILE),
            UNKNOWN)
        types = self.pt.listContentTypes()
        self.assertNotIn('Agenda', types)

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
            'collective.cover.controlpanel.ICoverSettings.available_tiles')
        self.assertIn('banner_rotativo', record)

    def test_to3000_available(self):
        step = self.list_upgrades(u'2000', u'3000')
        self.assertEqual(len(step), 1)

    def test_to3000_execution(self):
        # Executa upgrade
        self.execute_upgrade(u'2000', u'3000')
        record = api.portal.get_registry_record(
            'collective.cover.controlpanel.ICoverSettings.styles')
        self.assertIn('Verde Esporte|verde', record)

    def test_to4000_available(self):
        step = self.list_upgrades(u'3000', u'4000')
        self.assertEqual(len(step), 1)

    def test_to4000_execution(self):
        # Executa upgrade
        self.execute_upgrade(u'3000', u'4000')
        self.assertTrue(self.pp.site_properties.displayPublicationDateInByline)

    def test_to5000_available(self):
        step = self.list_upgrades(u'4000', u'5000')
        self.assertEqual(len(step), 1)

    def test_5000_corrige_pastas(self):
        # Ajustamos as pastas para nao estarem ordenadas
        pastas = ['assuntos', 'imagens']
        for pasta_id in pastas:
            pasta = api.content.create(
                type='Folder',
                container=self.portal,
                id=pasta_id,
            )
            pasta.setOrdering('unordered')
            conteudo = api.content.create(
                type='Folder',
                container=pasta,
                id='sub_{0}'.format(pasta_id),
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
            title=u'Uma notícia',
        )
        noticia.section = 'General'
        noticia.reindexObject(idxs=['section'])
        # Deixa General como secao disponivel
        api.portal.set_registry_record(
            'collective.nitf.controlpanel.INITFSettings.available_sections',
            set([u'General']),
        )
        # Deixa General como padrao
        api.portal.set_registry_record(
            'collective.nitf.controlpanel.INITFSettings.default_section',
            u'General')

    def test_to10300_execution(self):
        self._prepara_to10300()
        controlpanel = api.portal.get_tool('portal_controlpanel')
        # Executa upgrade
        self.execute_upgrade(u'5000', u'10300')
        # Ao acessar a view como site administrator conseguimos acesso
        with api.env.adopt_roles(['Site Administrator']):
            # Listamos todas as acoes do painel de controle
            installed = [a['id'] for a in controlpanel.enumConfiglets(group='Products')]  # NOQA
            # Validamos que o painel de controle da barra esteja instalado
            self.assertTrue('social-config' in installed)
        # Ao acessar a view como anonimo, a excecao e levantada
        with api.env.adopt_roles(['Anonymous']):
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

    def test_to10800_available(self):
        step = self.list_upgrades(u'10700', u'10800')
        self.assertEqual(len(step), 1)

    def test_to10801_available(self):
        step = self.list_upgrades(u'10800', u'10801')
        self.assertEqual(len(step), 1)

    def test_to10802_available(self):
        step = self.list_upgrades(u'10801', u'10802')
        self.assertEqual(len(step), 1)

    def _get_viewlets_from_manager(self, manager):
        """Returns all viewlets from a manager."""
        request = self.portal.REQUEST
        view = View(self.portal, request)
        manager = queryMultiAdapter(
            (self.portal, request, view),
            IViewletManager,
            manager,
            default=None,
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
            self._get_viewlets_from_manager('plone.portaltop'))
        self.assertEqual(len(top_available), len(new_viewlets_top))

        new_viewlets_footer = [u'plone.footer', u'brasil.gov.portal.topo']
        footer_available = self._get_available_viewlets_ids_from_manager(
            new_viewlets_footer,
            self._get_viewlets_from_manager('plone.portalfooter'))
        self.assertEqual(len(footer_available), len(new_viewlets_footer))
        configs = getattr(self.pp, 'brasil_gov', None)
        url_orgao = configs.getProperty('url_orgao')
        self.assertEqual(
            url_orgao,
            u'http://estruturaorganizacional.dados.gov.br/doc/' +
            u'unidade-organizacional/26')

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
                id=pasta_id,
            )
            pasta.setOrdering('unordered')
            conteudo = api.content.create(
                type='Folder',
                container=pasta,
                id='sub_{0}'.format(pasta_id),
            )
            conteudo.setOrdering('unordered')

        for pasta_id in pastas:
            pasta = self.portal[pasta_id]
            self.assertFalse(isinstance(pasta.getOrdering(), DefaultOrdering))

        self.st.setLastVersionForProfile('brasil.gov.tiles:default', '2000')
        self.assertTrue(len(self.st.listUpgrades('brasil.gov.tiles:default')))

        self.execute_upgrade(u'10600', u'10700')

        for pasta_id in pastas:
            pasta = self.portal[pasta_id]
            self.assertTrue(isinstance(pasta.getOrdering(), DefaultOrdering))

        self.assertEqual(len(self.st.listUpgrades('brasil.gov.tiles:default')), 0)

        # Executa o upgrade step com o brasil.gov.agenda desinstalado.
        # Em versões antigas do brasil.gov.portal o brasil.gov.agenda não era
        # instalado. O step que instala produtos de terceiros tem que executar
        # sem erro, quando o brasil.gov.agenda não está instalado.
        self.desinstala_agenda()
        self.execute_upgrade(u'10600', u'10700')
        self.assertEqual(
            self.st.getLastVersionForProfile(AGENDAPROFILE),
            UNKNOWN)

    def test_to10700_execution_different_upgrade_step_order(self):
        """
        Teste para simular a situação de upgrades em ordens diferentes que
        podem quebrar a capa. Ver
        https://github.com/plonegovbr/brasil.gov.portal/issues/289
        """

        # Todo esse teste para testar formato antigo da capa é baseado em
        # https://github.com/collective/collective.cover/blob/985d0faafdd3b3401c2ba56d5c0c2d8aaac2b48e/src/collective/cover/tests/test_upgrades.py#L368
        # Com a diferença de que ao invés de usarmos os upgradeSteps de
        # collective.cover, usaremos os métodos de atualização de terceiros
        # disponibilizados em brasil.gov.portal.

        old_data = (
            u'[{"type": "row", "children": [{"data": {"layout-type": "column", '
            u'"column-size": 16}, "type": "group", "children": [{"tile-type": '
            u'"collective.cover.carousel", "type": "tile", "id": '
            u'"ca6ba6675ef145e4a569c5e410af7511"}], "roles": ["Manager"]}]}]'
        )

        expected = (
            u'[{"type": "row", "children": [{"type": "group", "children": '
            u'[{"tile-type": "collective.cover.carousel", "type": "tile", '
            u'"id": "ca6ba6675ef145e4a569c5e410af7511"}], "roles": '
            u'["Manager"], "column-size": 16}]}]'
        )

        # simulate state on previous version of registry layouts
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ICoverSettings)
        settings.layouts = {
            u'test_layout': old_data,
        }

        with api.env.adopt_roles(['Manager']):
            cover = api.content.create(
                self.portal, 'collective.cover.content',
                'test-cover',
                template_layout='Empty layout',
            )

        cover.cover_layout = old_data

        ps = api.portal.get_tool('portal_setup')

        # Simulo a atualização de terceiros e depois a do brasil.gov.portal que
        # "sobrescreve" o que o collective.cover fez: se for feito exatamente
        # nessa ordem, a capa quebra, como apresentado no relato
        # https://github.com/plonegovbr/brasil.gov.portal/issues/289
        atualiza_produtos_terceiros(ps)
        self.execute_upgrade(u'10600', u'10700')

        # Acontece que agora, dentro do upgrade 10600-10700,
        # em corrige_conteudo_collectivecover, chamo "simplify_layout"
        # novamente bem no fim, corrigindo o problema caso o usuário execute
        # os upgradeSteps nessa ordem problemática.
        self.assertEqual(settings.layouts, {'test_layout': expected})

        self.assertEqual(cover.cover_layout, expected)

    def test_to10800_execution(self):
        # Remove configulet 'portal' para simular estado anterior ao upgrade.
        self.pc.unregisterConfiglet('portal')
        configlets = self.pc.enumConfiglets(group='Products')
        configlets = [a['id'] for a in configlets]
        self.assertNotIn('portal', configlets)
        # Remove records para simular estado anterior ao upgrade.
        registry = getUtility(IRegistry)
        id_esconde_autor = 'brasil.gov.portal.controlpanel.portal.'\
                           'ISettingsPortal.esconde_autor'
        id_esconde_data = 'brasil.gov.portal.controlpanel.portal.'\
                          'ISettingsPortal.esconde_data'
        del registry.records[id_esconde_autor]
        del registry.records[id_esconde_data]

        layouts = {
            u' Layout vazio': (
                u'[{"type": "row", "children": [{"type": "group", '
                u'"data":{"column-size":16, "layout-type":"column"}, '
                u'"roles": ["Manager"]}]}]'
            ),
            u'Destaques': (
                u'[{"type": "row", "children": [{"data": {"layout-type": '
                u'"column", "column-size": 16}, "type": "group", '
                u'"children": [{"tile-type": "em_destaque", "type": "tile", '
                u'"id": "em_destaque_tile_destaque"}], '
                u'"roles": ["Manager"]}]}]'
            ),
        }
        api.portal.set_registry_record(
            name='collective.cover.controlpanel.ICoverSettings.layouts',
            value=layouts)

        layout_registry = api.portal.get_registry_record(
            name='collective.cover.controlpanel.ICoverSettings.layouts')
        self.assertDictEqual(layout_registry, layouts)

        self.execute_upgrade(u'10700', u'10800')

        # Verifica se o configulet 'portal' foi instalado.
        configlets = self.pc.enumConfiglets(group='Products')
        configlets = [a['id'] for a in configlets]
        self.assertIn('portal', configlets)

        # Verifica se o registro esconde_autor existe.
        settings = registry.forInterface(ISettingsPortal)
        self.assertTrue(hasattr(settings, 'esconde_autor'))
        self.assertEqual(settings.esconde_autor, False)

        # Verifica se o registro esconde_data existe.
        self.assertTrue(hasattr(settings, 'esconde_data'))
        self.assertEqual(settings.esconde_data, False)

        layouts = {
            'Layout vazio': [
                {
                    'type': 'row',
                    'children': [
                        {
                            'type': 'group',
                            'column-size': 16,
                            'roles': ['Manager'],
                        },
                    ],
                },
            ],
            'Destaques': [
                {
                    'type': 'row',
                    'children': [{
                        'column-size': 16,
                        'type': 'group',
                        'children': [
                            {
                                'tile-type': 'em_destaque',
                                'type': 'tile',
                                'id': 'em_destaque_tile_destaque',
                            },
                        ],
                        'roles': ['Manager'],
                    }],
                },
            ],
        }

        layout_registry = api.portal.get_registry_record(
            name='collective.cover.controlpanel.ICoverSettings.layouts')
        for name, layout in layouts.items():
            self.assertListEqual(json.loads(layout_registry[name]), layout)

    def test_to10801_execution(self):
        # Simula estado em que os estilos foram alterados.
        record = '{0}.styles'.format(ICoverSettings.__identifier__)
        api.portal.set_registry_record(record,
                                       set(['Novo Estilo|novo-estilo']))

        self.execute_upgrade(u'10800', u'10801')

        expected = [
            'Amarelo|amarelo',
            'Azul Claro - borda|azul-claro-borda',
            'Azul Claro Saude|azul-claro',
            'Azul Escuro Turismo|azul-escuro',
            'Azul Governo|azul',
            'Azul Petroleo Defesa Seguranca|azul-petroleo',
            'Azul Piscina|azul-piscina',
            'Azul Turquesa - borda|azul-turquesa-borda',
            'Azul Turquesa|azul-turquesa',
            'Bege - borda|bege-borda',
            'Bege|bege',
            'Dourado Cultura|dourado',
            'Fio separador|fio-separador',
            'Laranja - borda|laranja-borda',
            'Laranja Cidadania Justica|laranja',
            'Link Externo|link-externo',
            'Lista Horizontal|lista-horizontal',
            'Lista Vertical|lista-vertical',
            'Marrom Claro Economia Emprego|marrom-claro',
            'Marrom Infraestrutura|marrom',
            'Novo Estilo|novo-estilo',
            'Padrao|padrao',
            'Roxo - borda|roxo-borda',
            'Roxo Ciencia Tecnologia|roxo',
            'Verde Claro Meio Ambiente|verde-claro',
            'Verde Escuro Educacao|verde-escuro',
            'Verde Esporte|verde',
        ]
        styles = sorted(api.portal.get_registry_record(record))
        self.assertEqual(styles, expected)

        # Executa upgrade quando brasil.gov.agenda não está instalado.
        self.desinstala_agenda()
        self.execute_upgrade(u'10800', u'10801')
        self.assertNotEqual(
            self.st.getLastVersionForProfile(AGENDAPROFILE),
            UNKNOWN)

    def test_to10802_execution(self):
        # Simula situação antiga
        old_selectable_views = ('folder_listing', 'news_listing')
        self.portal.manage_changeProperties(
            selectable_views=old_selectable_views)
        selectable_views_property = self.portal.getProperty('selectable_views')
        self.assertTupleEqual(selectable_views_property, old_selectable_views)

        self.execute_upgrade(u'10801', u'10802')

        selectable_views_property = self.portal.getProperty('selectable_views')
        self.assertTupleEqual(selectable_views_property, SELECTABLE_VIEWS)

    def test_css_upload_before_css_portlet_calendar_first_install(self):
        portal_css = api.portal.get_tool('portal_css')
        upload_css_id = '++resource++collective.upload/upload.css'
        portlet_calendar_css_id = '++resource++calendar_styles/calendar.css'
        upload_pos = portal_css.getResourcePosition(upload_css_id)
        calendar_pos = portal_css.getResourcePosition(portlet_calendar_css_id)
        self.assertLess(upload_pos, calendar_pos)

    def test_upgrade_step_variavel_hidden_profiles_deps_brasil_gov_portal(self):  # NOQA
        """
        Testa se todos os upgradeSteps de brasil.gov.portal que possuem profile
        estão nas variáveis HIDDEN_PROFILES e DEPS. Outros pacotes podem ser
        adicionados em outros testes.
        """
        upgradeSteps = listUpgradeSteps(self.st, self.profile, '')
        upgrades = [upgrade[0]['dest'][0] for upgrade in upgradeSteps]

        upgrades_hidden_profiles = []
        upgrades_deps = []
        prefix = 'brasil.gov.portal.upgrades.v%s'
        profile = self.profile.split(':')[-1]
        installable_profiles = self.qi.listInstallableProfiles()
        for upgrade in upgrades:
            upgrade_profile = prefix % upgrade
            # Verifica somente upgrades que possuem profiles
            if upgrade_profile in installable_profiles:
                upgrades_deps.append(upgrade_profile)
                upgrades_hidden_profiles.append(
                    '{0}:{1}'.format(upgrade_profile, profile))

        self.assertTrue(all(upgrade in HIDDEN_PROFILES
                            for upgrade in upgrades_hidden_profiles))

        self.assertTrue(all(upgrade in DEPS for upgrade in upgrades_deps))

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
        last_upgrade = sorted(upgrades, key=LooseVersion)[-1]
        self.assertEqual(upgrade_info['installedVersion'],
                         last_upgrade)
