# -*- coding: utf-8 -*-
from brasil.gov.portal.testing import INTEGRATION_TESTING
from collective.cover.controlpanel import ICoverSettings
from collective.nitf.controlpanel import INITFSettings
from collective.upload.interfaces import IUploadSettings
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

import unittest


class AddonsSettingsTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.registry = getUtility(IRegistry)
        self.nitf_settings = self.registry.forInterface(INITFSettings)
        self.wt = self.portal['portal_workflow']
        self.pm = self.portal['portal_membership']

    def test_collective_cover_available_tyles_settings(self):
        """ Tiles disponiveis no collective.cover
        """
        settings = self.registry.forInterface(ICoverSettings)
        expected = [
            'agenda',
            'audio',
            'audiogallery',
            'collective.cover.banner',
            'collective.cover.carousel',
            'collective.cover.collection',
            'collective.cover.list',
            'collective.cover.richtext',
            'standaloneheader',
            'video',
            'videogallery',
        ]
        available_tiles = settings.available_tiles
        available_tiles.sort()
        self.assertListEqual(available_tiles, expected)

    def test_collective_cover_content_type_settings(self):
        """ Tipos de conteudo buscaveis no cover
        """
        settings = self.registry.forInterface(ICoverSettings)
        allowed_types = [
            u'collective.nitf.content',
            u'collective.polls.poll',
            u'Collection',
            u'FormFolder',
            u'Image',
            u'Document',
            u'Link',
        ]
        self.assertListEqual(settings.searchable_content_types, allowed_types)

    def test_collective_cover_styles_settings(self):
        """Tile styles available on collective.cover configuration."""
        settings = self.registry.forInterface(ICoverSettings)
        expected = {
            'Box Branco|box-branco',
            'Box Colorido|box-colorido',
            'Box Escuro|box-escuro',
            'Colunas Destacadas|colunas-destacadas',
            'Colunas Discretas|colunas-discretas',
            'Colunas Quadradas|colunas-quadradas',
            'Com Etiqueta|tile-etiqueta',
            'Com Multimidia|com-multimidia',
            'Degrade para destaque topo|topo-com-degrade',
            'Discreto|tile-discreto',
            'FAQ|tile-faq',
            'Foto destacada grande|foto-destacada-grande',
            'Foto Sobreposta Grande|foto-sobreposta-grande',
            'Foto Sobreposta Pequena|foto-sobreposta-pequena',
            'Foto Sobreposta|foto-sobreposta',
            'Fundo topo claro|fundo-topo-claro',
            'Fundo topo escuro|fundo-topo-escuro',
            'Linha destacada|linha-destacada',
            'Linha destaque topo|linha-destaquetopo',
            'Linha discreta|linha-discreta',
            'Linha recuada|linha-recuada',
            'Lista Blocos|lista-blocos',
            'Lista em Alta|tile-em-alta',
            'Noticia Destaque|tile-noticia-destaque',
            'Noticia Vinculada|tile-vinculada',
            'Tile Transparente|tile-transparente',
            'Titulo Fio Separador|fio-separador',
        }
        styles = list(settings.styles)
        self.assertItemsEqual(styles, expected)

    def test_collective_nitf_available_genres(self):
        """ Genres used portal wide.
        """
        available_genres = list(self.nitf_settings.available_genres)
        available_genres.sort()
        expected_genres = [
            u'Analysis',
            u'Archive material',
            u'Current',
            u'Exclusive',
            u'From the Scene',
            u'Interview',
            u'Obituary',
            u'Opinion',
            u'Polls and Surveys',
            u'Press Release',
            u'Profile',
            u'Retrospective',
            u'Review',
            u'Special Report',
            u'Summary',
            u'Wrap',
        ]
        self.assertListEqual(available_genres, expected_genres)

    def test_collective_nitf_available_sections(self):
        """ News sections defined.
        """
        available_sections = list(self.nitf_settings.available_sections)
        available_sections.sort()
        expected = [
            u'Geral',
            u'Notícias',
        ]
        self.assertListEqual(available_sections, expected)

    def test_collective_nitf_default_section(self):
        self.assertEqual(self.nitf_settings.default_section, u'Notícias')

    def test_collective_upload_settings(self):
        # images uploaded must be smaller than 1024x1024
        settings = self.registry.forInterface(IUploadSettings)
        self.assertEqual(settings.resize_max_width, 1024)
        self.assertEqual(settings.resize_max_height, 1024)
        self.assertEqual(
            settings.upload_extensions, u'gif|jpeg|jpg|png|pdf|doc|txt|docx')

    def test_sc_social_likes_settings(self):
        from sc.social.like.interfaces import ISocialLikeSettings
        settings = self.registry.forInterface(ISocialLikeSettings)
        types_expected = (
            'Audio',
            'collective.cover.content',
            'collective.nitf.content',
            'collective.polls.poll',
            'Document',
            'Event',
            'Image',
            'sc.embedder',
        )
        self.assertTupleEqual(settings.enabled_portal_types, types_expected)
