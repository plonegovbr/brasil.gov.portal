# -*- coding: utf-8 -*-
from brasil.gov.portal.logger import logger
from plone import api
from plone.app.upgrade.utils import loadMigrationProfile

import json


def atualiza_layouts_capa(context):
    """ Atualiza as configurações de layout da capa para a nova versão do
        collective.cover
    """
    layout_registry = api.portal.get_registry_record(
        name='collective.cover.controlpanel.ICoverSettings.layouts')
    cover_layouts = {}
    for name, json_layouts in layout_registry.items():
        layouts = []
        for layout in json.loads(json_layouts):
            children = []
            for child in layout['children']:
                if 'data' in child:
                    data = child.pop('data')
                    child['column-size'] = data['column-size']
                children.append(child)
            layout['children'] = children
            layouts.append(layout)
        cover_layouts[name.strip()] = unicode(json.dumps(layouts))

    api.portal.set_registry_record(
        name='collective.cover.controlpanel.ICoverSettings.layouts',
        value=cover_layouts)


def apply_profile(context):
    """Atualiza profile para versao 10800."""
    profile = 'profile-brasil.gov.portal.upgrades.v10800:default'
    loadMigrationProfile(context, profile)
    logger.info('Atualizado para versao 10800')
